#!flask/bin/python
from flask import Flask, jsonify
from flask import abort, request
from flask import make_response

from subprocess import Popen
import time
import json

from forecastio import *

#Define some weather constants
MEYRIN=[46.228320, 6.070988]
LATITUDE=MEYRIN[0]
LONGITUDE=MEYRIN[1]
MY_APIKEY='7c33572b2f433a8ede9cb0be2062860a'

##
##define the data structure to hold slaves information and status
##

data = json.loads(open('tlaloc.json').read())
#modules = open('tlaloc.json').read()
print("Current status is:")
print(type(data))
print(data)

'''
modules = [
    {
        'id': 1,
        'name': u'tomatoes',
        'seconds': 4, 
        'watered': False
    },
    {
        'id': 2,
        'name': u'erbe',
        'seconds': 2, 
        'watered': False
    }
]
'''

##
##setup the radio communication
##
##TODO

##
##create the RESTful interface for remote control of slaves
##

app = Flask(__name__)

@app.before_request
def before_request():
  data = json.loads(open('tlaloc.json').read())

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tlaloc/api/v1.0/current', methods=['GET'])
def get_currentWeather():
  fio = ForecastIO.ForecastIO(MY_APIKEY,units=ForecastIO.ForecastIO.UNITS_SI,latitude=LATITUDE,longitude=LONGITUDE)
  current=FIOCurrently.FIOCurrently(fio)
  return jsonify({'temperature': current.temperature, 'humidity': current.humidity, 'feels like': current.apparentTemperature, '%rain': current.precipProbability})
  
@app.route('/tlaloc/api/v1.0/day', methods=['GET'])
def get_dayWeather():
  fio = ForecastIO.ForecastIO(MY_APIKEY,units=ForecastIO.ForecastIO.UNITS_SI,latitude=LATITUDE,longitude=LONGITUDE)
  if fio.has_daily():
    daily = FIODaily.FIODaily(fio)
    today = daily.get_day(0)
    return jsonify({'Min' : today['temperatureMin'], 'Max' : today['temperatureMax']})
  return jsonify({'error' : 'No Daily data available'})


@app.route('/tlaloc/api/v1.0/modules', methods=['GET'])
def get_modules():
    return jsonify(data)

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
  for module in data['modules']:
    if module['id'] == module_id:
      return jsonify({'module': module})
  abort(404)

@app.route('/tlaloc/api/v1.0/modules', methods=['POST'])
def create_modules():
    if not request.json or not 'name' or not 'seconds' in request.json:
        abort(400)
    module = {
        'id': request.json['id'],
        'name': request.json['name'],
        'seconds': request.json['seconds'],
        'watered': False
    }
    data['modules'].append(module)
    file = open('tlaloc.json','w')
    file.write(json.dumps(data))
    return jsonify({'module': module})

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    ##do some validation on the input request
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'seconds' in request.json and type(request.json['seconds']) is not int:
        abort(400)
    if 'watered' in request.json and type(request.json['watered']) is not bool:
        abort(400)
    ##OK, if we are it means the request is good enough
    for module in data["modules"]:
      if module['id'] == module_id:
        module['name'] = request.json.get('name', module['name'])
        module['seconds'] = request.json.get('seconds', module['seconds'])
        module['watered'] = request.json.get('watered', module['watered'])
        return jsonify({'module': module})
    #If we are here the input id was not matched
    abort(404)

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
  for module in data["modules"]:
    if module['id'] == module_id:
      data["modules"].remove(module)
      file = open('tlaloc.json','w')
      file.write(json.dumps(data))
      return jsonify({'result': "Success"})
  #If we are here the input id was not matched
  abort(404)

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>/go', methods=['GET'])
def go_module(module_id):
  for module in data["modules"]:
    if module['id'] == module_id:
      ##prepare the communication with module module_id
      ##TODO
      ##prepare the command to send
      ##send command to module module_id
      print("Sending watering command to module " + str(module_id) + ": " + str(module['seconds']) + "s")
      ##listen for confirmation
      print("Waiting for confirmation until timeout")
      received = True
      if received:
        return jsonify({'result': "Success"})
      else:
        return jsonify({'result': "Did not received slave confirmation"})
  abort(404)

@app.route('/tlaloc/api/v1.0/listen', methods=['POST'])
def listen():
  print("Launch the process to serve slave command requests...")
  proc=Popen("ls")
  ##proc=Popen("pimaster-nrf.exe")
  procId=proc.pid
  time.sleep(3)
  procExitCode=proc.poll()
  if proc.poll() == None:
    return jsonify({'result': "Succcess"})
  else:
    return jsonify({'result': "Error, process returned " + str(procExitCode)})

if __name__ == '__main__':
    app.run(debug=True)
    print("running?")
