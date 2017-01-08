# RaspberryPi-433MHz-Remote-Switches-Web-Controller
This project provides a web api, written in python, to control cheap Remote Control Switches based on 433 MHz via a Raspberry Pi. It also provides a web interface for a handy use of the API. All you need is a 433 MHz RF transmitter for a few bucks.

Features:
* Trigger rc switches to turn on and off via GET requests
* Store ('bookmark'), remove and list your devices with name and state via POST requests
* Simple web interface to control and manage your remote control switches

Planned features:
* Scheduler for time and event based tasks
* Improve security
* Code documentation (yeah, sorry ...)

**Feel free to ask, report bugs and improve!**

## What it is

I searched for an easy to use web api to control 433MHz Remote Control Switches, like the ones from Elro, via my Raspberry Pi. Previously I used [PowerPi](http://raspberrypiguide.de/howtos/powerpi-raspberry-pi-haussteuerung/) (sorry, it's German), but I'm more the Python guy and wanted a more flexible communication.

So this project provides a simple web API with a few endpoints to control and bookmark 433MHz RC Switches via HTTP. To turn a Switch on, you can do an HTTP-Get to `http://<ip-of-your-pi>/11011A/on`,  where `11011` is your house code and *A* is the identifier of the switch.
To get it a bit more comfortable the project also includes a small web interface to turn the switches on and off.

## Install

### Software

```bash
# install needed dependencies
sudo apt-get install git python3 python3-pip python-rpi.gpio
sudo pip install flask 

# clone this repo
git clone https://github.com/philipptrenz/RaspberryPi-433MHz-Remote-Switches-Web-Controller
cd RaspberryPi-433MHz-Remote-Switches-Web-Controller

# and start
sudo python3 433PyApi.py
```

If you want to run the script as a service on every boot:
```bash
# make the scripts executable
sudo chmod 755 433PyApi.py
sudo chmod 755 433PyApi.sh

# add the bash script to the service folder
sudo cp 433PyApi.sh /etc/init.d
sudo update-rc.d 433PyApi.sh defaults

```
Now you can start and stop your script via `sudo service 433PyApi start` or `stop` and it automatically starts on boot.

### Hardware

I used [this](http://www.watterott.com/de/RF-Link-Sender-434MHz) transmitter, but also other ones should work. Connect the transmitter to the Pi like in the illustration below:

```
	_____________
	|	 ___	|
	|  /   	 \	|
	| |		  |	|
	|  \ ___ /	|
	|___________|
	|	|	|	|
	|	|	|	|

	|	|	|	|_ antenna - 17cm cable
	|	|	|_ 5V - pin 4
	|	|_ data - gpio 17
	|_ ground - pin 6
```


## Get started

### For an easy use

When you just want to control your switches, install the project and navigate in a browser to the ip address of your Raspberry Pi. You will see an quite empty webpage
* Click on the gear at the top right. Now you can bookmark your switches
* First of all type in the house code of your remote controlled switches
* Followed by the letter of the specific switch
* Now choose a name for this switch
* Click the green button

![screenshot 1](/screenshots/mobile_3.png?raw=true)
![screenshot 2](/screenshots/desktop_1.png?raw=true)
![screenshot 3](/screenshots/mobile_2.png?raw=true)
![screenshot 4](/screenshots/desktop_2.png?raw=true)

The switch should now appear above. Now switch back to the first page and you see your switch ready to work.

### Extended

Besides the web interface you can speak directly to the Web API. For turning switches on and off use a simple GET request like:

```bash
curl http://<ip-of-your-pi>/11011A/on
curl http://<ip-of-your-pi>/11011A/off
```

Additionally you can use POST requests to bookmark, update, remove and list switches:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test","name":"My First Switch", "state":"off"}' http://<ip-of-your-pi/11011A/add
```
Repeat this for all of your Switches. You can use this endpoint also to update data. The `state` is optional and can be `on` and `off`.

You can also remove bookmarked switches:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test"}' http://<ip-of-your-pi/11011A/remove
```
And let's get a list of all bookmarks:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test"}' http://<ip-of-your-pi/list
```

### Overview of all endpoints

```
GET: 	/<house code + letter>/on
GET:	/<house code + letter>/off

POST: 	/<house code + letter>/add
POST: 	/<house code + letter>/remove
POST:	/list
```
The POST requests need a secret sent via JSON, by default it is `test` (see above in curls)
