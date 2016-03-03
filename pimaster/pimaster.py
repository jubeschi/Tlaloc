#!flask/bin/python
from flask import Flask, jsonify
from flask import abort, request
from flask import make_response

app = Flask(__name__)

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

@app.route('/tlaloc/api/v1.0/modules', methods=['GET'])
def get_modules():
    return jsonify({'modules': modules})

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
  for module in modules:
    if module['id'] == module_id:
      return jsonify({'module': module})
  abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

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
    module = [module for module in modules if module['id'] == module_id]
    if len(module) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'seconds' in request.json and type(request.json['seconds']) is not int:
        abort(400)
    if 'watered' in request.json and type(request.json['watered']) is not bool:
        abort(400)
    module[module_id-1]['name'] = request.json.get('name', module[module_id-1]['name'])
    module[module_id-1]['seconds'] = request.json.get('seconds', module[module_id-1]['seconds'])
    module[module_id-1]['watered'] = request.json.get('watered', module[module_id-1]['watered'])
    return jsonify({'module': module[module_id-1]})

@app.route('/tlaloc/api/v1.0/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = [module for module in modules if module['id'] == module_id]
    if len(module) == 0:
        abort(404)
    modules.remove(modules[module_id -1])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
