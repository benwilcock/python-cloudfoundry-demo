#!/bin/bash
# Gets an API token for a local PCF DEV instance and puts it in a file called 'token.json'.
curl -k -H 'AUTHORIZATION: Basic Y2Y6' -d 'username=user&password=pass&grant_type=password' https://uaa.local.pcfdev.io/oauth/token > token.json