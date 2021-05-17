# Budget-Monitor
A monthly budget monitor. Upload statement file, group by categories &amp; analyse your spending trends.

## What is it?
Python + Flask + SQLite (or PostgreSQL) web app. Upload a statement in QIF format. Data is saved in your local database. Create transaction tags, then monitor your spending habits month after month.

## Why QIF not CSV?
All banks I have expierienced with, produce the QIF file in exact same format, where CSV have different formatting.
This makes it easier to load a statement from multiple banks, in the same format.
ie:
In QIF file all transacitons amount coming out, are represented as negative (with preceding minus "-"). This is true across accounts (debit / credit).
In CSV depending on bank and account (credit/debit), the transation amount is represented differently, hence the *.qif preference over any other.
QIF format/layout is the same from bank to bank, CVS varies.

![alt text](https://github.com/michalchrzastek/Budget-Monitor/blob/master/img/microsoft_money_QIF.png)


## Why?
There is a number of budget monitor like apps, but appart of some requiring to register or to share personal and bank details, I just wanted to build my own :)

## Plans for the future:
Dependency on Bootstrap 4.5. Once version 5 is released, will update this app. This also links with removal of jQuery and elimination of FontAwesome in favour of default Bootstrap icons. Also dependency on Tempus-Dominus, (date picker) and BSMultiSelect (tag filter). All mentioned are used in the app via cdn.

## Installation instructions (for Mac):
Prerequisite: Python3.6 (minimum), check your version: python3 --version

1. Install Virtual Environment for Python3, might require sudo
```
pip3 install virtualenv
```
2. Download this repo
```
git clone https://github.com/michalchrzastek/Budget-Monitor
```
3. Go in and activate virtual environment
```
cd Budget-Monitor
python3 -m venv bm
. bm/bin/activate
```
> Notice **(bm)** at the start of each line in terminal, which indicates that you are working inside the virtual environment.

4. Install Flask within the (bm) venv
```
pip3 install Flask
pip3 install Flask-SQLAlchemy
```
5. Install Pandas within the (bm) venv
```
pip3 install pandas
```
6. [optional] Edit config.py, update location and upload folder paths
```
nano config.py
```
Change path to database and statement location
```
SQLALCHEMY_DATABASE_URI
UPLOAD_FOLDER
```
Then **CTRL + X**, to close and **Y** to confirm changes, then hit **ENTER**

7. Specify application discovery 
```
export FLASK_APP=main.py
```
8. Start the Flask app with this command:
```
flask run
```
9. Open a web browser and enter:
```
localhost:5000
```
10. PLAY :)


To Close the app and VENV
```
CTRL + C
deactivate
```
