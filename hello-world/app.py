from flask import Flask
import os
import pprint

app = Flask(__name__)

port = int(os.getenv('PORT', 5000))
host = str(os.getenv('CF_INSTANCE_IP', '0.0.0.0'))
mem = str(os.getenv('MEMORY_LIMIT', 'UNKNOWN'))
inst = str(os.getenv('CF_INSTANCE_INDEX', 'UNKNOWN'))

@app.route('/', methods = ['GET'])
def hello_world():
    message = '<html><head/><body><H1>[Python] Hello World!</H1><ul>'
    message += '<li>Version: <b>[1.0]</b></li>'
    message += '<li>Instance: <b>['+inst+']</b></li>'
    message += '<li>Memory: <b>[' +mem+ ']</b></li>'
    message += '</ul></body></html>'
    app.logger.info('Publishing: ' + message)
    return message

if __name__ == '__main__':
    app.run(host=host, port=port, debug=False)