from datetime import datetime
from app import app, db
from flask import render_template, request, redirect, session, flash, url_for, jsonify
from app.models import Account, Transaction, Taggroup, Tag, Condition, Description
import os,re

##----------------------------------------------------------------------------------------------------Index Page
@app.route('/', methods=['GET', 'POST'])
def index():
	templateData = {
		'accounts' : Account.list_acc()
	}
	session['filter_from'] = None
	session['filter_to'] = None
	session['filter_tag'] = None
	if request.method=='POST' and request.form['action']=='addAccount':
		newAccName = request.form['accName']
		Account.create_one(newAccName)
		accountid = Account.list_newest()
		Taggroup.insert_tag_group('New Tag Group - EDIT THIS', '#000000', accountid)
		last_group_id = Taggroup.list_tgroup_id_one(accountid)
		Tag.insert_tag('New Tag - EDIT THIS', last_group_id, 0,1,0,0,0)
		flash('New Account Created','success')
		return redirect(url_for('index'))
	elif request.method=='POST' and request.form['action']=='deleteAccount':
		accid = request.form['del_acc']
		Account.delete_account(accid)
		flash('The Account Has Been Deleted','success')
		return redirect(url_for('index'))
	else:
		return render_template("/index.html",**templateData)

##----------------------------------------------------------------------------------------------------Overview Page
@app.route("/overview/<accountid>", methods=['GET','POST'])
def overview(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='uploadStatement':
		#verify file extension
		def allowed_file(filename):
			return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

		card = request.form['card']
		file = request.files['file']
		if file and not allowed_file(file.filename):
			flash('This file type is not accepted, must be a *.qif statement', 'warning')
			return redirect(url_for('overview', accountid=accountid))
		else:
			#get conditions into dictionary
			conditions = Condition.list_cond(accountid)
			cond_dict = {}
			for cond in conditions:
				cond_dict[cond.cName] = cond.tag_id

			#get descriptions into dictionary
			descriptions = Description.list_desc(accountid)
			desc_dict = {}
			for desc in descriptions:
				desc_dict[desc.descfrom] = desc.descto

			data_file = os.path.join(app.config['DOWNLOADED_STATEMENT'], file.filename)
			with open(data_file, mode='r', encoding = "ISO-8859-1") as fr:
				data = fr.read()
				#cleanse data and combine into 1 line per transaction
				data = data.replace("\nT",";")									#remove line break with 'T' and seprate with comma
				data = data.replace("\nP",";")									#remove line break with 'P' and separate with comma
				#data = data.replace("\nM** "," **")							#remove line break with 'M' and join to the transaction description
				data = data.replace("\n^","")									#remove blank lines
				data = data.replace("&amp;"," and ")							#replace ampersand symbol to text
				data = re.sub("\nN\d{8}","",data)								#remove line break with 'N'
				data = re.sub("\nM.+|\nM","",data)								#remove line break with 'M'
				data_list = data.split("\nD")									#string into list
				transTag = None
				trans_inserted = 0
				trans_found = len(data_list)-1
				for dl in data_list[1:]:										#skip 1st line as this is not a transaction
					col = dl.split(';')											#each list item into columns
					datetimeobject = datetime.strptime(col[0],'%d/%m/%Y')		#change transaction date format
					transDate = datetimeobject.strftime('%Y-%m-%d')
					transAmnt = col[1]
					transDesc = col[2].replace("\n","")
					if desc_dict:												#if description exist
						for key, value in desc_dict.items(): 					#search for a matching string
							if key in transDesc:
								transDesc = transDesc.replace(key,value)
								break
							else:
								transDesc = transDesc
					if cond_dict:												#if conditions exist
						for key, value in cond_dict.items(): 					#search for a matching string
							if key in transDesc:
								transTag = value
								break
							else:
								transTag = None
					Transaction.create_one(transDate, transAmnt, transDesc, transTag, accountid, card, False)
					trans_inserted +=1
				
				if trans_inserted==trans_found:
					flash_msg = 'Statement uploaded, Found: ' + str(trans_found)
					flash_color = 'success'
				else:
					flash_msg = 'Found: ' + str(trans_found) + ', Saved: ' + str(trans_inserted)
					flash_color = 'danger'

			flash(flash_msg,flash_color)
			return redirect(url_for('listNew', accountid=accountid))
	elif request.method=='POST' and request.form['btnSubmit']=='applyFilter':
		session['selected_year'] = request.form['selectedYear']
		return redirect(url_for('overview', accountid=accountid))
	else:
		latest_list = Transaction.list_latest_uploads_by_card(accountid,'C') + Transaction.list_latest_uploads_by_card(accountid,'D')
		selected_year = session['selected_year'] if session.get('selected_year') != None else Transaction.max_year(accountid)
		chart_hight = Taggroup.list_count(accountid) * 28 if (Taggroup.list_count(accountid) * 28)>140 else 140
		templateData = {
			'accountid' : accountid,
			'title' : 'Account Summary',
			'acc_name' : Account.query.filter_by(id = accountid).first(),
			'cnt_new' : Transaction.cnt_new(accountid),
			'cnt_all' : Transaction.cnt_all(accountid),
			'latest' : latest_list,
			'years' : Transaction.list_year(accountid),
			'selected_year' : selected_year,
			'chart_months' : [app.config['CHART_1_MONTH_COUNT'],app.config['CHART_2_MONTH_COUNT'],app.config['CHART_3_MONTH_COUNT']],
			'chart1' : Transaction.chart_header('chart1', accountid),
			'chart2' : Transaction.chart_header('chart2', accountid),
			'chart3' : Transaction.chart_header('chart3', accountid),
			'chart_count' : [Transaction.chart_header('chart1', accountid).count(),Transaction.chart_header('chart2', accountid).count(),Transaction.chart_header('chart3', accountid).count()],
			'chart1_data' : Transaction.chart_data(accountid, 'chart1', app.config['CHART_1_MONTH_COUNT']),
			'chart2_data' : Transaction.chart_data(accountid, 'chart2', app.config['CHART_2_MONTH_COUNT']),
			'chart3_data' : Transaction.chart_data(accountid, 'chart3', app.config['CHART_3_MONTH_COUNT']),
			'chart_in_out' : Transaction.chart_in_out(accountid),
			'chart_monthly_trend' : Transaction.chart_monthly_trend(accountid),
			'chart_avg_month_height' : chart_hight,
			'chart_avg_month' : Transaction.get_stat_year(accountid, selected_year)
		}
		return render_template('/overview.html', **templateData)

##----------------------------------------------------------------------------------------------------Summary Table
@app.route("/summary/<accountid>/<table>/<what_year>", methods=['GET'])
def summary(accountid,table,what_year):
	if table=='1':
		df = Transaction.get_stat_year_df(accountid, what_year)
		t_d = Transaction.get_statsDate(what_year)
		dict_data = df.to_dict('index')
		return_str = '<table class="table table-sm table-striped"><tr style="text-align: right">\
						<th style="text-align: left">Category</th><th>Total</th><th>Prev Year</th><th>YTD</th><th>%YTD</th><th>Avg Month</th><th>Prev Month</th></tr>'
		s_d = []
		for key in dict_data:
			return_str = return_str + '<tr>'
			for subkey in dict_data[key]:
				s_d.append(dict_data[key][subkey])
				if len(s_d)==8:
					return_str = return_str + '<td style="text-align: left">' + s_d[0] + '</td>'
					return_str = return_str + '<td style="text-align: right"><a href="/prefilter/'+ str(accountid) +'?taggroup='+ str(int(s_d[1])) + '">' + str(s_d[2]) + '</a></td>'
					return_str = return_str + '<td style="text-align: right"><a href="/prefilter/'+ str(accountid) +'?taggroup='+ str(int(s_d[1])) + '&datefrom='+ t_d[0] +'&dateto='+ t_d[1] +'">' + str(s_d[3]) + '</a></td>'
					return_str = return_str + '<td style="text-align: right"><a href="/prefilter/'+ str(accountid) +'?taggroup='+ str(int(s_d[1])) + '&datefrom='+ t_d[2] +'&dateto='+ t_d[3] +'">' + str(s_d[4]) + '</a></td>'
					return_str = return_str + '<td style="text-align: right">' + str(s_d[5]) + '</td>'
					return_str = return_str + '<td style="text-align: right">' + str(s_d[6]) + '</td>'
					return_str = return_str + '<td style="text-align: right"><a href="/prefilter/'+ str(accountid) +'?taggroup='+ str(int(s_d[1])) + '&datefrom='+ t_d[4] +'&dateto='+ t_d[5] +'">' + str(s_d[7]) + '</a></td>'
			s_d = []
		return_str = return_str + '</tr></table>'
		return jsonify(return_str)

	elif table=='2':
		df = Transaction.get_stat_year_by_year(accountid)
		dict_data = [df.to_dict(), df.to_dict('index')]
		return_str = '<table class="table table-sm table-striped"><tr><th>Category</th>'
		keys_to_year = []
		for key in dict_data[0].keys():
			return_str = return_str + '<th style="text-align: right">' + str(key) + '</th>'
			keys_to_year.append(key)
		return_str = return_str + '</tr>'

		for key in dict_data[1].keys():
			col = str(key[0]) if type(key)==tuple else str(key)
			tag = str(key[1]) if type(key)==tuple else ''
			return_str = return_str + '<tr><td>' + col + '</td>'
			dict_i = -1
			for subkey in dict_data[1][key]:
				dict_i += 1
				date_from = '&datefrom='+ str(keys_to_year[dict_i]) +'-01-01' if dict_i > 0 else ''
				date_to   = '&dateto='+   str(keys_to_year[dict_i]) +'-12-31' if dict_i > 0 else ''
				return_str = return_str + '<td style="text-align: right"><a href="/prefilter/'+ str(accountid) +'?taggroup='+ tag + date_from + date_to +'">' + str(dict_data[1][key][subkey]) + '</a></td>'
		return_str = return_str + '</tr></table>'
		return jsonify(return_str)

	else:
		return jsonify('Hello, World!')

##----------------------------------------------------------------------------------------------------All Transactions Page
@app.route("/listAll/<accountid>", methods=['GET','POST'])
def listAll(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateTrans':
		t_id = request.form['trans_ID']
		t_date = request.form['trans_date']
		t_desc = request.form['trans_desc']
		t_amount = request.form['trans_amnt']
		t_tag = request.form['trans_tag']
		Transaction.update_trans(t_id, t_date, t_amount, t_desc, t_tag)
		flash('Transaction updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='insertTrans':
		t_id = request.form['trans_ID']
		t_date = request.form['trans_date']
		t_desc = request.form['trans_desc']
		t_amount = request.form['trans_amnt']
		t_amountprev = request.form.get('prevAmount')
		t_tag = request.form['trans_tag']
		t_adjust = request.form.get('adjust') != None
		Transaction.create_one(t_date, t_amount, t_desc, t_tag, accountid, 'M', 1)
		if t_adjust==True:
			Transaction.update_trans_amount(t_id, t_amountprev)
		flash('New transaction created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createCondition':
		t_desc = request.form['trans_desc']
		t_tag = request.form['trans_tag']
		Condition.insert_cond(t_desc,t_tag,accountid)
		flash('New condition created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteTrans':
		t_id = request.form['trans_ID']
		Transaction.delete_trans(t_id)
		flash('Transaction deleted.','warning')

	page = request.args.get('page', 1, type=int)
	f_from = session['filter_from'] if session.get('filter_from') != None else Transaction.first_date(accountid)
	f_to = session['filter_to'] if session.get('filter_to') != None else Transaction.last_date(accountid)
	f_tag = session['filter_tag'] if session.get('filter_tag') != None else Tag.list_tag_id(accountid)
	trns = Transaction.list_filtered(accountid, f_from, f_to, f_tag).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev = url_for('listAll', accountid=accountid, page=trns.prev_num) if trns.has_prev else None
	has_next = url_for('listAll', accountid=accountid, page=trns.next_num) if trns.has_next else None
	templateData = {
		'accountid' : accountid,
		'title' : 'All Transactions',
		'url_for_name' : 'listAll',
		'acc_name' : Account.one_acc(accountid),
		'tags' : Tag.list_tag(accountid),
		'cnt_avg_sum' : Transaction.cnt_avg_sum_filtered(accountid, f_from, f_to, f_tag),
		'filter_from' : f_from,
		'filter_to' : f_to,
		'filter_tag' : [f_tag],
		'cnt_new' : Transaction.cnt_new(accountid),
		'page_name' : 'listAll'
	}
	return render_template('/list.html', pagination=trns, has_prev=has_prev, has_next=has_next, **templateData)

##----------------------------------------------------------------------------------------------------New Transactions Page
@app.route("/listNew/<accountid>", methods=['GET','POST'])
def listNew(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateTrans':
		t_id = request.form['trans_ID']
		t_date = request.form['trans_date']
		t_desc = request.form['trans_desc']
		t_amount = request.form['trans_amnt']
		t_tag = request.form['trans_tag']
		Transaction.update_trans(t_id, t_date, t_amount, t_desc, t_tag)
		flash('Transaction updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='insertTrans':
		t_id = request.form['trans_ID']
		t_date = request.form['trans_date']
		t_desc = request.form['trans_desc']
		t_amount = request.form['trans_amnt']
		t_amountprev = request.form.get('prevAmount')
		t_tag = request.form['trans_tag']
		t_adjust = request.form.get('adjust') != None
		Transaction.create_one(t_date, t_amount, t_desc, t_tag, accountid, 'M', 1)
		if t_adjust==True:
			Transaction.update_trans_amount(t_id, t_amountprev)
		flash('New transaction created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createCondition':
		t_desc = request.form['trans_desc']
		t_tag = request.form['trans_tag']
		Condition.insert_cond(t_desc,t_tag,accountid)
		flash('New condition created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteTrans':
		t_id = request.form['trans_ID']
		Transaction.delete_trans(t_id)
		flash('Transaction deleted.','warning')
	
	page = request.args.get('page', 1, type=int)
	f_from = session['filter_from'] if session.get('filter_from') != None else Transaction.first_date(accountid)
	f_to = session['filter_to'] if session.get('filter_to') != None else Transaction.last_date(accountid)
	f_tag = session['filter_tag'] if session.get('filter_tag') != None else Tag.list_tag_id(accountid)
	trns = Transaction.list_filtered_new(accountid, f_from, f_to).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev = url_for('listNew', accountid=accountid, page=trns.prev_num) if trns.has_prev else None
	has_next = url_for('listNew', accountid=accountid, page=trns.next_num) if trns.has_next else None
	cnt_new = Transaction.cnt_new(accountid)
	templateData = {
		'accountid' : accountid,
		'title' : 'New Transactions',
		'url_for_name' : 'listNew',
		'acc_name' : Account.one_acc(accountid),
		'tags' : Tag.list_tag(accountid),
		'cnt_avg_sum' : Transaction.cnt_avg_sum_filtered_new(accountid, f_from, f_to),
		'filter_from' : f_from,
		'filter_to' : f_to,
		'filter_tag' : [f_tag],
		'cnt_new' : cnt_new,
		'page_name' : 'listNew'
	}
	if cnt_new[0] == 0:
		flash('No more new transactions to edit.','warning')
		return redirect(url_for('overview', accountid=accountid))
	return render_template('/list.html', pagination=trns, has_prev=has_prev, has_next=has_next, **templateData)

##----------------------------------------------------------------------------------------------------Filter Apply
@app.route("/filter/<accountid>/<page_name>", methods=['GET','POST'])
def filter(accountid,page_name='listAll'):
	if request.method == 'POST':
		if not request.form.getlist("filter_tag[]"): #when submiting a filter, check if category is selected
			session['filter_from'] = request.form['filter_from']
			session['filter_to']   = request.form['filter_to']
			session['filter_tag']  = None
			flash('At least 1 TAG must be selected. Found NONE, selected ALL.','warning')
		else:
			session['filter_from'] = request.form['filter_from']
			session['filter_to']   = request.form['filter_to']
			session['filter_tag']  = request.form.getlist("filter_tag[]", type=int)
		return redirect(url_for(page_name, accountid=accountid))
	else: #reset filter
		session['filter_from'] = None
		session['filter_to'] = None
		session['filter_tag'] = None
		return redirect(url_for(page_name, accountid=accountid))

##----------------------------------------------------------------------------------------------------Pre-Filter Apply
@app.route("/prefilter/<accountid>")
def prefilter(accountid):
	session['filter_from'] = request.args.get('datefrom') if request.args.get('datefrom')!=None else None
	session['filter_to'] = request.args.get('dateto') if request.args.get('dateto')!=None else None
	session['filter_tag'] = Tag.list_tag_id_of_group(request.args.get('taggroup'), accountid) if request.args.get('taggroup') not in [None,'0'] else None
	return redirect(url_for('listAll', accountid=accountid))

##----------------------------------------------------------------------------------------------------Condition Page
@app.route("/condition/<accountid>", methods=['GET','POST'])
def condition(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateCond':
		c_id = request.form['cond_ID']
		c_desc = request.form['cond_desc']
		c_tag = request.form['cond_tag']
		Condition.update_cond(c_id, c_desc, c_tag)
		flash('Condition updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createCond':
		c_desc = request.form['cond_desc']
		c_tag = request.form['cond_tag']
		Condition.insert_cond(c_desc,c_tag,accountid)
		flash('New condition created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteCond':
		c_id = request.form['cond_ID']
		Condition.delete_cond(c_id)
		flash('Condition deleted.','warning')
	
	page = request.args.get('page', 1, type=int)
	conds = Condition.list_cond(accountid).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev = url_for('condition', accountid=accountid, page=conds.prev_num) if conds.has_prev else None
	has_next = url_for('condition', accountid=accountid, page=conds.next_num) if conds.has_next else None
	shw_pag = True if Condition.list_count(accountid) > app.config['POSTS_PER_PAGE'] else False
	templateData = {
		'accountid' : accountid,
		'title' : 'Tag Conditions',
		'url_for_name' : 'condition',
		'acc_name' : Account.one_acc(accountid),
		'tags' : Tag.list_tag(accountid),
		'cnt_new' : Transaction.cnt_new(accountid),
		'show_pagination' : shw_pag
	}
	return render_template('/condition.html', pagination=conds, has_prev=has_prev, has_next=has_next, **templateData)

##----------------------------------------------------------------------------------------------------Description Page
@app.route("/description/<accountid>", methods=['GET','POST'])
def description(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateDesc':
		id = request.form['ID']
		descfrom = request.form['descfrom']
		descto = request.form.get('descto')
		Description.update_desc(id, descfrom, descto)
		flash('Description updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createDesc':
		descfrom = request.form['descfrom']
		descto = request.form.get('descto')
		Description.insert_desc(descfrom, descto, accountid)
		flash('New description created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='applyDesc':
		descfrom = request.form['descfrom']
		descto = request.form.get('descto')
		Transaction.update_desc(accountid, descfrom, descto)
		flash('Matching Text Replaced.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteDesc':
		id = request.form['ID']
		Description.delete_desc(id)
		flash('Description deleted.','warning')
	
	page = request.args.get('page', 1, type=int)
	descs = Description.list_desc(accountid).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev = url_for('description', accountid=accountid, page=descs.prev_num) if descs.has_prev else None
	has_next = url_for('description', accountid=accountid, page=descs.next_num) if descs.has_next else None
	shw_pag = True if Description.list_count(accountid) > app.config['POSTS_PER_PAGE'] else False
	templateData = {
		'accountid' : accountid,
		'title' : 'Shorten Transaction Description',
		'url_for_name' : 'description',
		'acc_name' : Account.one_acc(accountid),
		'cnt_new' : Transaction.cnt_new(accountid),
		'show_pagination' : shw_pag
	}
	return render_template('/description.html', pagination=descs, has_prev=has_prev, has_next=has_next, **templateData)

##----------------------------------------------------------------------------------------------------Tag Group Page
@app.route("/taggroup/<accountid>", methods=['GET','POST'])
def taggroup(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateGroup':
		g_id = request.form['group_ID']
		g_desc = request.form['group_desc']
		g_col = request.form['color']
		Taggroup.update_tag_group(g_id, g_desc, g_col)
		flash('Group updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createGroup':
		g_desc = request.form['group_desc']
		g_col = request.form['color']
		Taggroup.insert_tag_group(g_desc, g_col, accountid)
		last_id = Taggroup.list_tgroup_id_one(accountid)
		Tag.insert_tag(g_desc, last_id, 0,True,0,0,0 )
		flash('New group created. New tag created','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteGroup':
		g_id = request.form['group_ID']
		Taggroup.delete_tag_group(g_id)
		flash('Group deleted.','warning')
	
	page = request.args.get('page', 1, type=int)
	grps = Taggroup.list_tgroup(accountid).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev = url_for('taggroup', accountid=accountid, page=grps.prev_num) if grps.has_prev else None
	has_next = url_for('taggroup', accountid=accountid, page=grps.next_num) if grps.has_next else None
	shw_pag = True if Taggroup.list_count(accountid) > app.config['POSTS_PER_PAGE'] else False
	templateData = {
		'accountid' : accountid,
		'title' : 'Tag Groups',
		'url_for_name' : 'taggroup',
		'acc_name' : Account.one_acc(accountid),
		'cnt_new' : Transaction.cnt_new(accountid),
		'show_pagination' : shw_pag
	}
	return render_template('/taggroup.html', pagination=grps, has_prev=has_prev, has_next=has_next, **templateData)

##----------------------------------------------------------------------------------------------------Tag Page
@app.route("/tag/<accountid>", methods=['GET','POST'])
def tag(accountid):
	if request.method=='POST' and request.form['btnSubmit']=='updateTag':
		t_id = request.form['tag_ID']
		t_desc = request.form['tag_desc']
		t_group = request.form['tag_group']
		t_bal = request.form.get('isBlnc') != None
		t_sum = request.form.get('inSum') != None
		t_c1 = request.form.get('chart1') != None
		t_c2 = request.form.get('chart2') != None
		t_c3 = request.form.get('chart3') != None
		Tag.update_tag(t_id, t_desc, t_group, t_bal, t_sum, t_c1, t_c2, t_c3)
		flash('Tag updated.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='createTag':
		t_desc = request.form['tag_desc']
		t_group = request.form['tag_group']
		t_bal = request.form.get('isBlnc') != None
		t_sum = request.form.get('inSum') != None
		t_c1 = request.form.get('chart1') != None
		t_c2 = request.form.get('chart2') != None
		t_c3 = request.form.get('chart3') != None
		Tag.insert_tag(t_desc, t_group, t_bal, t_sum, t_c1, t_c2, t_c3)
		flash('New tag created.','success')
	elif request.method=='POST' and request.form['btnSubmit']=='deleteTag':
		t_id = request.form['tag_ID']
		Tag.delete_tag(t_id)
		flash('Tag deleted.','warning')
	
	page = request.args.get('page', 1, type=int)
	tags = Tag.list_tag(accountid).paginate(page, app.config['POSTS_PER_PAGE'], False)
	has_prev= url_for('tag', accountid=accountid, page=tags.prev_num) if tags.has_prev else None
	has_next = url_for('tag', accountid=accountid, page=tags.next_num) if tags.has_next else None
	shw_pag = True if Tag.list_count(accountid) > app.config['POSTS_PER_PAGE'] else False
	templateData = {
		'accountid' : accountid,
		'title' : 'Tags',
		'url_for_name' : 'tag',
		'acc_name' : Account.one_acc(accountid),
		'groups' : Taggroup.list_tgroup(accountid),
		'cnt_new' : Transaction.cnt_new(accountid),
		'show_pagination' : shw_pag
	}
	return render_template('/tag.html', pagination=tags, has_prev=has_prev, has_next=has_next, **templateData)

################################################################################ ADMIN
""" only enabled on raspberry
@app.route("/PowerOFF")
def PowerOFF():
	print('Called the SHUT-DOWN script')
	print('Good Bye!')
	os.system("sudo shutdown -h now")

@app.route("/Reboot")
def Reboot():
	print('Called the REBOOT script')
	print('See you soon!')
	os.system("sudo reboot now")
"""

