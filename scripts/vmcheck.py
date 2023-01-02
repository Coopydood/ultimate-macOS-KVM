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

output_stream = os.popen('lspci |  grep "VMWare"')
vmc1 = output_stream.read().splitlines()

output_stream1 = os.popen('lspci |  grep "VirtualBox\|Oracle"')
vmc2 = output_stream1.read().splitlines()

output_stream2 = os.popen('lspci |  grep "Redhat\|RedHat"')
vmc3 = output_stream2.read().splitlines()

for x in vgaGrep:
    print("\n",x)