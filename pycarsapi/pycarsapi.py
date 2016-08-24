import json
import os
import seedy
import connector
from flask import Flask
from flask import Response

app = Flask(__name__)
port = int(os.getenv('PORT', 5000))
host = str(os.getenv('CF_INSTANCE_IP', '0.0.0.0'))
mem = str(os.getenv('MEMORY_LIMIT', 'UNKNOWN'))
inst = str(os.getenv('CF_INSTANCE_INDEX', 'UNKNOWN'))

@app.before_first_request
def seed():
    seedy.seedCarsDb()

@app.route('/', methods = ['GET'])
def hello_world():
    message = '<html><head/><body><H1>[Python] Cars API Microservice</H1>'
    message += 'This <b>Microservice</b> lists popular Vehicle manufacturers contained in a PostgreSQL database.<p/><ul>'
    message += '<li>Instance: <b>['+inst+']</b></li>'
    message += '<li>Memory: <b>[' +mem+ ']</b></li>'
    message += '<li>CARS REST API Endpoint: <a href="./cars">[GET /cars (returns JSON)]</a>.</li>'
    message += '<li>VCAP_APPLICATION: <a href="./application">[GET /application (returns JSON)]</a>.</li>'
    message += '<li>VCAP_SERVICES: <a href="./services">[GET /services (returns JSON)]</a>.</li>'
    message += '</ul></body></html>'
    return message

### cars api - GET - retrieve cars
@app.route('/cars', methods=['GET'])
def get_cars():
    query = 'SELECT * FROM demo.cars'
    connection = connector.getDatabaseConnection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        rows = cursor.fetchall()
        return Response(json.dumps(rows), mimetype='application/json')

### Get the application config
@app.route('/application', methods=['GET'])
def get_application_config():
    vcap_app = json.loads(os.getenv('VCAP_APPLICATION'))
    return Response(json.dumps(vcap_app), mimetype='application/json')

### Get the services config
@app.route('/services', methods=['GET'])
def get_services_config():
    vcap_srv = json.loads(os.getenv('VCAP_SERVICES'))
    return Response(json.dumps(vcap_srv), mimetype='application/json')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=False)