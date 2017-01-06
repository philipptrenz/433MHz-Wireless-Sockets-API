#!/usr/bin/python3
"""

"""
import flask
from flask import Flask, render_template, request, json, jsonify
import RPi.GPIO as GPIO
import time, atexit, re
from tinydb import TinyDB, Query
from tinydb.operations import delete

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

###############################################

@app.route('/<device_id>/on', methods=['GET', 'POST'])
def switchOn(device_id):
	device_id = device_id[0:7]
	if device_regex.match(device_id):
		print('turned ', device_id, ' on')
		remoteSwitch.switchOn(device_id)
		db.switch_state(device_id, 'on')
		return 'switched on'
	else:
		print('device id not matching regex')
		flask.abort(400)

@app.route('/<device_id>/off', methods=['GET', 'POST'])
def switchOff(device_id):
	device_id = device_id[0:7]
	if device_regex.match(device_id):
		print('turned ', device_id, ' off')
		remoteSwitch.switchOff(device_id)
		db.switch_state(device_id, 'off')
		return 'switched off'
	else:
		print('device id not matching regex')
		flask.abort(400)

###############################################

@app.route('/<device_id>/add', methods=['POST'])
def add(device_id):
	device_id = device_id[0:7]
	if not device_regex.match(device_id):
		print('device id not matching regex')
		flask.abort(400)
	if is_authorized(request):
		if request.headers['Content-Type'] == 'application/json':
			content = request.json
			if 'name' not in content: flask.abort(400)
			name = content['name']
			if 'state' in content:
				state = content['state']
				if state == 'on' or state == 'off':
					return db.add(device_id, name, state)
				else:
					flask.abort(400)
			else:
				return db.add(device_id, name)
		else:
			flask.abort(400)

@app.route('/<device_id>/remove', methods=['POST'])
def remove(device_id):
	device_id = device_id[0:7]
	if not device_regex.match(device_id):
		print('device id not matching regex')
		flask.abort(400)
	if is_authorized(request):
		return db.remove(device_id)

@app.route('/list', methods=['POST'])
def list():
	if is_authorized(request):
		devices_list = db.list()
		return jsonify(devices_list)

#######################################################################

class RemoteSwitch(object):
	repeat = 10 # Number of transmissions
	pulselength = 300 # microseconds
	GPIOMode = GPIO.BCM
	
	def __init__(self, pin):
		self.pin = pin
		''' 
		devices: A = 1, B = 2, C = 4, D = 8, E = 16  
		key: according to dipswitches on your Elro receivers
		pin: according to Broadcom pin naming
		'''		
		self.device_letter = { "A":1, "B":2, "C":4, "D":8, "E":16, "F":32, "G":64 } 

		GPIO.setmode(self.GPIOMode)
		GPIO.setup(self.pin, GPIO.OUT)
		
	def switchOn(self, device_id):
		key = [int(device_id[0]),int(device_id[1]),int(device_id[2]),int(device_id[3]),int(device_id[4])]
		device = self.device_letter[device_id[5]]
		self._switch(GPIO.HIGH, key, device)

	def switchOff(self, device_id):
		key = [int(device_id[0]),int(device_id[1]),int(device_id[2]),int(device_id[3]),int(device_id[4])]
		device = self.device_letter[device_id[5]]
		self._switch(GPIO.LOW, key, device)

	def _switch(self, switch, key, device):
		self.bit = [142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 136, 128, 0, 0, 0]		

		for t in range(5):
			if key[t]:
				self.bit[t]=136	
		x=1
		for i in range(1,6):
			if device & x > 0:
				self.bit[4+i] = 136
			x = x<<1

		if switch == GPIO.HIGH:
			self.bit[10] = 136
			self.bit[11] = 142
				
		bangs = []
		for y in range(16):
			x = 128
			for i in range(1,9):
				b = (self.bit[y] & x > 0) and GPIO.HIGH or GPIO.LOW
				bangs.append(b)
				x = x>>1
				
		GPIO.output(self.pin, GPIO.LOW)
		for z in range(self.repeat):
			for b in bangs:
				GPIO.output(self.pin, b)
				time.sleep(self.pulselength/1000000.)

#######################################################################

class Database:

	def __init__(self, file):
		self.tinydb = TinyDB(file)
		self.devices_table = self.tinydb.table('devices')
		self.Device = Query()

	def get_eid(self, device_id):
		el_list = self.devices_table.search(self.Device.device == device_id)
		if len(el_list) < 1: return False 	# nothing found
		eid = el_list[0].eid
		print(device_id,' already exists in db with eid ',eid)
		return eid

	def add(self, device_id, name, state='off'):
		eid = self.get_eid(device_id)
		if eid is False:
			self.devices_table.insert({'device':device_id,'name':name,'state':state})
			print('added: ',device_id,', ',name,', state: ', state)
			return 'added'
		else:
			self.devices_table.update({'name':name,'state':state}, eids=[eid])
			print('updated: ',device_id,', ',name,', ', state)
			return 'updated'

	def remove(self, device_id):
		eid = self.get_eid(device_id)
		if eid is False: flask.abort(400) # does not exist
		self.devices_table.remove(eids=[eid])
		print('removed: ',device_id)
		return 'removed'

	def list(self):
		print('sending list ...')
		return self.devices_table.all()

	def switch_state(self, device_id, state):
		eid = self.get_eid(device_id)
		if eid is False: return False # does not exist
		self.devices_table.update({'state':state}, eids=[eid])
		return True



#######################################################################

def cleanup():
	GPIO.cleanup()

def is_authorized(request):
	if request.headers['Content-Type'] == 'application/json':
		newInput = request.json
		if 'secret' in newInput and newInput['secret'] == secret:
			print('request authorized')
			return True
	elif request.args['secret'] == secret:
		print('request authorized')
		return True
	else:
		flask.abort(550)


#######################################################################

if __name__ == '__main__':
	atexit.register(cleanup)
	
	default_GPIO_pin = 17					# change the GPIO pin according to your wiring
	remoteSwitch = RemoteSwitch(pin=default_GPIO_pin)

	secret = 'test' 					# TODO: changable

	device_regex = re.compile("[01]{5}[A-G]")	# regex to test device indentifiers

	db = Database(file='db.json')
	app.run(host='0.0.0.0', port=80)
