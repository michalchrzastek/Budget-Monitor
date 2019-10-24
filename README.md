# Budget-Monitor
A monthly budget monitor. Upload statement file, group by categories &amp; analyse your spending trends.

# What is it?
Python + Flask + PostgreSQL web app. Upload a statement in QIF format. Data is saved in your local database. Create transaction tags, then monitor your spending habits month after month.

# Why QIF not CSV?
All banks I have expierienced with, produce the QIF file in exact same format, where CSV have different formatting.
This makes it easier to convert and upload the file with python to DB.
[[https://github.com/michalchrzastek/Budget-Monitor/blob/master/img/microsoft_money_QIF.png|alt=QIF]]


# Why?
There is a number of budget monitor like apps, but they all require to share personal and bank details. I didn't want to do it. This is why I created this web app, to have full control of the data and the layout.
