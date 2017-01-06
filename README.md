# RaspberryPi-433MHz-Remote-Switches-Web-Controller
This project provides a web api, written in python, to control cheap Remote Control Switches based on 433 MHz via a Raspberry Pi. It also provides a web interface for a handy use of the API. All you need is a 433 MHz RF transmitter for a few bucks. Have fun!

**NOTICE: Still in development, many features are still missing!**

## What it is

I searched for an easy to use web api to control 433MHz Remote Control Switches, like the ones from Elro, via my Raspberry Pi. Previously I used [PowerPi](http://raspberrypiguide.de/howtos/powerpi-raspberry-pi-haussteuerung/) (sorry, it's German), but I'm more the Python guy and wanted a more flexible communication.

So this project provides a simple web API with a few endpoints to control and bookmark 433MHz RC Switches via HTTP. To turn a Switch on, you can do an HTTP-Get to `http://<ip-of-your-pi>/11011A/on`,  where `11011` is your house code and *A* is the identifier of the switch.
To get it a bit more comfortable the project also includes a small web interface to turn the switches on and off.

## Install

```bash
# install needed dependencies
sudo apt-get install git python3 python3-pip python-rpi.gpio
sudo pip install flask 

# clone this repo
git clone https://github.com/philipptrenz/RaspberryPi-433MHz-Remote-Switches-Web-Controller
cd RaspberryPi-433MHz-Remote-Switches-Web-Controller

# and start
python3 433PyApi.py
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


## Get started

### For an easy use

As shortly explained above, you can directly control your switches via the browser, just type into the address bar `http://<ip-of-your-pi>/11011A/on` or `http://<ip-of-your-pi>/11011A/off` while the code, here `11011`, has to match the house code (first five dip switches on your Remote Control Switches), in general: up is 1, down is 0, from left to right). The following letter is the numbering of the switches. 

### Extended

To use the web interface, first bookmark some of your switches. While this functionality is not yet provided by the web interface and we use HTTP-POST for this, here are examples with curl:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test","name":"My First Switch"}' http://<ip-of-your-pi/11011A/add
```

Repeat this for all of your Switches. You can also remove bookmarked switches:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test"}' http://<ip-of-your-pi/11011A/remove
```
And let's get a list of all bookmarks:

```bash
curl -H "Content-Type: application/json" -X POST -d '{"secret":"test"}' http://<ip-of-your-pi/list
```

### Overview over all endpoints

```
GET: 	/<house code + letter>/on
GET:	/<house code + letter>/off

POST: 	/<house code + letter>/add
POST: 	/<house code + letter>/remove
POST:	/list
```
The POST requests need a secret sent via JSON, by default it is `test` (see above)
