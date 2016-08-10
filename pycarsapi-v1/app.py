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
db = os.getenv('DATABASE_URL', None)

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
    message += 'This <b>Microservice</b> lists the Vehicle manufacturers in a \'bound\' Postgres database<p/>'
    message += '<ul><li>Instance index ['+inst+']</li>'
    message += '<li>Hosted internally on [' + host + ':' + str(port) + ']</li>'
    message += '<li>[' +mem+ '] memory</li>'
    message += '<li>Postgresql DB is available: ['+str(connected)+']</li>'
    message += '<li>Cars REST API Endpoint <a href="./cars">[GET (JSON)]</a>.</li></ul>'
    message += '<H3>Application Environment Variables</H3><small>'
    message += pprint.pformat(str(os.environ))
    message += '</small><p><blockquote><b>FYI:</b> The environment variables added by PCF services are listed under '
    message += 'VCAP_XXXX but some are promoted (such as \'MEMORY_LIMIT\' etc.)</blockquote></body></html>'
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