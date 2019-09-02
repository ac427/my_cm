#!/usr/bin/python

import xmlrpclib
import requests
import sys
import ConfigParser
import json  

Config = ConfigParser.ConfigParser()
Config.read('/home/ac/.spacecmd/config')
SATELLITE_LOGIN = Config.get ("spacecmd", "username")
SATELLITE_PASSWORD= Config.get ("spacecmd", "password")
SATELLITE_URL = "https://spacewalk.foo.com/rpc/api"


client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

Config.read('/home/ac/.slack/config')
SLACKUSER=Config.get("slack", "username")
CHANNEL=Config.get("slack", "channel")
WEBHOOK_URL=Config.get("slack", "webhook")

inactive_systems = client.system.listInactiveSystems(key)
inactive_systems_list =[]

for inactive in inactive_systems:
  inactive_systems_list.append(inactive['name'])


data = {
  "username": SLACKUSER,
  "channel": CHANNEL,
  "icon_emoji": ":female-astronaut::skin-tone-4:",
  "attachments": [
    {
      "fallback": "Spacewalk - https://spacewalk.foo.com",
      "text": "<https://spacewalk.foo.com|Spacewalk> ",
      "author_icon": "https://avatars2.githubusercontent.com/u/6648455?s=200&v=4",
      "fields": [
        {
          "title": "Inactive Systems",
          "value": 'List of inactive systems: '+' '.join(inactive_systems_list)
        }
      ],
      "footer": "Spacewalk",
      "footer_icon": "https://avatars2.githubusercontent.com/u/6648455?s=200&v=4",
      "color": "danger"
    }
  ]
}

if inactive_systems_list:
  response = requests.post(WEBHOOK_URL, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

client.auth.logout(key)
