#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.
You are free to distribute this script however you see fit as long as credit is given.
Enjoy!

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

output_stream = os.popen('lspci -nn |  grep "Display\|VGA\|Audio device" | cut -d"(" -f 1')
vgaGrep = output_stream.read().splitlines()

for x in vgaGrep:
    print("\n",x)

print("\n"+color.BOLD+color.CYAN+"HOW TO:"+color.END,"For each device you intend on passing through, look at the end of the entry\n        toward the value INSIDE"+color.BOLD+" the last pair of sqaure [] brackets."+color.END,"\n        There should bean 8-digit value split by a colon, such as XXXX:XXXX.\n"+color.BOLD+"        Note down this value, with the colon included."+color.END)
print("\n"+color.BOLD+"         Example:"+color.END,"...[AMD Radeon RX 550]"+color.BOLD+"[1002:67ff]"+color.END+" = "+color.BOLD+color.YELLOW+color.UNDERLINE+"1002:67ff"+color.END+"\n")