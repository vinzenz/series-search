#!/usr/bin/env python2

#from subprocess import call

from search import get_magnet_links
import sys
#import os.path
import requests
import json

name, from_season, from_episode = sys.argv[1:4]

result = get_magnet_links(name, False)
seasons = sorted(result.keys())[sorted(result.keys()).index(from_season):]
episodes = sorted(result[seasons[0]].keys())[sorted(result[seasons[0]].keys()).index(from_episode):]

for idx, season in enumerate(seasons):
    for episode in episodes:
        try:
            session = requests.post("http://localhost:9091/transmission/rpc", data=json.dumps({"method":
                "session-get"}))
            session_id = session.headers['X-Transmission-Session-Id']
            response = requests.post("http://localhost:9091/transmission/rpc",
                                     data=json.dumps({"method":"torrent-add","arguments":{"paused":False,"download-dir":"/Users/vfeenstr/Downloads","filename":result[season][episode][0]}}),
                                     headers={'X-Transmission-Session-Id': session_id})
#            call([os.path.expanduser("~/Applications/Deluge.app/Contents/MacOS/Deluge"), "add", result[season][episode][0]])
        except:
            print "Failed to add S{}E{}".format(season, episode)
    if idx + 1 < len(seasons):
        episodes = sorted(result[seasons[idx+1]].keys())
