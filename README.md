# Python Cloud Foundry Demo's

The simple Python Microservice can be used to test deployment of Python applications to Pivotal Cloud Foundry (PCF) installations and [Pivotal Web Services (a.k.a PWS)](https://run.pivotal.io/). 

## Getting Started

First, make a clone of this repository onto your local file system.

````bash
$ git clone https://github.com/benwilcock/python-cloudfoundry-demo.git
````

Second, if you don't have Pivotal Cloud Foundry yet but you'd like to follow along with this tutorial, follow the simple instructions below to get yourself set-up:-

* Follow the Getting Started guide here: [Getting Started](https://docs.run.pivotal.io/starting/index.html) to register for a free Pivotal Web Services account and [install the CF CLI command line tools](https://docs.run.pivotal.io/cf-cli/install-go-cli.html)

You can then login to Pivotal Web Services from the command line as follows

````bash
$ cf login -a https://api.run.pivotal.io
````

> To login you'll need the email and password you used to sign up and the first time you do it it may ask for your API key which can be found in your account profile.

Once you've logged in, if you execute `cf target` at the cmd line, you should see something like:

````bash
API endpoint:   https://api.run.pivotal.io (API version: 2.58.0)
User:           user@org.com
Org:            myorg
Space:          development
````

If you see this, your CF CLI has successfully connected to Pivotal Web Services (api.run.pivotal.io) and you're ready to push applications to it.

## Running the 'Hello World' application

The folder `hello-world` contains a basic Python web application that you can push to Cloud Foundry.

#### This App Runs on...

* Local PC
* PCF DEV
* Pivotal Web Services
* Pivotal Cloud Foundry

#### This App Requires...

* Nothing (*when running on PCF DEV, PWS or Pivotal Cloud Foundry*)
* Python3, pip3, flask (*but only if you plan to run it locally on your PC*)

#### To Run The App on PWS...

Assuming you've already connected your CF CLI to Pivotal Web Services, simply execute the following commands while in your git cloned directory.

````bash
$ cd hello-world
$ cf push
````

After a short while and some output, you should see something like this...

````bash
requested state: started
instances: 1/1
usage: 256M x 1 instances
urls: pyhello-world-grouselike-gteau.cfapps.io
last uploaded: Wed Aug 10 14:55:44 UTC 2016
stack: cflinuxfs2
buildpack: python 1.5.8

     state     since                    cpu    memory         disk         details
#0   running   2016-08-10 03:58:03 PM   0.0%   824K of 256M   1.3M of 1G
````

To see your app, paste the url given on the line `urls:` into a browser window. You should see 'Python Hello World!' and a bunch of other stuff.

## Running the 'PyCarsApi-v1' Microservice

The folder `pycarsapi-v1` contains a Python microservice application which is backed by a database and which you can also push to Cloud Foundry.

#### This App Runs On...

* [Pivotal Web Services (PWS)](https://run.pivotal.io/)
* Pivotal Cloud Foundry (*if you have a PostgreSQL service available in the marketplace*)

#### This App Depends On....

* Cloud Foundry PostgreSQL Service (*instructions to attach this service when using Pivotal Web Services are below*)

#### To Run The App on PWS...

The first thing you'll need to do is provision your PostgreSQL service on Pivotal Web Services. Because Pivotal web Services already has a PostgreSQL service broker installed (called ElepantSQL), you can add the Postgres database service very easily using the CF CLI you installed earlier.

````bash
$ cd pycarsapi-v1
$ cf create-service elephantsql turtle postgresql
````

This command tells the ElephantSQL service provider to create a free 'turtle' account for your databases and attach it to Cloud Foundry using the service name `postgresql`. Once attached, the app can use the environment properties given to it to connect to the Postgres database. To double check your database service was created and has the right name do the following...

````bash
$ cf services

name         service       plan     bound apps                 last operation
postgresql   elephantsql   turtle                              create succeeded
````

The `cf services` command just lists the current services in your Cloud Foundry space so you can visually check that `postgresql` was added to it as requested. Here you can see the __postgresql__ service has been added but no apps have bound to it yet (as expected, it's new!).

Within the pycarsapi-v1 application the [manifest.yml](manifest.yml) file controls how the app will be deployed to Cloud Foundry, so make sure you keep the `postgresql` database service name as the application is configured to expect that service name when deploying.

Finally, to run the pycarsapi-v1 microservice, simply 'push' it to the Cloud Foundry...

````bash
$ cf push
````

Cloud Foundry will upload all the files in the directory to Pivotal Web Services which will then deploy the application using the standard Python buildpack. Once deployed, the application's endpoint address will be given to you (look for something like `urls: pycarsapi-v1-mystery-machine.cfapps.io`). 


If you `curl -X GET http://<your url here>/cars` you should see a response containing a list of vehicle manufacturers similar to the one below...

````json
[[1, "Audi"], [2, "Mercedes"], [3, "Skoda"], [4, "Volvo"], [5, "Bentley"], [6, "Citroen"], [7, "BMW"], [8, "Volkswagen"]]
````

This data came from the postgres database on Pivotal Web services. Don't believe me? If you login to the Pivotal Apps Manager online at [http://run.pivotal.io](http://run.pivotal.io) then go to the `pycarsapi-v1` app in your space, then under 'services' you'll find ElephantSQL and from there you can choose to 'manage' your databases and then 'browse' them. From here within ElephantSQL you can issue SQL statements directly against your databases. Try `SELECT * FROM demo.cars`. The data you see returned should be the same as that listed above.