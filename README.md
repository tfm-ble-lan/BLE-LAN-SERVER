# TFM-BLE-SERVER
[![Docker Image CI](https://github.com/geonexus/TFM-BLE-LAN/actions/workflows/docker-image.yml/badge.svg)](https://github.com/geonexus/TFM-BLE-LAN/actions/workflows/docker-image.yml)

## Trello board Development
https://trello.com/c/zdqi9l4A

## Production Server
https://tfmbleserver.azurewebsites.net/

## Portal Azure
https://portal.azure.com/

## References
BLEAK - https://github.com/hbldh/bleak

BUILD IMAGE
-----------
docker build . --file Dockerfile --tag ble-lan-server:latest

RUN_IMAGE
---------
docker run -d --name ble_lan_server -p 80:80 ble-lan-server

For local execute:

    python app.py

RUN IN PRODUCTION
-----------------

Remember to set some environment variables to connect the container to the Mongo Database:
- AZURE_DB_HOST
- AZURE_DB_PORT
- AZURE_DB_PRIMARY_USER
- AZURE_DB_PRIMARY_PASS
- AZURE_DB_SECONDARY_USER
- AZURE_DB_SECONDARY_PASS
- APP_ENV (AzurePrimary, AzurePrimary, AzureTest, Local)
