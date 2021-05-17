from datetime import date, datetime, timedelta
import pandas as pd
import flask
from sqlalchemy import extract, asc, desc, func, column, case, text
from app import db, app

today = date.today()
first_of_this_month = today.replace(day=1)
last_of_prev_month = first_of_this_month - timedelta(days=1)
first_of_prev_month = last_of_prev_month.replace(day=1)
minus_13_months = (first_of_this_month - timedelta(days=390)).replace(day=1)

class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	accName = db.Column(db.String, unique=True, nullable=False)
	transactions = db.relationship("Transaction", back_populates="account", cascade="all, delete", passive_deletes=True)
	taggroups = db.relationship('Taggroup', back_populates="account", cascade="all, delete", passive_deletes=True)
	conditions = db.relationship('Condition', back_populates="account", cascade="all, delete", passive_deletes=True)
	descriptions = db.relationship('Description', back_populates="account", cascade="all, delete", passive_deletes=True)

	def __repr__(self):
		return '<Account {}>'.format(self.accName)

	def create_one(newAccName):
		stmt = Account(accName=newAccName)
		db.session.add(stmt)
		db.session.commit()

	def one_acc(account_id):
		return Account.query.filter_by(id = account_id).first()

	def delete_account(account_id):
		#PRAGMA... https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys
		cursor = db.session.execute(text("PRAGMA foreign_keys=ON")).cursor
		q = db.session.query(Account).filter(Account.id==account_id).first()
		db.session.delete(q)
		db.session.commit()
	
	def list_newest():
		return db.session.query(func.max(Account.id).label('lastid')).scalar()

	def list_acc():
		cte = db.session.query(\
							Transaction.acc_id\
							,Transaction.amount.label('balance')\
							,func.row_number().over(partition_by=Transaction.acc_id, order_by=desc(Transaction.traDate)).label("rn"))\
						.outerjoin(Tag)\
						.filter(Tag.isBlnc==1)\
						.cte()
		q1 = db.session.query(cte.c.acc_id, cte.c.balance).filter(cte.c.rn == 1).subquery()
		q2 = db.session.query(Account.id, Account.accName, func.max(func.date(Transaction.uplDate)).label('upldate'))\
			.outerjoin(Transaction)\
			.group_by(Account.id, Account.accName)\
			.subquery()
		return db.session.query(q2.c.id, q2.c.accName, q2.c.upldate, q1.c.balance)\
			.outerjoin(q1, q2.c.id == q1.c.acc_id)

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	traDate = db.Column(db.Date, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	desc = db.Column(db.String, nullable=False)
	card = db.Column(db.String(1), nullable=False)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=True)
	acc_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'))
	uplDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
	confirmed = db.Column(db.Boolean, nullable=True, default=False)
	account = db.relationship('Account', back_populates='transactions')

	def __repr__(self):
		return '<Transaction {}>'.format(self.desc)

	def create_one(tDate, tAmnt, tDesc, tag, acc, card, confrm):
		date_obj = datetime.strptime(tDate,'%Y-%m-%d')
		stmt = Transaction(traDate=date_obj, amount=tAmnt, desc=tDesc, card=card, tag_id=tag, acc_id=acc, confirmed=confrm)
		db.session.add(stmt)
		db.session.commit()

	def update_trans(tid, traDate, amount, desc, tag):
		date_obj = datetime.strptime(traDate,'%Y-%m-%d')
		stmt = Transaction.query.filter_by(id=tid).first()
		stmt.traDate = date_obj
		stmt.amount = amount
		stmt.desc = desc
		stmt.tag_id = tag
		stmt.confirmed = 1
		db.session.commit()

	def update_trans_amount(tid, amount):
		stmt = Transaction.query.filter_by(id=tid).first()
		stmt.amount = amount
		db.session.commit()

	def update_desc(account_id, desc_from, desc_to):
		db.session.query(Transaction)\
			.filter(Transaction.desc.like('%'+ desc_from +'%'))\
			.update({Transaction.desc: func.replace(Transaction.desc, desc_from, desc_to)}
            ,synchronize_session=False)		
		db.session.commit()

	def delete_trans(tid):
		stmt = Transaction.query.filter_by(id=tid).first()
		db.session.delete(stmt)
		db.session.commit()

	def cnt_all(account_id):
		return Transaction.query.with_entities(func.count(Transaction.id).label('cnt'))\
				.filter(Transaction.acc_id == account_id).one_or_none()

	def cnt_new(account_id):
		return Transaction.query.with_entities(func.count(Transaction.id).label('cnt'))\
				.filter(Transaction.acc_id == account_id, Transaction.confirmed == 0).one_or_none()

	def cnt_avg_sum_filtered(account_id, date_from, date_to, sel_tags):
		return Transaction.query\
				.with_entities(func.count(Transaction.amount).label('a_cnt'), func.avg(Transaction.amount).label('a_avg'), func.sum(Transaction.amount).label('a_sum'))\
				.filter(Transaction.acc_id == account_id, Transaction.traDate >= date_from, Transaction.traDate <= date_to, Transaction.tag_id.in_(sel_tags)).one_or_none()

	def list_filtered(account_id, date_from, date_to, sel_tags):
		return Transaction.query.filter(Transaction.acc_id == account_id\
								,Transaction.traDate >= date_from\
								,Transaction.traDate <= date_to\
								,Transaction.tag_id.in_(sel_tags))\
							.order_by(Transaction.traDate.desc(), Transaction.amount)

	def cnt_avg_sum_filtered_new(account_id, date_from, date_to):
		return Transaction.query\
				.with_entities(func.count(Transaction.amount).label('a_cnt'), func.avg(Transaction.amount).label('a_avg'), func.sum(Transaction.amount).label('a_sum'))\
				.filter(Transaction.acc_id == account_id, Transaction.traDate >= date_from, Transaction.traDate <= date_to, Transaction.confirmed == 0).one_or_none()

	def list_filtered_new(account_id, date_from, date_to):
		return Transaction.query.filter(Transaction.acc_id == account_id, Transaction.traDate >= date_from, Transaction.traDate <= date_to, Transaction.confirmed == 0)\
				.order_by(Transaction.traDate.desc(), Transaction.amount)

	def list_latest_uploads_by_card(account_id, card):
		return db.session.query(Transaction.card, Transaction.desc, Transaction.traDate, Transaction.amount)\
				.filter(Transaction.acc_id == account_id, Transaction.card == card)\
				.order_by(Transaction.traDate.desc()).limit(3).all()

	def first_date(account_id):
		return db.session.query(db.func.min(Transaction.traDate)).filter(Transaction.acc_id==account_id).scalar() or today

	def last_date(account_id):
		return db.session.query(db.func.max(Transaction.traDate)).filter(Transaction.acc_id==account_id).scalar() or today

	def count_months(account_id):
		return db.session.query(func.strftime('%Y%m',Transaction.traDate))\
			.filter(Transaction.acc_id == account_id, Transaction.traDate < first_of_this_month)\
			.distinct().count()

	def max_year(account_id):
		return Transaction.query\
				.with_entities(extract('year',func.max(Transaction.traDate).label('max_year')))\
				.filter(Transaction.acc_id == account_id).scalar()

	def list_year(account_id):
		return db.session.query(extract('year',Transaction.traDate).label('year'))\
				.filter(Transaction.acc_id == account_id).distinct().order_by(desc('year'))

	def chart_header(column_name, account_id):
		subquery = db.session.query(Tag.tgr_id).filter(getattr(Tag, column_name)==1, Taggroup.acc_id==account_id)
		return db.session.query(Taggroup.gName, Taggroup.gColor)\
				.filter(Taggroup.id.in_(subquery))\
				.order_by(Taggroup.gName)

	def chart_data(account_id, column_name, months):
		first_of_n_month = (first_of_this_month - timedelta(days=months*30)).replace(day=1)
		q = db.session.query(Taggroup.gName
							,func.strftime('%Y%m',Transaction.traDate).label('orderByCol')\
							,func.strftime('%m',Transaction.traDate).label('mnth')\
							,func.SUM(Transaction.amount).label('total'))\
    					.outerjoin(Tag, Transaction.tag_id == Tag.id)\
						.outerjoin(Taggroup, Taggroup.id == Tag.tgr_id)\
    					.filter(Transaction.acc_id == account_id\
								,Transaction.confirmed == 1\
								,Transaction.traDate >= first_of_n_month\
								,Transaction.traDate < first_of_this_month\
								,getattr(Tag, column_name)==1)\
						.group_by(Taggroup.gName\
								,func.strftime('%Y%m',Transaction.traDate)\
								,func.strftime('%m',Transaction.traDate).label('mnth'))\
						.order_by('orderByCol',Taggroup.gName)

		#get unique groups
		g = []
		prev_val = ''
		for row in q:
			if row.gName != prev_val:
				g.append(row.gName)
			prev_val = row.gName

		#create months/group with default value 
		mon_dict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
		m = {}
		prev_val = ''
		for row in q:
			if row.mnth != prev_val:
				m[mon_dict[row.mnth]] = {g_:0 for g_ in g}
			prev_val = row.mnth
		
		#replace values in dict if exists in q
		for row in q:
			for key in m:
				for mk in m[key]:
					if mon_dict[row.mnth]==key and mk==row.gName :
						m[key][mk] = row.total
		return m

	def get_dates(what_year_):
		what_year = int(what_year_)
		prev_year = what_year - 1
		prev_month_num = last_of_prev_month.strftime("%m")
		prev_month = int(prev_month_num) - 1 if int(prev_month_num) > 1 else 12
		year_num = last_of_prev_month.strftime("%Y")
		which_year = year_num if int(year_num) == what_year else prev_year
		which_month = prev_month_num if int(year_num) == what_year else prev_month
		end_12_month = last_of_prev_month.replace(year=what_year)
		start_12_month = (end_12_month - timedelta(days=360)).replace(day=1)
		return what_year, prev_year, which_year, which_month, start_12_month, end_12_month

	def get_stats_year(account_id, what_year, lbl1, lbl2):
		return db.session.query(Tag.tgr_id.label(lbl1), func.SUM(Transaction.amount).label(lbl2))\
			.outerjoin(Tag, Transaction.tag_id == Tag.id)\
			.filter(Transaction.acc_id == account_id, Transaction.confirmed == 1, Tag.isBlnc == 0, extract('year',Transaction.traDate)==what_year)\
			.group_by(Tag.tgr_id).subquery()

	def get_statsDate(what_year):
		gd = Transaction.get_dates(what_year)
		fopm = first_of_prev_month.replace(year=int(gd[2]))
		lopm = last_of_prev_month.replace(year=int(gd[2])) #, hour=23, minute=59, second=59 )
		return [str(gd[1])+'-01-01', str(gd[1])+'-12-31', str(gd[0])+'-01-01', str(gd[0])+'-12-31', str(fopm), str(lopm)]

	def get_stat_year(account_id, what_year):
		gd = Transaction.get_dates(what_year)
		tg = Taggroup.list_tgroup_id_inSum(account_id)
		q1 = db.session.query(Tag.tgr_id.label('tag1'), Taggroup.gName.label('Category'), Taggroup.gColor.label('color'), func.SUM(Transaction.amount).label('Total'))\
    		.outerjoin(Tag, Transaction.tag_id == Tag.id)\
			.outerjoin(Taggroup, Taggroup.id == Tag.tgr_id)\
    		.filter(Transaction.acc_id == account_id, Transaction.confirmed == 1, Tag.isBlnc == 0, extract('year',Transaction.traDate)<=gd[0])\
			.group_by(Tag.tgr_id, Taggroup.gName, Taggroup.gColor)\
			.order_by(Tag.tgr_id).subquery()
		q2 = Transaction.get_stats_year(account_id, gd[1], 'tag2', 'Prev_Year')
		q3 = Transaction.get_stats_year(account_id, gd[0], 'tag3', 'This_Year')
		month_count = Transaction.count_months(account_id) if Transaction.count_months(account_id) < 12 else 12
		q4 = db.session.query(Tag.tgr_id.label('tag4'), func.SUM(Transaction.amount/month_count).label('Avg_Month'))\
			.outerjoin(Tag, Transaction.tag_id == Tag.id)\
			.filter(Transaction.acc_id == account_id, Transaction.confirmed == 1, Transaction.traDate>=gd[4], Transaction.traDate<gd[5])\
			.group_by(Tag.tgr_id).subquery()
		q5 = db.session.query(Tag.tgr_id.label('tag5'), func.SUM(Transaction.amount).label('Prev_Month'))\
			.outerjoin(Tag, Transaction.tag_id == Tag.id)\
			.filter(Transaction.acc_id == account_id, Transaction.confirmed == 1, extract('year',Transaction.traDate)==gd[2], extract('month',Transaction.traDate)==gd[3])\
			.group_by(Tag.tgr_id).subquery()
		return db.session.query(q1.c.Category, q1.c.tag1, q1.c.Total, q2.c.Prev_Year, q3.c.This_Year, (100*(q3.c.This_Year/q2.c.Prev_Year)).label('%_YTD'), q4.c.Avg_Month, q5.c.Prev_Month, q1.c.color)\
			.outerjoin(q2, q1.c.tag1 == q2.c.tag2)\
			.outerjoin(q3, q1.c.tag1 == q3.c.tag3)\
			.outerjoin(q4, q1.c.tag1 == q4.c.tag4)\
			.outerjoin(q5, q1.c.tag1 == q5.c.tag5)\
			.order_by(q1.c.tag1)

	def get_stat_year_df(account_id, what_year):
		tg = Taggroup.list_tgroup_id_inSum(account_id)
		q = Transaction.get_stat_year(account_id, what_year)
		df = pd.read_sql_query(q.statement, db.session.bind)
		#transform valies from object to float
		pd.options.display.float_format = '{:.2f}'.format
		#exclude BILLS from summary
		s = df.mask(~df['tag1'].isin(tg)).drop('tag1',1).sum()
		#calculate '% YTD'
		s.loc['%_YTD'] = 100*(s['This_Year'] / s['Prev_Year']) if s['Prev_Year']!=0 else 0
		#replace calculated value in specific position
		df.loc[len(df)] = s
		#replace summarised categ name
		df = df.fillna({'Category':'Summary','tag1':0,'color':''})
		#replace 'NaN' to '0', then limit decimals to 2
		return df.fillna(0).round(2)

	def get_stat_year_by_year(account_id):
		tg = Taggroup.list_tgroup_id_inSum(account_id)
		q = db.session.query( Tag.tgr_id.label('tag')\
							, Taggroup.gName.label('Category')\
							, Transaction.traDate.label('date')\
							, Transaction.amount)\
    		.outerjoin(Tag, Transaction.tag_id == Tag.id)\
			.outerjoin(Taggroup, Taggroup.id == Tag.tgr_id)\
    		.filter(Transaction.acc_id == account_id, Transaction.confirmed == 1, Tag.isBlnc == 0)\
			.order_by(Tag.tgr_id)
		df = pd.read_sql_query(q.statement, db.session.bind)
		#add column 'year' based on 'date'
		df['Year'] = pd.DatetimeIndex(df['date']).year
		#groupby
		df = df.groupby(['tag','Category','Year']).sum()
		#pivot
		df = pd.pivot_table(df, values = 'amount', index=['Category','tag'], columns = 'Year')\
			.sort_values(by=['tag'], ascending=True)
		#add column 'Total', to sum horizontally, per category
		df.insert(loc=0, column='Total', value=df.sum(axis=1))
		#add row 'Summary' to sum columns, except BILLS
		df.loc['Summary'] = df.query("tag in @tg").sum()
		#change FLOAT values to INT
		return df.fillna(0).astype(int)

	def chart_in_out(account_id):
		sum_in  = Transaction.query.with_entities(func.ABS(func.SUM(Transaction.amount)))\
				.outerjoin(Tag)\
				.filter(Transaction.acc_id == account_id, Transaction.amount > 0 \
					, Tag.isBlnc == 0 \
					, Transaction.traDate>=first_of_prev_month, Transaction.traDate<first_of_this_month)\
				.scalar()
		sum_out = Transaction.query.with_entities(func.ABS(func.SUM(Transaction.amount)))\
				.outerjoin(Tag)\
				.filter(Transaction.acc_id == account_id, Transaction.amount < 0 \
					, Tag.isBlnc == 0 \
					, Transaction.traDate>=first_of_prev_month, Transaction.traDate<first_of_this_month)\
				.scalar()
		return sum_in if sum_in is not None else 0, sum_out if sum_out is not None else 0

	def chart_monthly_trend(account_id):
		tag_inSum = Tag.list_tag_id_inSum(account_id)
		case_expr = case([
					(func.strftime('%m',Transaction.traDate) == '01', 'Jan')
				,],
        	else_ = func.strftime('%m',Transaction.traDate)).label("mmm")
		month_by_month = db.session.query(\
							func.strftime('%Y%m',Transaction.traDate).label('orderByCol')\
							,func.strftime('%m',Transaction.traDate).label('mnth')\
							,func.SUM(Transaction.amount).label('total')\
							,column('Dummy')\
							,case([
								(func.strftime('%m',Transaction.traDate) == '01', 'Jan'),
								(func.strftime('%m',Transaction.traDate) == '02', 'Feb'),
								(func.strftime('%m',Transaction.traDate) == '03', 'Mar'),
								(func.strftime('%m',Transaction.traDate) == '04', 'Apr'),
								(func.strftime('%m',Transaction.traDate) == '05', 'May'),
								(func.strftime('%m',Transaction.traDate) == '06', 'Jun'),
								(func.strftime('%m',Transaction.traDate) == '07', 'Jul'),
								(func.strftime('%m',Transaction.traDate) == '08', 'Aug'),
								(func.strftime('%m',Transaction.traDate) == '09', 'Sep'),
								(func.strftime('%m',Transaction.traDate) == '10', 'Oct'),
								(func.strftime('%m',Transaction.traDate) == '11', 'Nov'),
								(func.strftime('%m',Transaction.traDate) == '12', 'Dec'),
								],
        						else_ = func.strftime('%m',Transaction.traDate)).label("mmm")
							)\
							.filter(Transaction.tag_id.in_(tag_inSum), Transaction.traDate>=minus_13_months, Transaction.traDate<first_of_this_month)\
							.group_by(func.strftime('%Y%m',Transaction.traDate),func.strftime('%m',Transaction.traDate),column('Dummy'))\
							.subquery()
		month_count = Transaction.count_months(account_id) if Transaction.count_months(account_id) < 13 else 13
		month_avg = db.session.query(\
							column('orderByCol')\
							,column('MON')\
							,func.SUM(Transaction.amount/month_count).label('total_avg')\
							,column('Dummy')\
							,column('Dummy2'))\
							.filter(Transaction.tag_id.in_(tag_inSum), Transaction.traDate>=minus_13_months, Transaction.traDate<first_of_this_month)\
							.subquery()
		return db.session.query(month_by_month.c.orderByCol\
								,month_by_month.c.mnth\
								,month_by_month.c.total\
								,month_avg.c.total_avg\
								,month_by_month.c.mmm\
								)\
				.outerjoin(month_by_month, month_by_month.c.Dummy == month_avg.c.Dummy)\
				.order_by(month_by_month.c.orderByCol)
		
class Taggroup(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	gName = db.Column(db.String, nullable=False)
	gColor = db.Column(db.String(11), nullable=False)
	acc_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), nullable=True)
	account = db.relationship('Account', back_populates='taggroups')
	tags = db.relationship('Tag', back_populates="taggroup", cascade="all, delete", passive_deletes=True)

	def __repr__(self):
		return '<TagGroup {}>'.format(self.gName)

	def insert_tag_group(g_name, color, accid):
		stmt = Taggroup(gName=g_name, gColor=color, acc_id=accid)
		db.session.add(stmt)
		db.session.commit()
		newid = stmt.id 

	def update_tag_group(gid, g_name, color):
		stmt = Taggroup.query.filter_by(id=gid).first()
		stmt.gName = g_name
		stmt.gColor = color
		db.session.commit()

	def delete_tag_group(gid):
		stmt = Taggroup.query.filter_by(id=gid).first()
		db.session.delete(stmt)
		db.session.commit()

	def list_tgroup(account_id):
		return Taggroup.query.filter(Taggroup.acc_id == account_id).order_by(Taggroup.id)

	def list_tgroup_id(account_id):
		q = db.session.query(Taggroup.id).filter(Taggroup.acc_id==account_id).order_by(Taggroup.id).all()
		return [val for val, in q]

	def list_tgroup_id_one(account_id):
		return db.session.query(func.max(Taggroup.id).label('id')).filter(Taggroup.acc_id==account_id).scalar()

	def list_count(account_id):
		return db.session.query(db.func.count(Taggroup.id)).filter(Taggroup.acc_id==account_id).scalar()
	
	def list_tgroup_id_inSum(account_id):
		q = db.session.query(Taggroup.id)\
			.outerjoin(Tag)\
			.filter(Tag.inSum==1, Taggroup.acc_id==account_id)\
			.distinct()
		return [val for val, in q]

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	tName = db.Column(db.String, nullable=False)
	tgr_id = db.Column(db.Integer, db.ForeignKey('taggroup.id', ondelete='CASCADE'), nullable=True)
	isBlnc = db.Column(db.Boolean, nullable=False, default=0)
	inSum = db.Column(db.Boolean, nullable=False, default=1)
	chart1 = db.Column(db.Boolean, nullable=False, default=0)
	chart2 = db.Column(db.Boolean, nullable=False, default=0)
	chart3 = db.Column(db.Boolean, nullable=False, default=0)
	taggroup = db.relationship('Taggroup', back_populates='tags')

	def __repr__(self):
		return '<Tag {}>'.format(self.tName)

	def insert_tag(t_name, g_id, balance, summary, c1, c2, c3):
		stmt = Tag(tName=t_name, tgr_id=g_id, isBlnc=balance, inSum=summary, chart1=c1, chart2=c2, chart3=c3)
		db.session.add(stmt)
		db.session.commit()

	def update_tag(tid, t_name, g_id, balance, summary, c1, c2, c3):
		stmt = Tag.query.filter_by(id=tid).first()
		stmt.tName = t_name
		stmt.tgr_id = g_id
		stmt.isBlnc = balance
		stmt.inSum = summary
		stmt.chart1 = c1
		stmt.chart2 = c2
		stmt.chart3 = c3
		db.session.commit()

	def delete_tag(tid):
		stmt = Tag.query.filter_by(id=tid).first()
		db.session.delete(stmt)
		db.session.commit()

	def list_tag(account_id):
		return db.session.query(Tag.id ,Tag.tName ,Tag.tgr_id ,Tag.isBlnc ,Tag.inSum ,Tag.chart1 ,Tag.chart2 ,Tag.chart3)\
			.outerjoin(Taggroup)\
			.filter(Taggroup.acc_id==account_id)\
			.order_by(Tag.tgr_id, Tag.id)

	def list_tag_id(account_id):
		q = db.session.query(Tag.id)\
			.outerjoin(Taggroup)\
			.filter(Taggroup.acc_id==account_id)
		return [val for val, in q]

	def list_tag_id_of_group(grpid,account_id):
		q = db.session.query(Tag.id)\
			.outerjoin(Taggroup)\
			.filter(Tag.tgr_id==grpid, Taggroup.acc_id==account_id)
		return [val for val, in q]

	def list_tag_id_inSum(account_id):
		q = db.session.query(Tag.id)\
			.outerjoin(Taggroup)\
			.filter(Tag.inSum==1, Taggroup.acc_id==account_id)
		return [val for val, in q]

	def list_count(account_id):
		return db.session.query(db.func.count(Tag.id))\
			.outerjoin(Taggroup)\
			.filter(Taggroup.acc_id==account_id).scalar()

class Condition(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	cName = db.Column(db.String, nullable=False)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)
	acc_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), nullable=True)
	account = db.relationship('Account', back_populates='conditions')

	def __repr__(self):
		return '<Condition {}>'.format(self.cName)

	def insert_cond(cname, tag, accid):
		stmt = Condition(cName=cname, tag_id=tag, acc_id=accid)
		db.session.add(stmt)
		db.session.commit()

	def update_cond(cid, cName, tag):
		stmt = Condition.query.filter_by(id=cid).first()
		stmt.cName = cName
		stmt.tag_id = tag
		db.session.commit()

	def delete_cond(cid):
		stmt = Condition.query.filter_by(id=cid).first()
		db.session.delete(stmt)
		db.session.commit()

	def list_cond(account_id):
		return db.session.query(Condition.id, Condition.cName, Condition.tag_id)\
    		.outerjoin(Tag, Condition.tag_id == Tag.id)\
    		.filter(Condition.acc_id == account_id)\
			.order_by(Tag.tgr_id, Condition.tag_id, Condition.id)

	def list_count(account_id):
		return db.session.query(db.func.count(Condition.id)).filter(Condition.acc_id==account_id).scalar()

class Description(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	descfrom = db.Column(db.String, nullable=False)
	descto = db.Column(db.String, nullable=True)
	acc_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'), nullable=True)
	account = db.relationship('Account', back_populates='descriptions')

	def __repr__(self):
		return '<Condition {}>'.format(self.descfrom)

	def insert_desc(descfrom, descto, accid):
		stmt = Description(descfrom=descfrom, descto=descto, acc_id=accid)
		db.session.add(stmt)
		db.session.commit()

	def update_desc(id, descfrom, descto):
		stmt = Description.query.filter_by(id=id).first()
		stmt.descfrom = descfrom
		stmt.descto = descto
		db.session.commit()

	def delete_desc(id):
		stmt = Description.query.filter_by(id=id).first()
		db.session.delete(stmt)
		db.session.commit()

	def list_desc(account_id):
		return Description.query.filter(Description.acc_id == account_id).order_by(Description.descfrom)

	def list_count(account_id):
		return db.session.query(db.func.count(Description.id)).filter(Description.acc_id==account_id).scalar()

#create all tables based on models above
with app.app_context():
    db.create_all()
