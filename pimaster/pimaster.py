#!flask/bin/python
from flask import Flask, jsonify
from flask import abort, request
from flask import make_response

##
##define the data structure to hold slaves information and status
##

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

##
##setup the radio communication
##
##TODO

##
##create the RESTful interface for remote control of slaves
##

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tlaloc/api/v1.0/modules', methods=['GET'])
def get_modules():
    return jsonify({'modules': modules})

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
  for module in modules:
    if module['id'] == module_id:
      return jsonify({'module': module})
  abort(404)

@app.route('/tlaloc/api/v1.0/modules', methods=['POST'])
def create_modules():
    if not request.json or not 'name' or not 'seconds' in request.json:
        abort(400)
    module = {
        'id': modules[-1]['id'] + 1,
        'name': request.json['name'],
        'seconds': request.json['seconds'],
        'watered': False
    }
    modules.append(module)
    return jsonify({'module': module}), 201

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    ##module = [module for module in modules if module['id'] == module_id]
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
    for module in modules:
      if module['id'] == module_id:
        module['name'] = request.json.get('name', module['name'])
        module['seconds'] = request.json.get('seconds', module['seconds'])
        module['watered'] = request.json.get('watered', module['watered'])
        return jsonify({'module': module})
    #If we are here the input id was not matched
    abort(404)

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = [module for module in modules if module['id'] == module_id]
    if len(module) == 0:
        abort(404)
    modules.remove(modules[module_id -1])
    return jsonify({'result': "Success"})

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>/go', methods=['GET'])
def go_module(module_id):
  for module in modules:
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
def listen(module_id):
  print("Launch the process to serve slave command requests...")
  #set the NRF to listen, when receiving a request treat it accordingly
  return jsonify({'result': "Succcess"})
  


if __name__ == '__main__':
    app.run(debug=True)
    print("running?")