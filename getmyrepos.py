#!/usr/bin/env python3
# Get public repos
import requests
import json

r = requests.get("https://api.github.com/users/alexloser/repos?type=all&page=1&per_page=99")

print("#!/bin/bash")
for d in json.loads(r.content.decode()):
    print("wget", d["html_url"] + "/archive/master.zip -O", d["name"] + ".zip")

