# Budget-Monitor
A monthly budget monitor. Upload statement file, group by categories &amp; analyse your spending trends.

## What is it?
Python + Flask + SQLite web app. Upload a statement in QIF format. Data is saved in your local database. Create transaction tags, then monitor your spending habits month after month. Combine statements from credit &amp; debit cards, even from different banks, to create one clear picture of your personal cash flow. Is your credit card statement generated mid-month? No more, now you can see each month from 1st to last day.

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
- Maintain...

July 2024 update
- Upgraded Bootstrap to 5.3.3
- Upgraded Bootstrap Icons to 1.11.3
- Upgraded ChartsJS to 4.4.3
- Upgraded requirements.txt packanges to latest versions
- Automated MPG calculation for fuel chart
- Added 2 new optional filters for transaction view, [text] & [card] type
- Added card type column to transaction view
- Changed JS getAjax function from fixed host to auto detect 'IP' or 'localhost'

May 2023 update:
- Upgraded Bootstrap to 5.2.3
- Upgraded ChartsJS to 3.9.1
- Upgraded to pandas 2.0.1
- Date Picker works again with TempusDominus 6.7.7
- Redesigned how the overview page works/looks
- Added new fuel chart

January 2022 update:
- Upgraded Bootstrap from 4.5 to 5.1
- Replaced FontAwesome for Bootstrap Icons
- Upgraded ChartsJS from 2.* to 3.7
- Removed jQuery
- Removed BSMultiSelect
- Added option to set the interface with a different language
- Date picker (TempusDominus) temporary disabled, until v6 is completed

## Installation instructions (for Mac):
Prerequisite: Python3.8 (minimum), check your version: python3 --version

1. Open Terminal, navigate to desired location, ie [Downloads] or [Documents]

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

## Upgrade instructions (for Mac):
1. Go to the folder where you installed the repo
2. Copy the budgetmonitor.db file to a safe place.
3. Delete the Budget-Monitor folder
4. Follow the installation instructions
5. After initial launch, close the app/terminal and replace the new budgetmonitor.db file with your backup copy fom step 2.
6. Start the app same way as usual.