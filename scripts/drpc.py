#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
It will not work outside of this project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""


import os
import time
import subprocess
import re 
import json
import sys
import argparse
try:
    from pypresence import Presence
except:
     None
osVer = "Unknown"

version = open("./.version")
version = version.read()

versionDash = version.replace(".","-")

parser = argparse.ArgumentParser("main")
parser.add_argument("--os", dest="osVer",action="store")

args = parser.parse_args()

osVer = args.osVer


client_id = "1149434759152422922"

try:
    RPC = Presence(client_id)
except:
    None

projectVer = "Powered by ULTMOS v"+version

if osVer is not None:
    osName = "macOS "+osVer

if osVer is None:
        osVer = "unknown"
        osName = "macOS"
os = "macos"

startTime = int(time.time())
osVer = osVer.replace(" ","")
osOpt = os+"-"+osVer.lower()

if osOpt != "macos-highsierra" and osOpt != "macos-mojave" and osOpt != "macos-catalina" and osOpt != "macos-bigsur" and osOpt != "macos-monterey" and osOpt != "macos-ventura" and osOpt != "macos-sonoma":
     osOpt = "macos-unknown" # arm large image to use the unknown asset if valid macOS version can't be detected

# print("DEBUG:",osVer,osName,osOpt)    #  mmmmm it works, sexy

try:
    RPC.connect()
    RPC.update(large_image="ultmos",large_text=projectVer,details="Loading...",buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
except:
    exit
time.sleep(4)
try:
    RPC.update(small_image="ultmoslite",large_image=osOpt,large_text=osName,small_text=projectVer,details=osName,start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}])) 
    #RPC.update(small_image=osOpt,large_image="ultmos",large_text=osName,small_text=projectVer,details=osName,start=startTime,buttons=([{"label": "View on GitHub", "url": "https://github.com/Coopydood/ultimate-macOS-KVM"}]))
    while True:  
        time.sleep(15) 
except:
    exit