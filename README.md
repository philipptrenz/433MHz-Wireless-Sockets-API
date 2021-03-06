# 433MHz Wireless Sockets API
This project provides a RESTlike web API, written in Python, to control cheap remote control sockets based on 433 MHz via a Raspberry Pi. It also provides a web interface for a handy use of the API. All you need is a 433 MHz RF transmitter for a few bucks, a Pi and some minutes to get it running.

## What it is

I searched for an easy to use web API to control 433MHz wireless sockets, like the ones from Elro or Mumbi via WLAN. Previously I used [PowerPi](http://raspberrypiguide.de/howtos/powerpi-raspberry-pi-haussteuerung/) (German, sorry), but I'm more the Python guy and wanted a flexible communication to build my own apps and extensions.

So this project provides a simple API with a few endpoints to control and bookmark 433MHz wireless sockets via HTTP. To get it a bit more comfortable the project also includes a web interface to turn the sockets on and off. And of course it's responsive ;)

![screenshot 1](/screenshots/screen_1.png?raw=true)

Features:
* Trigger wireless sockets to turn on and off via GET requests
* Store ('bookmark'), remove and list your devices with name and state via POST requests
* Simple web interface to control and manage your remote control sockets
* [MacOS Status Bar App](https://github.com/philipptrenz/433MHz-Wireless-Sockets-MacOS-App)

Planned features (in this order):
* Scheduler for time and event based tasks
* Improve security
* Code documentation (yeah, sorry ...)

**Feel free to ask, report bugs and improve!**

## Install

### Software

```bash
# install needed dependencies
sudo apt-get install git python3 python3-pip
sudo pip3 install flask tinydb RPi.GPIO

# clone this repo
git clone https://github.com/philipptrenz/433MHz-Wireless-Sockets-API
cd 433MHz-Wireless-Sockets-API

# and start
sudo python3 433PyApi.py
```

If you want to run the script as a service on every boot:
```bash
# make the scripts executable
sudo chmod 755 433PyApi.py

# add the bash script to the service folder
sudo cp 433PyApi.sh /etc/init.d/433PyApi
sudo chmod 755 /etc/init.d/433PyApi
sudo update-rc.d 433PyApi defaults

```
Now you can start and stop your script via `sudo service 433PyApi start` or `stop` and it automatically starts on boot.

### Hardware

I used [this](http://www.watterott.com/de/RF-Link-Sender-434MHz) transmitter, but also others should work. Connect the transmitter to the Pi like this:

```
	 ___________
	|    ___    |
	|  /   	 \  |
	| |	  | |
	|  \ ___ /  |
	|___________|
	|   |	|   |
	|   |	|   |
	|   |	|   |_ antenna - 17cm cable
	|   |	|_ 5V - pin 4
	|   |_ data - gpio 17
	|_ ground - pin 6
```


## Get started

### For an easy use

When you just want to control your sockets, install the project and navigate in a browser to the ip address of your Raspberry Pi. You will see an quite empty webpage
* Click on the gear at the top right. Now you can bookmark your sockets
* First of all type in the house code of your remote controlled sockets
* Followed by the letter of the specific socket
* Now choose a name for this socket
* Click the green button

The socket should now appear above. Now switch back to the first page and you see your socket ready to work.

![screenshot 2](/screenshots/screen_2.png?raw=true)

### Extended

Besides the web interface you can speak directly to the Web API. For turning sockets on and off use a simple GET request like:

```bash
curl http://<ip-of-your-pi>/11011A/on
curl http://<ip-of-your-pi>/11011A/off
```

Additionally you can use POST requests to bookmark, update, remove and list sockets:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test","name":"My First Socket", "state":"off"}' http://<ip-of-your-pi/11011A/add
```
Repeat this for all of your sockets. You can use this endpoint also to update data. The `state` is optional and can be `on` and `off`.

You can also remove bookmarked sockets:
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
