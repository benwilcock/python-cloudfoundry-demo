# Deploying Python Apps to Pivotal Web Services

In this tutorial you'll learn how to deploy Python applications to [Pivotal Web Services (a.k.a PWS)](https://run.pivotal.io/). It should take no more than about 15 - 30 minutes to complete this tutorial, by the end of which you'll have deployed two applications to the cloud (a web-app and a microservice). You don't have to write any code, all the code has been provided.

## Getting Started

First, download a ZIP of this repository and unpack it into to your preferred local workspace location. Open a terminal or command line and go to the directory you just created.

````bash
$ cd <path-to>/python-cloudfoundry-demo
````

Next, if you don't have Pivotal Web Services account and no other access to Pivotal Cloud Foundry but you'd still like to follow along with this tutorial, follow the simple instructions below to get yourself set-up:-

* Follow the Getting Started guide here: [Getting Started](https://docs.run.pivotal.io/starting/index.html) to register for a free Pivotal Web Services account
* Install the [CF CLI command line tools](https://docs.run.pivotal.io/cf-cli/install-go-cli.html) on your computer

Finally, you should now be able to login to Pivotal Web Services with the command line tool as follows:-

````bash
$ cf login -a https://api.run.pivotal.io
````

> To login you'll need the email and password details you used to sign up for your account and the first time you login you may be asked for your API key which can be found in your account profile online.

Once you've logged in, if you execute `cf target` at the cmd line, you should see something like this:-

````bash
API endpoint:   https://api.run.pivotal.io (API version: 2.58.0)
User:           user@org.com
Org:            myorg
Space:          development
````

This output is telling you that your CF CLI has successfully connected to the Pivotal Web Services endpoint at `https://api.run.pivotal.io` and you're ready to push applications to your `development` space.

## Running the 'Hello World' application

The folder `hello-world` contains a basic Python web application that you can quickly push to Cloud Foundry.

#### This App Can Run on...

* [Pivotal Web Services (PWS)](https://run.pivotal.io/)
* PCF Dev (if you've installed it locally)
* Pivotal Cloud Foundry Installations

#### To Run The App on PWS...

Assuming you've already connected your CF CLI to Pivotal Web Services, simply execute the following commands while the source directory. 

> In the `push` command below, to prevent your app-name clashing with someone else's you should replace `<initials>` with your initials and `<4didgitnum>` with a random 4 digit number of your choice.

````bash
$ cd hello-world
$ cf push pyhello-world-<initials>-<4digitnum>
````

After a short while and some output, you should see something like this...

````bash
requested state: started
instances: 1/1
usage: 256M x 1 instances
urls: pyhello-world-grouselike-gateau.cfapps.io
last uploaded: Wed Aug 10 14:55:44 UTC 2016
stack: cflinuxfs2
buildpack: python 1.5.8

     state     since                    cpu    memory         disk         details
#0   running   2016-08-10 03:58:03 PM   0.0%   824K of 256M   1.3M of 1G
````

To see your app, paste the url given on the line `urls:` into a browser window. You should see 'Python Hello World!' and a bunch of other stuff. 

Congratulations, you just deployed an app to the cloud. Use `cf help` and take a look at what you can do with the `scale` command (spoiler: it's awesome!).

## Running the 'PyCarsApi' Microservice

The folder `pycarsapi` contains a Python microservice application which you can also push to Cloud Foundry. This application expects a service called 'postgresql' to be available when you push it.

#### This App Can Run On...

* [Pivotal Web Services (PWS)](https://run.pivotal.io/)
* Pivotal Cloud Foundry (*if you have a PostgreSQL service available in your installation's marketplace*)

#### This App Depends On....

* Cloud Foundry PostgreSQL Service attached to the space where you push it (*instructions on to create and attach this service when using Pivotal Web Services are below*)

#### To Run The App on PWS...

The first thing you'll need to do is provision your PostgreSQL service on Pivotal Web Services. Because Pivotal web Services has a PostgreSQL service broker from ElepantSQL, you can add the Postgres database service very easily using the CF CLI.

````bash
$ cd ../pycarsapi
$ cf create-service elephantsql turtle postgresql
````

This command tells the ElephantSQL service provider to provision a free 'turtle' sized account for your databases and attach it as a Cloud Foundry service using the service name `postgresql`. Once attached, the app can use the environment properties given to it to connect to the Postgres database. To double check your database service was created and has the right name do the following...

````bash
$ cf services

name         service       plan     bound apps                 last operation
postgresql   elephantsql   turtle                              create succeeded
````

The `cf services` command just lists the current services in your Cloud Foundry space so you can visually check that `postgresql` was added to it as requested. Here you can see the __postgresql__ service has been added but no apps have bound to it yet (as expected - it's brand new).

This time I've made deploying the app simpler by specifying a `manifest.yml` file for Cloud Foundry to use as deployment settings. If you take a look inside the [manifest.yml](manifest.yml) within the pycarsapi application you'll see how this file guides the `push` by specifying how the app should be be deployed. In this case it specifies the application a name, assigns it a random route to avoid duplication and specifies which services it needs. For it to work properly, make sure you keep `postgresql` as the database service name as the application is expecting a service with this name to be available in the space when deploying.

To run the pycarsapi microservice, simply 'push' it to Cloud Foundry...

````bash
$ cf push
````

Cloud Foundry will upload all the files in the `pycarsapi` directory to Pivotal Web Services which will then deploy the application using the standard Python buildpack. Once deployed, the application's endpoint address will be given to you (look for something like `urls: pycarsapi-mystery-machine.cfapps.io`). 


If you `curl -X GET http://<your url here>/cars` you should see a response containing a list of vehicle manufacturers similar to the one below...

````json
[[1, "Audi"], [2, "Mercedes"], [3, "Skoda"], [4, "Volvo"], [5, "Bentley"], [6, "Citroen"], [7, "BMW"], [8, "Volkswagen"]]
````

This data came from the postgres database on Pivotal Web services. Don't believe me? If you login to the Pivotal Apps Manager online at [http://run.pivotal.io](http://run.pivotal.io) then go to the `pycarsapi` app in your space. Click on 'Services' > 'ElephantSQL' > 'Manage' > 'Browse'. From here within ElephantSQL you can issue SQL statements directly against your databases. Type `SELECT * FROM demo.cars` and click 'Execute'. The table you see returned should contain the same data as that listed above.

Congratulations, you just self-provisioned a new PostgreSQL database service and pushed a microservice application that depends upon it into the cloud.