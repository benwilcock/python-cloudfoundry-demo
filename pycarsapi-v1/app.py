import json
import os
import pprint

import psycopg2
import seedy
from flask import Flask

app = Flask(__name__)

port = int(os.getenv('PORT', 5000))
host = str(os.getenv('CF_INSTANCE_IP', '0.0.0.0'))
mem = str(os.getenv('MEMORY_LIMIT', 'UNKNOWN'))
inst = str(os.getenv('CF_INSTANCE_INDEX', 'UNKNOWN'))
db = os.getenv('DATABASE_URL', 'postgres://postgres:password@127.0.0.1:5432/postgres')

connected = False
cur = None
seeded = False

if db is not None:
    try:
        conn = psycopg2.connect(db)
        connected = True
        cur = conn.cursor()
    except:
        connected = False

@app.before_first_request
def seed():
    if connected is True:
        seedy.seedCarsDb()

@app.route('/', methods = ['GET'])
def hello_world():
    message = '<html><head/><body><H1>[Python] Cars API Microservice v1</H1>'
    message += 'This <b>Microservice</b> lists the Vehicle manufacturers in a \'bound\' Postgres database<p/><ul>'
    message += '<li>Instance: <b>['+inst+']</b></li>'
    message += '<li>Memory: <b>[' +mem+ ']</b></li>'
    message += '<li>DB Connected: <b>['+str(connected)+']</b></li>'
    message += '<li>REST API Endpoint: <a href="./cars">[GET (JSON)]</a>.</li>'
    message += '</ul><H3>Application Environment Variables</H3><small>'
    message += pprint.pformat(str(os.environ))
    message += '</small><p><blockquote><b>FYI:</b> If available, the ENV variables for PCF services are listed under '
    message += 'VCAP_XXXX (but some may get promoted).</blockquote></body></html>'
    app.logger.info('Publishing: ' + message)
    return message

### cars api - GET - retrieve cars
@app.route('/cars', methods=['GET'])
def get_cars():
     response = ''
     query = 'SELECT * FROM demo.cars'
     if cur is not None:
         cur.execute(query)
         conn.commit()
         rows = cur.fetchall()
         response = json.dumps(rows)
     return response

if __name__ == '__main__':
    app.logger.info('Starting up...')
    app.run(host=host, port=port, debug=False)