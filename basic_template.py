#!/usr/bin/python3
import sys
import qbittorrentapi
import os
import logging

logging.basicConfig(filename='/config/scripts/log.log', level='INFO')

# This loads all the variables available for use in your script. See https://wiki.servarr.com/sonarr/custom-scripts.
vars = {}
for k, v in os.environ.items():
    if 'sonarr' in k:
        vars[k] = v
        logging.debug(f'{k} = {v}')

logging.info(f'-------------------------{vars["sonarr_eventtype"]} event triggered-------------------------')

def login():
    qbt_client = qbittorrentapi.Client(host='192.168.1.2:8081', username='admin', password='adminadmin')
    try:
        qbt_client.auth_log_in()
        logging.info("Login successful.")
    except qbittorrentapi.LoginFailed as e:
        logging.info("Login FAILED.")
        logging.info(e)
        sys.exit()

match vars["sonarr_eventtype"]:
    case "Grab":
        logging.info('Grab event successful')
    case "Download":
        logging.info('Download event successful')
    case "Rename":
        logging.info('Rename event successful')
    case "EpisodeFileDelete":
        logging.info('EpisodeFileDelete event successful')
    case "SeriesDelete":
        logging.info('SeriesDelete event successful')
    case "HealthIssue":
        logging.info('HealthIssue event successful')
    case "ApplicationUpdate":
        logging.info('ApplicationUpdate event successful')
    case "Test":
        logging.info('Test event successful')
    case unknown_event:
        print (f"Unknown event '{unknown_event}'")



logging.info(f'-------------------------End {vars["sonarr_eventtype"]} event-------------------------')

# On Grab = Grab
# On Import/On Upgrade = Download
# On Rename = Rename
# On Episode File Delete = EpisodeFileDelete
# On Series Delete = SeriesDelete
# On Health Issue = HealthIssue
# On Application Update = ApplicationUpdate
# On Test = Test
