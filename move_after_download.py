#!/usr/bin/python3

# Set this to run "On Import/On Upgrade"
# Because of how torrents work, Sonarr hardlinks or copies a file instead of moving it to its final destinination.
# After Sonarr imports the file, this script will change the save location in qBittorrent to where Sonarr
# saved it and delete it from the save location, essentially doing an equivalent to moving the file after download.

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
        logging.info("Login successful.")
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        logging.info("Login FAILED.")
        logging.info(e)
        sys.exit()

def importOrUpgrade():
    qbittorrent = login()
    download_id = vars["sonarr_download_id"]
    try:
        if qbittorrent.torrents_properties(download_id)['is_private']:
            qbittorrent.torrents_set_save_path(save_path=os.path.dirname(vars["sonarr_episodefile_path"]), torrent_hashes=download_id)
        os.remove(vars['sonarr_episodefile_sourcepath'])
    except Exception as e:
        logging.error(f"Error: {e}")

match vars["sonarr_eventtype"]:
    case "Grab":
        for var in vars:
            logging.info(f'{var} = {vars[var]}')
        logging.info('Grab event successful')
    case "Download":
        for var in vars:
            logging.info(f'{var} = {vars[var]}')
        importOrUpgrade()
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
