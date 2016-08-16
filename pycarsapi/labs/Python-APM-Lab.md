# Lab Exercise

## Configure and Use New Relic APM Service with Python

- From the PWS Apps Manager, go to the Marketplace and provision a free new New Relic service instance. Name the instance anything you would like (suggestion: "newrelic"). Do not bind to an app yet.

- The PHP and Java buildpacks automatically add the New Relic agent if the New Relic service has been bound to the application but the Python buildpack does not. There are further modifications required to get Python apps to use New Relic for APM monitoring.

    ````bash
    $ pip install newrelic
    $ newrelic-admin generate-config <YOUR-LICENSE-KEY-HERE> newrelic.ini
    ````

- Then edit the `newrelic.ini` file created in the last step so that:

    - app_name = PyCarsAPI
    - log_file = ./logs/newrelic-python-agent.log

- Next alter the `Procfile` so that New Relic 'wraps' the uWGSI application:

    ````bash
    web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uwsgi --http :8080 --wsgi-file app.py --callable app --logto ./logs/server.log --enable-threads --single-interpreter
    ````
    
    > Note that different WSGI servers have different settings, so you'll have to find the right ones for you in the New Relic online help.

- Now you can use `cf push` to upload your app (while targetting PWS).

- Scale your app to two instances.

- Once the application starts, use the JMeter project to put some load on the app.

- Return to the PWS Apps Manager. From the list of services in your application’s	space, locate the new-relic service and click on the "Manage" link.

- New Relic will use OAuth for authentication, so you will be prompted with a login screen from Pivotal Web Services.

- Agree to the New Relic terms of service, or temporarily defer.

- You should now see a page that lists your Cloud Foundry application with the name you put in the newrelic.ini file. Click on this entry to obtain detailed monitoring information. (Note that it may take several minutes for any performance monitoring information to appear.)

- Congratulations! You have successfully bound your application to an APM via a Pivotal Cloud Foundry service. If you have time, investigate the APM’s capabilities.

> Note that for this Python application, it's not actually necessary to have the New Relic service bound to your app in the Cloud Foundry. Therefore, the app should still run and output APM stats even in PCF DEV. If this were a Java or PHP application the process would be simpler as all that is required is for the New Relic service to be available to the app in Cloud Foundry, but this service is not available in PCF DEV.

## Troubleshooting

If you have issues try the following:-

- Make sure you can login to New Relic using the 'Manage' link in PWS.

- Set the newrelic log level to debug in the newrelic.ini file.

- Validate the configuration in the newrelic.ini by running the validator:-

    ````bash
    $ cf push -c "newrelic-admin validate-config newrelic.ini - stdout"
    ````
  
  Remember to `cf push -c null` afterwards to reset your push command settings.

- Check the [Troubleshooting Guide](https://docs.newrelic.com/docs/agents/python-agent/troubleshooting) on the NewRelic app.
