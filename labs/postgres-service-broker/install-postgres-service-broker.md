# Exercise

## Install Postgres Service Broker

### Requirements

- PCF Dev running locally
- An app on PCF Dev you want to bind a service to
- Docker for Mac, Docker for Windows, Docker (Linux)
- Docker Postgres Image Running Locally (use `docker-compose up -d` to ensure you get the right defaults)

### Steps


Begin in the `python-cloudfoundry-demo` folder. If you haven't aready, bring up the Docker container for Postgres:

````bash
$ docker-compose up -d
````

Login to PCF Dev as admin:

````bash
$ cf logout
$ cf login -a api.local.pcfdev.io -o pcfdev-org -u admin -p admin --skip-ssl-validation
````

Push the Postgres CF Service Broker JAR file to PCF Dev:

````bash
$ cd labs/service-broker
$ cf push
````

Create a new service-broker in Cloud Foundry:

````bash
$ cf create-service-broker p-postgres user password http://postgresql-cf-service-broker.local.pcfdev.io
$ cf service-brokers
````

Add the service broker to the Marketplace:

````bash
$ cf enable-service-access PostgreSQL -p "Basic PostgreSQL Plan" -o pcfdev-org
````

Create an instance of the service:

````bash
$ cf create-service PostgreSQL "Basic PostgreSQL Plan" sb-postgres
$ cf services
````

Bind the service to an an existing PCF hosted application:

````bash
$ cf bind-service <app-name> sb-postgres
$ cf restage <app-name>
````

Now check if the service has been added to the application's environment:

````bash
$ cf env <app-name>
````
   > You should see that the "VCAP_SERVICES" environment variable now has a new entry called "PostgreSQL". This entry contains a PostgreSQL database URI unique to this application and various other details about the service such as it's service plan.

````json
{
 "VCAP_SERVICES": {
  "PostgreSQL": [
   {
    "credentials": {
     "uri": "postgres://4c6ad185-c412-41e7-aca3-f4f9bc258268:dt59iv63r4643l2ugffj8in49m@192.168.11.1:5432/4c6ad185-c412-41e7-aca3-f4f9bc258268"
    },
    "label": "PostgreSQL",
    "name": "sb-postgres",
    "plan": "Basic PostgreSQL Plan",
    "provider": null,
    "syslog_drain_url": null,
    "tags": [
     "PostgreSQL",
     "Database storage"
    ]
   }
  ]
 }
}
````

Congratulations, you have added a new type of service broker for Postgres Databases and providioned your first service from the marketplace using the new broker.

## Helping hand

> The source code and documentation for the service broker we have used is [here](https://github.com/cloudfoundry-community/postgresql-cf-service-broker). You can also obtain ready made Cloud Foundry service brokers from lots of organisations both open-source and commercial. 

> You can of course implement your own service brokers using any language web-services aware language.