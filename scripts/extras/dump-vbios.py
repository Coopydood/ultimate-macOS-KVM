#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""


# COOPYDOOD INTERNAL TERMINAL UI BLUEPRINT


import os
import time
import subprocess
import re 
import json
import sys
import argparse
sys.path.append('./resources/python')
from cpydColours import color

detectChoice = 1
latestOSName = "Sequoia"
latestOSVer = "15"
runs = 0


class cpyd:
    HEADING = "DUMP VBIOS ASSISTANT"
    SUBHEADING = "by Coopydood"

    BODY_1 = "This tool can assist you in dumping the contents"
    BODY_2 = "of your GPU's onboard video BIOS (VBIOS) for use"
    BODY_3 = "with this project's passthrough functionality."

    CALLTOACTION = "Select an option to continue."
    
    USER_SELECT_TITLE_1 = "Dump VBIOS..."
    USER_SELECT_TITLE_2 = "MAJOR_SELECTION2"

    USER_SELECT_BODY_1 = "Continue to GPU selection."
    USER_SELECT_BODY_2 = "Oh look, yet another example body of text\n         underneath a user-selectable option header."

    USER_SUBSELECT_TITLE_1 = "MINOR_SELECTION1"

    USER_HELP_TITLE = "Help"
    USER_ESCAPE_TITLE = "Exit to Extras"

    INPUT_FIELD_TEXT = "Select"

def initMenu():
    global detectChoice
    print("\n\n  "+color.BOLD+color.GREEN,cpyd.HEADING+color.END,"")
    print("  ",cpyd.SUBHEADING+color.END+"\n")
    print("  ",cpyd.BODY_1,"\n  ",cpyd.BODY_2,"\n  ",cpyd.BODY_3+color.END)
    #print("  ",cpyd.CALLTOACTION)
    print(color.BOLD+"\n      1.",cpyd.USER_SELECT_TITLE_1)
    print(color.END+"        ",cpyd.USER_SELECT_BODY_1+"\n")
    print(color.END+"      ?.",cpyd.USER_HELP_TITLE)
    print(color.END+"      Q.",cpyd.USER_ESCAPE_TITLE+"\n")
    detectChoice = str(input(color.BOLD+cpyd.INPUT_FIELD_TEXT+"> "+color.END))
    return


def startup():
    global detectChoice
    initMenu()

       


def clear(): print("\n" * 150)

startup()