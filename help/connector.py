import os
import json
import psycopg2

conn = None

### Extract the database URI value from VCAP_SERVICES
def getDatabaseUri():

    # Extract VCAP_SERVICES
    vcap_services = os.environ.get('VCAP_SERVICES',
                                   '{"user-provided": [{"credentials": {"uri": "postgres://postgres:password@192.168.11.1:5432/postgres"}, "tags": [], "label": "user-provided", "name": "postgresql"}]}')

    if vcap_services is None:
        print('The VCAP_SERVICES environment variable does not appear to be set.')
        return None

    decoded_config = json.loads(vcap_services)

    for key, value in decoded_config.items():
        print('Inspecting key: "' + str(key) + '" with value: ' + str(value))
        if decoded_config[key][0]['name'] == 'postgresql':
            creds = decoded_config[key][0]['credentials']
            uri = creds['uri']
            print('Identified postgres uri: ' + uri)
            return uri


def getDatabaseConnection():
    uri = getDatabaseUri()
    global conn

    if conn is not None:
        return conn

    if uri is not None:
        try:
            conn = psycopg2.connect(uri)
            print('Connected to: ' + uri)
            return conn
        except:
            print('PyCarsAPI Database Connection Attempt Failed: ')
            return None
    else:
        print('Database Uri was unexpectedly empty: ' + str(uri))
        return None

if __name__ == '__main__':
    uri = getDatabaseUri()
    print('Obtained the postgresql uri: ' + uri + ' from VCAP_SERVICES')
    connection = getDatabaseConnection()
    print('Connected to the database: ' + str(connection))