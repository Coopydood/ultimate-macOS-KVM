#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

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

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

version = open("./VERSION")
version = version.read()

if os.path.exists("./resources/WEBVERSION"): os.system("rm ./resources/WEBVERSION")
os.system("wget -q --output-document=./resources/WEBVERSION --no-cache --no-cookies https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION")
webVersion = open("./resources/WEBVERSION")
webVersion = webVersion.read()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

print("Your version:",version)
print("Web version:",webVersion)

#https://raw.githubusercontent.com/Coopydood/ultimate-macOS-KVM/main/VERSION