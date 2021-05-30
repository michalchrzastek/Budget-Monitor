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

1. Open Terminal, navigate to desired location, ie [Dowlnoads] or [Documents]

2. Download this repo
```
git clone https://github.com/michalchrzastek/Budget-Monitor
```
3. Go in and use the installer script
```
cd Budget-Monitor
./installer.sh
```
4. Open a web browser and enter:
```
localhost:5000
```


> NOTES
If you close the Terminal, this will terminate the virtual environment session. To start the application next time use the start.sh script
```
cd Budget-Monitor
./start.sh
```
Then open a web browser
```
localhost:5000
```
