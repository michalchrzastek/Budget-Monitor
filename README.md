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
```sudo apg-get update && apg-get upgrade -y```
4. Once all done, restart the Pi:
```sudo shutdown -r now```
5. Install Virtal Environment for Python3
```sudo apt-get install python-virtualenv```
6. You still should be in the home directory, create a new folder, venv and activate it
```
mkdir budget-monitor
cd budget-monitor/
python3 -m venv venv
. venv/bin/activate
```
7. Install Flask
```pip3 install Flask```
8. Create a new folder for the web app files
```
mkdir bm_app
cd bm_app/
nano app.py
```
9. In the app.py file paste this, then close and save
```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```
10. Then start the app with this command:
```flask run --host=0.0.0.0```
11. Open a web browser on your laptop/PC and enter the IP address of the Pi followed by port 5000 ie:
```192.168.0.18:5000```
12. You should see a website with "Hello, World". If this is not the case you can refer to offical [Flask Guide](https://flask.palletsprojects.com/en/1.1.x/quickstart/).
13. In the future you can use **raspberryPi** in your browser instead of IP, but i fyou have few of them running it's best to rename it, otherwise skip this step. Close the virtual env for now. We will change Pi network name so in the future don't have to remember or check the IP. Continue in the terminal while still connected remotely, type in:
```sudo nano /etc/hostname```
You can replace it to something shorter like: **home**, then:
```sudo nano /etc/hosts```
Again, replace raspberrypi to **home**, close+save, then reboot.

