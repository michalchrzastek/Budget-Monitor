# Budget-Monitor
A monthly budget monitor. Upload statement file, group by categories &amp; analyse your spending trends.

## What is it?
Python + Flask + PostgreSQL web app. Upload a statement in QIF format. Data is saved in your local database. Create transaction tags, then monitor your spending habits month after month.

## Why QIF not CSV?
All banks I have expierienced with, produce the QIF file in exact same format, where CSV have different formatting.
This makes it easier to convert and upload the file with python to DB.
![alt text](https://github.com/michalchrzastek/Budget-Monitor/blob/master/img/microsoft_money_QIF.png)


## Why?
There is a number of budget monitor like apps, but they all require to share personal and bank details. I didn't want to do it. This is why I created this web app, to have full control of the data and the layout.

## Instalation instructions:
Installed on a Raspberry Pi, connected to home network. This way I can access the web app from any laptop / mobile.
Feel free not to follow this :)

1. Clean installation or Raspbian on a SD card
2. Added a blank file named **ssh** to the SD, so I can connect to the Pi remotely.
3. Connect to Pi from terminal: ssh pi@xxx.xxx.xxx.xxx, run: (this will take few mins)
```
sudo apg-get update && apg-get upgrade -y
```
4. **Optional** In the future you can use **RaspberryPi** in your browser instead of the IP. However if you have few Pi's running it's best to rename it, otherwise you will have a conflict.
```
sudo nano /etc/hostname
```
You can replace it to something shorter like: **home**, close+save then:
```
sudo nano /etc/hosts
```
Again, replace **raspberrypi** to **home**, close+save
    
5. Once all done, restart the Pi:
```
sudo shutdown -r now
```
6. Connect to the Pi again
```
ssh pi@home.local
```
7. Install Virtual Environment for Python3
```
sudo apt-get install python-virtualenv
```
8. You still should be in the home directory, create a new folder, venv and activate it
```
mkdir budget-monitor
cd budget-monitor/
python3 -m venv venv
. venv/bin/activate
```
> Notice **(venv)** at the start of each line in terminal, which indicates that you are working inside the virtual environment.

9. Install Flask
```
pip3 install Flask
```
10. Create a new folder for the web app files
```
mkdir bm_app
cd bm_app/
nano app.py
```
11. In the **app.py** file paste this, then close and save
```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```
12. Start the Flask app with this command:
```
flask run --host=0.0.0.0
```
13. Open a web browser on your laptop/PC and enter the IP address of the Pi or the new name **home** followed by port 5000 ie:
```
home.local:5000
```
14. You should see a web page with **Hello, World**. If this is not the case you can refer to offical [Flask Guide](https://flask.palletsprojects.com/en/1.1.x/quickstart/).
15. Close VENV
```
deactivate
```
16. Install PostgreSQL database to store the bank transactions
```
sudo apt-get install postgresql postgresql-client
```
17. Then create a new user
 ```
sudo -u postgres bash
CREATE USER bm_appuser WITH ENCRYPTED PASSWORD ‘bm_appuser01’;
ALTER ROLE bm_appuser WITH SUPERUSER;
```
18. Create database for our app
```
CREATE DATABASE budgetmonitor WITH ENCODING 'UTF-8';
\q
```
19. Enable remote access to DB
```
nano /etc/postgresql/11/main/postresql.conf
```
> Then change this line:
```
#listen_addresses = ‘localhost’
```
> To:
```
listen_addresses = ‘*’
```
> Make a note of what port is configured ie: 5432
> Then edit this config file:
```
nano /etc/postgresql/11/main/pg_hba.conf
```
> Find line 
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
```
> Replace the IP, to **0.0.0.0/0**

20. Restart the PostgreSQL service
```
/etc/init.d/postgresql restart
```
> Then type in `exit` so you are no longer root
> For any help with troubleshooting follow the [PostgreSQL Guide](https://www.stuartellis.name/articles/postgresql-setup/)
