#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# AUTOPILOT BY COOPYDOOD
# (c) Copyright Coopydood 2022-2023

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
from datetime import datetime
import timeit
import random
import uuid
import platform


script = "autopilot.py"
scriptName = "AutoPilot"
scriptID = "APC"
scriptVendor = "Coopydood"

parser = argparse.ArgumentParser("autopilot")
parser.add_argument("--disable-logging", dest="disableLog", help="Disables the logfile",action="store_true")

args = parser.parse_args()

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"
runs = 0

enableLog = True

if args.disableLog == True:
   enableLog = False

version = open("./.version")
version = version.read()

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
   GRAY = '\u001b[38;5;245m'


global logTime

if enableLog == True: # LOG SUPPORT
   if not os.path.exists("./logs"):
      os.system("mkdir ./logs")

   logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
   os.system("echo ULTMOS AUTOPILOT LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/APC_RUN_"+logTime+".log")
   os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/APC_RUN_"+logTime+".log")

   def cpydLog(logStatus,logMsg,*args):
      logFile = open("./logs/APC_RUN_"+logTime+".log","a")
      if logStatus == "ok":      logStatus = "[ ✔ ]"
      if logStatus == "info":    logStatus = "[ ✦ ]"
      if logStatus == "warn":    logStatus = "[ ⚠ ]"
      if logStatus == "error":   logStatus = "[ ✖ ]"
      if logStatus == "fatal":   logStatus = "[ ☠ ]"
      if logStatus == "wait":    logStatus = "[ ➜ ]"
      
      #if logStatus == "ok":      logStatus = "[    OK ]"
      #if logStatus == "info":    logStatus = "[  INFO ]"
      #if logStatus == "warn":    logStatus = "[  WARN ]"
      #if logStatus == "error":   logStatus = "[ ERROR ]"
      #if logStatus == "fatal":   logStatus = "[ FATAL ]"
      #if logStatus == "wait":    logStatus = "[  WAIT ]"
      entryTime = str(datetime.today().strftime('%H:%M:%S.%f'))
      entryTime = entryTime[:-3]
      entryLine = ("["+entryTime+"]"+str(logStatus)+":  "+str(logMsg)+"\n")
      logFile.write(entryLine)
      #os.system("cp ./logs/APC_RUN_"+logTime+".log ./logs/latest.log")
      logFile.close()
else:
   def cpydLog(logStatus,logMsg,*args):
      None


cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/APC_RUN_"+logTime+".log"))


def startup():
    global detectChoice
    cpydLog("info",("Displaying menu"))
    print("\n\n   Welcome to"+color.BOLD+color.PURPLE,"AutoPilot"+color.END,"")
    print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    print("   The purpose of this script is to automatically guide you through \n   the process of",color.BOLD+"creating and running a basic macOS VM",color.END+"using settings \n   based on answers to a number of questions. \n\n   Many of the values can be left to default - especially if you are unsure.\n   It won't be perfect, but it's supposed to make it as"+color.BOLD,"easy as possible."+color.END)
    #print(color.BOLD+"\n"+"   Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"      Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM") # no shameless plugs anymore :[
    if enableLog == False:
       print("\n   "+"  "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
       print("   "+color.BOLD+color.YELLOW+"   ⚠ "+color.END+color.BOLD+" LOGGING DISABLED"+color.END)
       print("   "+color.END+"      The logfile has been disabled. \n         No diagnostic information will be recorded."+color.END)
       print("   "+"  "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)

       #print(color.YELLOW+"\n   ⚠"+color.END+color.BOLD+" WARNING"+color.END)
       #print("   Logging has been disabled")
    #print("   Continue whenever you're ready, or return to the main menu.")
    print(color.BOLD+"\n      1. Start")
    print(color.END+"         Begin creating a new QEMU-based macOS config file \n")
    print(color.END+"      2. Main menu")
    print(color.END+"      ?. Help")
    print(color.END+"      Q. Exit\n")
    cpydLog("ok",str("Menu displayed"))
    cpydLog("wait",("Waiting on user input"))
    detectChoice = str(input(color.BOLD+"Select> "+color.END))
    cpydLog("ok",str("User input received"))
    # EXPERIMENTAL MENU, NOT FINISHED OR IN USE
    #global detectChoice
    #print("\n\n   Welcome to"+color.BOLD+color.PURPLE,"AutoPilot"+color.END,"")
    #print("   Created by",color.BOLD+"Coopydood\n"+color.END)
    #print("   Welcome to AutoPilot - an advanced configuration automation tool.\n   To get started, choose an operation mode from the options below."+color.END)#print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    #print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    #print(color.BOLD+"\n      1. Create boot script... (default)")
    #print(color.END+"         AutoPilot will ask you a series of questions, of which\n         your answers will define the configuration. This will\n         then be processed to generate a valid file.")
    #print(color.BOLD+"\n      2. Create boot script and add to virt-manager...")
    #print(color.END+"         Use this option if you do not have an AutoPilot config file.\n         This script will take you through the AutoPilot steps before\n         generating an XML file based on your answers. No existing\n         data, such as vHDDs, can be used with this method.")
    #print(color.BOLD+"\n      3. Import XML file...")
    #print(color.END+"         Use this option if you already have an XML file.\n         This option lets you import a previously-created XML file\n         into virsh for use with virt-manager.\n")
  
    #print(color.END+"      ?. Help")
    #print(color.END+"      M. Main menu")
    #print(color.END+"      Q. Exit\n")
    #detectChoice = str(input(color.BOLD+"Select> "+color.END))

def clear(): print("\n" * 150)

clear()
startup()
clear()

def autopilot():
   global USR_CPU_SOCKS
   global USR_CPU_CORES
   global USR_CPU_THREADS
   global USR_CPU_MODEL
   global USR_CPU_FEATURE_ARGS
   global USR_ALLOCATED_RAM
   global USR_REPO_PATH
   global USR_NETWORK_DEVICE
   global USR_ID
   global USR_NAME
   global USR_CFG
   global USR_TARGET_OS
   global USR_HDD_SIZE
   global USR_BOOT_FILE
   global USR_MAC_ADDRESS
   global USR_SCREEN_RES
   global USR_TARGET_OS_NAME

   USR_CPU_SOCKS = 1
   USR_CPU_CORES = 2 
   USR_CPU_THREADS = 1
   USR_CPU_MODEL = "Penryn"
   USR_CPU_FEATURE_ARGS = "+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"
   USR_ALLOCATED_RAM = "4G"
   USR_REPO_PATH = "."
   USR_NETWORK_DEVICE = "e1000-82545em"
   USR_ID = "macOS"
   USR_NAME = "macOS"
   USR_CFG = "boot.sh"
   USR_TARGET_OS = 1015
   USR_HDD_SIZE = "80G"
   USR_BOOT_FILE = "BaseSystem.img"
   USR_MAC_ADDRESS = "00:16:cb:00:21:09"
   USR_SCREEN_RES = "1280x720"
   USR_TARGET_OS_NAME = "Catalina"
   
   

   global currentStage
   currentStage = 1
   
   global customValue
   customValue = 0

   
   def stage14():
      global USR_CPU_SOCKS
      global USR_CPU_CORES
      global USR_CPU_THREADS
      global USR_CPU_MODEL
      global USR_CPU_FEATURE_ARGS
      global USR_ALLOCATED_RAM
      global USR_REPO_PATH
      global USR_NETWORK_DEVICE
      global USR_ID
      global USR_NAME
      global USR_CFG
      global USR_TARGET_OS
      global USR_HDD_SIZE
      global USR_BOOT_FILE
      global USR_TARGET_OS_F
      global USR_CPU_TOTAL_F
      global USR_MAC_ADDRESS
      global USR_CREATE_XML
      global USR_CFG_XML
      global USR_TARGET_OS_NAME
      cpydLog("ok",str("Interrogation complete, displaying summary and AP autoflow sliproad"))
      USR_CFG_XML = USR_CFG.replace(".sh",".xml")

      USR_ALLOCATED_RAM_F = USR_ALLOCATED_RAM.replace("G","")
      USR_HDD_SIZE_F = USR_HDD_SIZE.replace("G","")
      USR_CPU_TOTAL = USR_CPU_CORES * USR_CPU_THREADS
      USR_CPU_TOTAL_F = str(USR_CPU_TOTAL)

      if USR_TARGET_OS > 1000:
         USR_TARGET_OS_F = USR_TARGET_OS / 100
      else:
         USR_TARGET_OS_F = USR_TARGET_OS / 10

      if USR_BOOT_FILE == "-1":
         USR_BOOT_FILE_F = "Download from Apple..."
      elif USR_BOOT_FILE == "-2":
         USR_BOOT_FILE_F = "Not configured"
      else:
         USR_BOOT_FILE_F = "Local image file"

      clear()
      if USR_CREATE_XML == "True":
         print("   "+"\n   "+color.BOLD+"Ready to generate files"+color.END)
      else:
         print("   "+"\n   "+color.BOLD+"Ready to generate config file"+color.END)
      #print("   "+"Review your preferences")
      print("   "+"The config wizard is complete.\n   Review your preferences below and continue when ready."+color.END)
      print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
      if USR_CREATE_XML == "True":
         print("   "+color.BOLD+color.PURPLE+"FILES   ",color.END+color.END+USR_CFG+", "+USR_CFG_XML)
      else:
         print("   "+color.BOLD+color.PURPLE+"FILE    ",color.END+color.END+USR_CFG+color.END)
      if USR_TARGET_OS < 1012:
         print("   "+color.BOLD+color.GREEN+"OS      ",color.END+color.END+"Mac OS X",USR_TARGET_OS_NAME,color.END+"("+str(USR_TARGET_OS_F)+")")
      else:
         print("   "+color.BOLD+color.GREEN+"OS      ",color.END+color.END+"macOS",USR_TARGET_OS_NAME,color.END+"("+str(USR_TARGET_OS_F)+")")
      print("   "+color.BOLD+color.YELLOW+"BOOT    ",color.END+color.END+USR_BOOT_FILE_F,color.END)
      print("   "+color.BOLD+color.CYAN+"CPU     ",color.END+color.END+USR_CPU_MODEL+",",USR_CPU_CORES,"cores,",USR_CPU_THREADS,"threads","("+USR_CPU_TOTAL_F+")"+color.END)  
      #print("   "+color.BOLD+color.CYAN+"        ",color.END+color.BOLD+USR_CPU_FEATURE_ARGS+color.END)
      print("   "+color.BOLD+color.CYAN+"RAM     ",color.END+color.END+USR_ALLOCATED_RAM_F+" GB"+color.END)
      print("   "+color.BOLD+color.CYAN+"DISK    ",color.END+color.END+USR_HDD_SIZE_F+" GB (dynamic)"+color.END)
      
      if USR_MAC_ADDRESS != "00:16:cb:00:21:09":
         print("   "+color.BOLD+color.CYAN+"NETWORK ",color.END+color.END+USR_NETWORK_DEVICE+color.END+" ("+USR_MAC_ADDRESS+")")
      else:
         print("   "+color.BOLD+color.CYAN+"NETWORK ",color.END+color.END+USR_NETWORK_DEVICE+color.END+"")
      print("   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
      if USR_BOOT_FILE == "-1":
         print(color.BOLD+"\n      1. Download and generate...")
         print(color.END+"         Fetch a new recovery image, then create the config\n         and hard disk files in the repo folder\n")
      else:
         print(color.BOLD+"\n      1. Generate")
         print(color.END+"         Copy the local recovery image, then create the config\n         and hard disk files in the repo folder\n")
      
      print("    "+color.END+"  B. Back")
      print("    "+color.END+"  X. Start Over")
      print("    "+color.END+"  ?. Help")
      print("    "+color.END+"  Q. Exit\n")
      stageSelect = str(input(color.BOLD+"Select> "+color.END))
   
      if stageSelect == "1":
         #cpydLog("ok",str("Using default value of "+str(defaultValue)))
         handoff()

      elif stageSelect == "b" or stageSelect == "B":
         stage13()

      elif stageSelect == "x" or stageSelect == "X":
         global customValue
         currentStage = 1
         customValue = 0
         stage1()

      elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#review-your-preferences > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage14()
         
      elif stageSelect == "q" or stageSelect == "Q":
         exit   

      else:
            stage14()

   def stage13():
      global customValue
      global currentStage
      global USR_CREATE_XML
      defaultValue = "True"
      cpydLog("ok",str("Stage 13 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"Generate XML file"+color.END)
      print("   Step 13")
      print("\n   You can now generate an XML file during AutoPilot. \n   This will be created alongside your boot script file,\n   and can be imported into virt-manager. This will allow\n   you to use the VM through the GUI, for easy access.\n\n   "+color.BOLD+color.CYAN+"NOTE:",color.END+color.BOLD+"You can convert boot scripts to XML files at\n         any time using the built-in converter tool."+color.END)
      
      print(color.BOLD+"\n      1. Generate and import XML")
      print(color.END+"      2. Skip")
      print(color.END+"\n      B. Back")
      print(color.END+"      ?. Help")
      print(color.END+"      Q. Exit\n   ")
      stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
      if stageSelect == "1":
         cpydLog("ok",str("Using default value of "+str(defaultValue)))
         USR_CREATE_XML = "True"
         blob = open("./blobs/USR_CREATE_XML.apb","w")
         blob.write(USR_CREATE_XML)
         blob.close()
         currentStage = currentStage + 1
         stage14()

      elif stageSelect == "2":
         cpydLog("ok",str("XML generation will be skipped from AP flow"))
         USR_CREATE_XML = "False"
         blob = open("./blobs/USR_CREATE_XML.apb","w")
         blob.write(USR_CREATE_XML)
         blob.close()
         customValue = 1
         stage14()

      elif stageSelect == "b" or stageSelect == "B":
         currentStage = 1
         stage12()
         
      elif stageSelect == "?":
         clear()
         print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
         print("   Continue in your browser\n")
         print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
         os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#13-generate-xml-file > /dev/null 2>&1')
         time.sleep(6)
         clear()
         stage13()

      elif stageSelect == "q" or stageSelect == "Q":
         exit   

      else:
            stage13()
   
   def stage12():
      global customValue
      global currentStage
      global USR_SCREEN_RES
      defaultValue = "1280x720"
      cpydLog("ok",str("Stage 12 sequence initiated"))
      clear()
      
      if USR_TARGET_OS >= 100 and USR_TARGET_OS <= 1012: 
         cpydLog("warn",str("Custom resolution unsupported on legacy OS, using default value of "+str(defaultValue)))
         USR_SCREEN_RES = "1280x720"
         blob = open("./blobs/USR_SCREEN_RES.apb","w")
         blob.write(USR_SCREEN_RES)
         blob.close()
         blob = open("./blobs/.cdn_control","w")
         blob.write("fresh_cdn")
         blob.close()
         currentStage = currentStage + 1
         stage13()
      else:   
         print("\n   "+color.BOLD+"Screen resolution"+color.END)
         print("   Step 12")
         print("\n   Select a compatible booter screen resolution. \n   This resolution will apply to both the bootloader and\n   macOS, and can be changed later in OVMF Plaform Settings. If you\n   intend on using GPU passthrough, your GPU/monitor determines this."+color.END)
         print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
         if customValue == 1:
            cpydLog("info",str("Custom value requested, setting up"))
         #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<file>"+color.YELLOW+".img"+color.END+"\n   Enter a custom value.\n   \n   ")
            print(color.END+"\n      1. 800x600")
            print(color.END+"      2. 1024x768")
            print(color.BOLD+"      3. 1280x720 (720p)")
            print(color.END+"      4. 1280x1024")
            print(color.END+"      5. 1440x900")
            print(color.END+"      6. 1920x1080 (1080p)")
            print(color.END+"      7. 2560x1440 (1440p)")
            print(color.END+"      8. 3840x2160 (4K)\n")
            customInput = str(input(color.BOLD+"Select> "+color.END))
            
            if customInput == "1":
               customInput = "800x600"
            elif customInput == "2":
               customInput = "1024x768"
            elif customInput == "3":
               customInput = "1280x720"
            elif customInput == "4":
               customInput = "1280x1024"
            elif customInput == "5":
               customInput = "1440x900"
            elif customInput == "6":
               customInput = "1920x1080"
            elif customInput == "7":
               customInput = "2560x1440"
            elif customInput == "8":
               customInput = "3840x2160"
            else:
               customInput = "1280x720"

            USR_SCREEN_RES = customInput
            cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
            currentStage = currentStage + 1
            customValue = 0
            blob = open("./blobs/USR_SCREEN_RES.apb","w")
            blob.write(USR_SCREEN_RES)
            blob.close()
            stage13()
         else:
            print(color.BOLD+"\n      1. 1280x720")
            print(color.END+"      2. More resolutions...")
            print(color.END+"\n      B. Back")
            print(color.END+"      ?. Help")
            print(color.END+"      Q. Exit\n   ")
            stageSelect = str(input(color.BOLD+"Select> "+color.END))
         
            if stageSelect == "1":
               cpydLog("ok",str("Using default value of "+str(defaultValue)))
               USR_SCREEN_RES = "1280x720"
               blob = open("./blobs/USR_SCREEN_RES.apb","w")
               blob.write(USR_SCREEN_RES)
               blob.close()
               blob = open("./blobs/.cdn_control","w")
               blob.write("fresh_cdn")
               blob.close()
               currentStage = currentStage + 1
               stage13()

            elif stageSelect == "2":
               customValue = 1
               stage12()

            elif stageSelect == "b" or stageSelect == "B":
               currentStage = 1
               stage11()
               
            elif stageSelect == "?":
               clear()
               cpydLog("ok",("Contacting xdg-open with URL"))
               print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
               print("   Continue in your browser\n")
               print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
               os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#12-screen-resolution > /dev/null 2>&1')
               time.sleep(6)
               clear()
               stage12()

            elif stageSelect == "q" or stageSelect == "Q":
               exit   

            else:
               stage12()


   def stage11():
      global customValue
      global currentStage
      global USR_BOOT_FILE
      defaultValue = "BaseSystem.img"
      cpydLog("ok",str("Stage 11 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"macOS Recovery image file"+color.END)
      print("   Step 11")
      print("\n   Choose a bootable image file the virtual machine should boot to. \n   You need a macOS Recovery image (BaseSystem.img). You can either\n   select an existing one or the wizard can download one for you.\n   It must be in the *.img file format."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"NOTE:",color.END+color.BOLD+"This stage is optional. You can skip it if\n         you intend on using an existing HDD file."+color.END)
      if USR_TARGET_OS >= 100 and USR_TARGET_OS <= 1012:
         print(color.YELLOW+"\n     ⚠"+color.END+color.BOLD+"   Download flow disabled for legacy versions.\n         You must download an image manually."+color.END)

      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<file>"+color.YELLOW+".img"+color.END+"\n   Enter a custom value.\n   \n   ")
         print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+""+color.END+color.BOLD+"<file>"+color.YELLOW+".img"+color.END+"\n   Enter the full path to a bootable macOS Recovery image file.\n   It will be automatically copied into the root repo directory, or you\n   can place it there now and type \"BaseSystem.img\" without a path.\n   You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n      "+color.BOLD+"TIP:"+color.END,"You can drag and drop a file onto this window.\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))

         USR_BOOT_FILE = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_BOOT_FILE.apb","w")
         blob.write(USR_BOOT_FILE)
         blob.close()
         stage12()
      else:
         if USR_TARGET_OS >= 100 and USR_TARGET_OS <= 1012:
            print(color.END+color.GRAY+"\n      1. Download from Apple..."+color.END)
            print(color.BOLD+"      2. Select existing...")
         else:
            print(color.BOLD+"\n      1. Download from Apple...")
            print(color.END+"      2. Select existing...")
         print(color.END+"      3. Skip")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
         if stageSelect == "1" and USR_TARGET_OS >= 100 and USR_TARGET_OS <= 1012:
            stage11()
         elif stageSelect == "1":
            cpydLog("info","Arming download mechanism")
            USR_BOOT_FILE = "-1"
            blob = open("./blobs/USR_BOOT_FILE.apb","w")
            blob.write(USR_BOOT_FILE)
            
            blob.close()
            cpydLog("ok","Downloader armed, will be triggered by AP flow")
            blob = open("./blobs/.cdn_control","w")
            blob.write("fresh_cdn")
            blob.close()
            currentStage = currentStage + 1
            stage12()

         elif stageSelect == "2":
            
            customValue = 1
            stage11()

         elif stageSelect == "3":
            cpydLog("warn","No system image will be used in this session")
            USR_BOOT_FILE = "-2"
            blob = open("./blobs/USR_BOOT_FILE.apb","w")
            blob.write(USR_BOOT_FILE)
            blob.close()
            blob = open("./blobs/.cdn_control","w")
            blob.write("fresh_cdn")
            blob.close()
            currentStage = currentStage + 1
            stage12()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage10()
            
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#11-macos-recovery-image-file > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage11()

         elif stageSelect == "q" or stageSelect == "Q":
            exit   
         
         else:
            stage11()

   def stage10():
      global customValue
      global currentStage
      global USR_MAC_ADDRESS
      defaultValue = "00:16:cb:00:21:09"
      cpydLog("ok",str("Stage 10 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"Network MAC address"+color.END)
      print("   Step 10")
      print("\n   The network adapter needs a virtual MAC address. \n   The default is fine unless you intend on using features such\n   as iMessage and FaceTime, as these services require specific\n   MAC address values. In this case, you should use one\n   generated by this script or your own custom one."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<file>"+color.YELLOW+".img"+color.END+"\n   Enter a custom value.\n   \n   ")
         print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+""+color.END+color.BOLD+"XX"+color.YELLOW+":"+color.END+color.BOLD+"XX"+color.YELLOW+":"+color.END+color.BOLD+"XX"+color.YELLOW+":"+color.END+color.BOLD+"XX"+color.YELLOW+":"+color.END+color.BOLD+"XX"+color.YELLOW+":"+color.END+color.BOLD+"XX"+color.END+"\n   You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n      ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_MAC_ADDRESS = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_MAC_ADDRESS.apb","w")
         blob.write(USR_MAC_ADDRESS)
         blob.close()
         stage11()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Generate automatically")
         print(color.END+"      3. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_MAC_ADDRESS = "00:16:cb:00:21:09"
            blob = open("./blobs/USR_MAC_ADDRESS.apb","w")
            blob.write(USR_MAC_ADDRESS)
            blob.close()
            blob = open("./blobs/.cdn_control","w")
            blob.write("fresh_cdn")
            blob.close()
            currentStage = currentStage + 1
            stage11()

         elif stageSelect == "3":
            customValue = 1
            stage10()

         elif stageSelect == "2":
            cpydLog("info",str("Generating compatible MAC address"))
            macp1 = str(random.randint(10,50))
            macp2 = str(random.randint(10,50))
            USR_MAC_ADDRESS = str("00:16:cb:00:"+macp1+":"+macp2)
            cpydLog("ok",str("Generated MAC address with value "+USR_MAC_ADDRESS))
            cpydLog("info",str("Setting generated MAC address as live variable"))
            blob = open("./blobs/USR_MAC_ADDRESS.apb","w")
            blob.write(USR_MAC_ADDRESS)
            blob.close()
            blob = open("./blobs/.cdn_control","w")
            blob.write("fresh_cdn")
            blob.close()
            currentStage = currentStage + 1
            stage11()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage9()

         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#10-network-mac-address > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage10()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

         else:
            stage10()

   def stage9():
      global USR_NETWORK_DEVICE
      global customValue
      global currentStage
      global USR_TARGET_OS
      cpydLog("ok",str("Stage 9 sequence initiated"))
      if USR_TARGET_OS >= 100 and USR_TARGET_OS <= 1012:
         defaultValue = "e1000-82545em"
      else:
         defaultValue = "vmxnet3"

      clear()
      print("\n   "+color.BOLD+"Set network adapter model"+color.END)
      print("   Step 9")
      print("\n   Set the model of the virtual network adapter. \n   The default below has been selected based on your target OS,\n   so there shouldn't be a need to change it."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<model name>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+""+color.END+color.BOLD+"<model name>"+color.YELLOW+""+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_NETWORK_DEVICE = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_NETWORK_DEVICE.apb","w")
         blob.write(USR_NETWORK_DEVICE)
         blob.close()
         stage10()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_NETWORK_DEVICE = defaultValue
            blob = open("./blobs/USR_NETWORK_DEVICE.apb","w")
            blob.write(USR_NETWORK_DEVICE)
            blob.close()
            currentStage = currentStage + 1
            stage10()

         elif stageSelect == "2":
            customValue = 1
            stage9()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage8()
            
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#9-set-network-adapter-model > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage9()

         elif stageSelect == "q" or stageSelect == "Q":
            exit   

         else:
            stage9() 

   def stage8():
      global USR_HDD_SIZE
      global customValue
      global currentStage
      defaultValue = "80G"
      cpydLog("ok",str("Stage 8 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"Set hard disk capacity"+color.END)
      print("   Step 8")
      print("\n   Set the maximum virtual hard disk size (capacity). \n   Change this based on how much storage you think you'll need.\n   NOTE: The file will grow dynamically, and is not allocated in full."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
         print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+""+color.END+color.BOLD+"<number>"+color.YELLOW+"G"+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_HDD_SIZE = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_HDD_SIZE.apb","w")
         blob.write(USR_HDD_SIZE)
         blob.close()
         stage9()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_HDD_SIZE = defaultValue
            blob = open("./blobs/USR_HDD_SIZE.apb","w")
            blob.write(USR_HDD_SIZE)
            blob.close()
            currentStage = currentStage + 1
            stage9()

         elif stageSelect == "2":
            customValue = 1
            stage8()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage7()
            
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#8-set-hard-disk-capacity > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage8()

         elif stageSelect == "q" or stageSelect == "Q":
            exit   

         else:
            stage8()

   def stage7():
      global USR_ALLOCATED_RAM
      global customValue
      global currentStage
      defaultValue = "4G"
      cpydLog("ok",str("Stage 7 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"Set amount of allocated RAM"+color.END)
      print("   Step 7")
      print("\n   Set how much memory the guest can use. \n   As a general rule and for max performance, use no\n   more than half of your total host memory."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
         print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+""+color.END+color.BOLD+"<number>"+color.YELLOW+"G"+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_ALLOCATED_RAM = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))              #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_ALLOCATED_RAM.apb","w")
         blob.write(USR_ALLOCATED_RAM)
         blob.close()
         stage8()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_ALLOCATED_RAM = defaultValue
            blob = open("./blobs/USR_ALLOCATED_RAM.apb","w")
            blob.write(USR_ALLOCATED_RAM)
            blob.close()
            currentStage = currentStage + 1
            stage8()

         elif stageSelect == "2":
            customValue = 1
            stage7()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage6()
         
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#7-set-amount-of-allocated-ram > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage7()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit     

         else:
            stage7()

   def stage6():
      global USR_CPU_FEATURE_ARGS
      global customValue
      global currentStage
      defaultValue = "+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"
      cpydLog("ok",str("Stage 6 sequence initiated"))

      clear()
      print("\n   "+color.BOLD+"Set CPU feature arguments"+color.END)
      print("   Step 6")
      print("\n   Set the virtual CPU's feature arguments. \n   Do not change this unless you know what you're doing.\n   The default is more than enough for most people."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
         print(color.BOLD+color.PURPLE+"\n   FORMAT:",color.YELLOW+"+"+color.END+color.BOLD+"<arg>"+color.YELLOW+","+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_CPU_FEATURE_ARGS = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_FEATURE_ARGS.apb","w")
         blob.write(USR_CPU_FEATURE_ARGS)
         blob.close()
         stage7()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_CPU_FEATURE_ARGS = defaultValue
            blob = open("./blobs/USR_CPU_FEATURE_ARGS.apb","w")
            blob.write(USR_CPU_FEATURE_ARGS)
            blob.close()
            currentStage = currentStage + 1
            stage7()

         elif stageSelect == "2":
            customValue = 1
            stage6()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage5()
            
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#6-set-cpu-feature-arguments > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage6()

         elif stageSelect == "q" or stageSelect == "Q":
            exit    

         else:
            stage6()

   def stage5():
      global USR_CPU_MODEL
      global USR_TARGET_OS
      global customValue
      global currentStage
      if USR_TARGET_OS >= 1013:
         defaultValue = "Haswell-noTSX"
      else:
         defaultValue = "Penryn"
      cpydLog("ok",str("Stage 5 sequence initiated"))

      clear()
      print("\n   "+color.BOLD+"Set CPU model"+color.END)
      print("   Step 5")
      print("\n   Set the model of the virtual CPU. \n   Unless your host CPU is supported in macOS, leave this alone.\n   Use \"host\" to expose the host CPU model to the guest."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<model name>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_CPU_MODEL = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_MODEL.apb","w")
         blob.write(USR_CPU_MODEL)
         blob.close()
         stage6()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_CPU_MODEL = defaultValue
            blob = open("./blobs/USR_CPU_MODEL.apb","w")
            blob.write(USR_CPU_MODEL)
            blob.close()
            currentStage = currentStage + 1
            stage6()

         elif stageSelect == "2":
            customValue = 1
            stage5()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage4()

         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#5-set-cpu-model > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage5()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit    

         else:
            stage5()

   def stage4():
      global USR_CPU_THREADS
      global customValue
      global currentStage
      defaultValue = 2
      cpydLog("ok",str("Stage 4 sequence initiated"))

      clear()
      print("\n   "+color.BOLD+"Set number of CPU threads"+color.END)
      print("   Step 4")
      print("\n   Set the desired number of virtual CPU threads. \n   Like cores, more threads can dramatically improve guest performance if\n   your host can handle it."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         customInput = int(input(color.BOLD+"Value> "+color.END))
         USR_CPU_THREADS = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_THREADS.apb","w")
         blob.write(str(USR_CPU_THREADS))
         blob.close()
         stage5()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_CPU_THREADS = defaultValue
            blob = open("./blobs/USR_CPU_THREADS.apb","w")
            blob.write(str(USR_CPU_THREADS))
            blob.close()
            currentStage = currentStage + 1
            stage5()

         elif stageSelect == "2":
            customValue = 1
            stage4()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage3()
            
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#4-set-number-of-cpu-threads > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage4()

         elif stageSelect == "q" or stageSelect == "Q":
            exit

         else:
            stage4()

   def stage3():
      global USR_CPU_CORES
      global USR_TARGET_OS
      global USR_TARGET_OS_ID
      global USR_TARGET_OS_NAME
      global customValue
      global currentStage
      defaultValue = 2
      cpydLog("ok",str("Stage 3 sequence initiated"))

      if USR_TARGET_OS >= 11 and USR_TARGET_OS <= 99:
         USR_TARGET_OS = USR_TARGET_OS * 100

      USR_TARGET_OS_NAME = "N/A"
      if USR_TARGET_OS == 102:
         USR_TARGET_OS_NAME = "Jaguar"
      elif USR_TARGET_OS == 103:
         USR_TARGET_OS_NAME = "Panther"
      elif USR_TARGET_OS == 104:
         USR_TARGET_OS_NAME = "Tiger"
      elif USR_TARGET_OS == 105:
         USR_TARGET_OS_NAME = "Leopard"
      elif USR_TARGET_OS == 106:
         USR_TARGET_OS_NAME = "Snow Leopard"
      elif USR_TARGET_OS == 107:
         USR_TARGET_OS_NAME = "Lion"
      elif USR_TARGET_OS == 108:
         USR_TARGET_OS_NAME = "Mountain Lion"
      elif USR_TARGET_OS == 109:
         USR_TARGET_OS_NAME = "Mavericks"
      elif USR_TARGET_OS == 1010:
         USR_TARGET_OS_NAME = "Yosemite"
      elif USR_TARGET_OS == 1011:
         USR_TARGET_OS_NAME = "El Capitan"
      elif USR_TARGET_OS == 1012:
         USR_TARGET_OS_NAME = "Sierra"
      elif USR_TARGET_OS == 1013:
         USR_TARGET_OS_NAME = "High Sierra"
      elif USR_TARGET_OS == 1014:
         USR_TARGET_OS_NAME = "Mojave"
      elif USR_TARGET_OS == 1015:
         USR_TARGET_OS_NAME = "Catalina"
      elif USR_TARGET_OS == 1100:
         USR_TARGET_OS_NAME = "Big Sur"
      elif USR_TARGET_OS == 1200:
         USR_TARGET_OS_NAME = "Monterey"
      elif USR_TARGET_OS == 1300:
         USR_TARGET_OS_NAME = "Ventura"
      elif USR_TARGET_OS == 1400:
         USR_TARGET_OS_NAME = "Sonoma"

      blob = open("./blobs/USR_TARGET_OS_NAME.apb","w")
      blob.write(str(USR_TARGET_OS_NAME))
      blob.close()

      if USR_TARGET_OS == 1400:
         USR_TARGET_OS_ID = "sonoma"
      elif USR_TARGET_OS == 1300:
         USR_TARGET_OS_ID = "ventura"
      elif USR_TARGET_OS == 1200:
         USR_TARGET_OS_ID = "monterey"
      elif USR_TARGET_OS == 1100:
         USR_TARGET_OS_ID = "big-sur"
      elif USR_TARGET_OS == 1015:
         USR_TARGET_OS_ID = "catalina"
      elif USR_TARGET_OS == 1014:
         USR_TARGET_OS_ID = "mojave"
      elif USR_TARGET_OS == 1013:
         USR_TARGET_OS_ID = "high-sierra"
      elif USR_TARGET_OS == 109:
         USR_TARGET_OS_ID = "mavericks"

      clear()
      print("\n   "+color.BOLD+"Set number of CPU cores"+color.END)
      print("   Step 3")
      print("\n   Set the desired number of virtual CPU cores. \n   More cores can dramatically improve guest performance if\n   your host can handle it."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
      #   print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n   \n   ")
         customInput = int(input(color.BOLD+"Value> "+color.END))
         USR_CPU_CORES = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_CORES.apb","w")
         blob.write(str(USR_CPU_CORES))
         blob.close()
         stage4()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_CPU_CORES = defaultValue
            blob = open("./blobs/USR_CPU_CORES.apb","w")
            blob.write(str(USR_CPU_CORES))
            blob.close()
            currentStage = currentStage + 1
            stage4()

         elif stageSelect == "2":
            customValue = 1
            stage3()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage2()
         
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#3-set-number-of-cpu-cores > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage3()

         elif stageSelect == "q" or stageSelect == "Q":
            exit

         else:
            stage3()

   def stage2():
      global USR_TARGET_OS
      global customValue
      global currentStage
      defaultValue = 1015
      cpydLog("ok",str("Stage 2 sequence initiated"))
      clear()
      print("\n   "+color.BOLD+"Set target OS"+color.END)
      print("   Step 2")
      print("\n   This configures networking and image download version. \n   The most suitable network adapter will be automatically\n   selected for you based on this later."+color.END)
      print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,"Catalina (10.15)",color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.END+"\n      1. Sonoma (14)")
         print(color.END+"      2. Ventura (13)")
         print(color.END+"      3. Monterey (12)")
         print(color.END+"      4. Big Sur (11)")
         print(color.BOLD+"      5. Catalina (10.15)")
         print(color.END+"      6. Mojave (10.14)")
         print(color.END+"      7. High Sierra (10.13)\n")

         print(color.END+"      8. Legacy versions...\n")
         customInput = str(input(color.BOLD+"Select> "+color.END))
         
         if customInput == "1":
            customInput = 14
         elif customInput == "2":
            customInput = 13
         elif customInput == "3":
            customInput = 12
         elif customInput == "4":
            customInput = 11
         elif customInput == "5":
            customInput = 1015
         elif customInput == "6":
            customInput = 1014
         elif customInput == "7":
            customInput = 1013
         elif customInput == "8":
            customValue = 2
            stage2()
            

         else:
            customValue = 1
            stage2()

         USR_TARGET_OS = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = 3
         customValue = 0
         #if USR_TARGET_OS > 110 and USR_TARGET_OS < 999:
         #   USR_TARGET_OS = USR_TARGET_OS * 10
         blob = open("./blobs/USR_TARGET_OS.apb","w")
         blob.write(str(USR_TARGET_OS))
         blob.close()
         stage3()

      elif customValue == 2:
         cpydLog("info",str("Custom value requested, setting up"))
         print(color.END+"\n      1. Sierra (10.12)")
         print(color.END+"      2. El Capitan (10.11)")
         print(color.END+"      3. Yosemite (10.10)")
         print(color.END+"      4. Mavericks (10.9)")
         print(color.END+"      5. Mountain Lion (10.8)")
         print(color.END+"      6. Lion (10.7)\n")
         #print(color.END+"      7. Snow Leopard (10.6)")
         #print(color.END+"      8. Leopard (10.5)\n")
         customInput = str(input(color.BOLD+"Select> "+color.END))
         
         if customInput == "1":
            customInput = 1012
         elif customInput == "2":
            customInput = 1011
         elif customInput == "3":
            customInput = 1010
         elif customInput == "4":
            customInput = 109
         elif customInput == "5":
            customInput = 108
         elif customInput == "6":
            customInput = 107
         else:
            customInput = 1015
         USR_TARGET_OS = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = 3
         customValue = 0
         #if USR_TARGET_OS > 110 and USR_TARGET_OS < 999:
         #   USR_TARGET_OS = USR_TARGET_OS * 10
         blob = open("./blobs/USR_TARGET_OS.apb","w")
         blob.write(str(USR_TARGET_OS))
         blob.close()
         stage3()
      else:
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Select macOS version...")
         print(color.END+"\n      B. Back")
         print(color.END+"      ?. Help")
         print(color.END+"      Q. Exit\n   ")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_TARGET_OS = defaultValue
            blob = open("./blobs/USR_TARGET_OS.apb","w")
            blob.write(str(USR_TARGET_OS))
            blob.close()
            currentStage = 3
            stage3()

         elif stageSelect == "2":
            customValue = 1
            stage2()

         elif stageSelect == "b" or stageSelect == "B":
            currentStage = 1
            stage1()
         
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#2-set-target-os > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage2()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   
         
         else:
            stage2()

   #def stage2():
      #global USR_TARGET_OS
      #global customValue
      #global currentStage
      #defaultValue = 1015

      #clear()
      #print("\n   "+color.BOLD+"Set target OS"+color.END)
      #print("   Step 2")
      #print("\n   This configures networking and image download version. \n   The most suitable network adapter will be automatically\n   selected for you based on this later."+color.END)
      #print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      #if customValue == 1:
         #cpydLog("info",str("Custom value requested, setting up"))
         #print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\n   Enter a custom value.\n   \n   ")
         #customInput = int(input(color.BOLD+"Value> "+color.END))
         #USR_TARGET_OS = customInput
         #
         # cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         #currentStage = 3
         #customValue = 0
         ##if USR_TARGET_OS > 110 and USR_TARGET_OS < 999:
         ##   USR_TARGET_OS = USR_TARGET_OS * 10
         #blob = open("./blobs/USR_TARGET_OS.apb","w")
         #blob.write(str(USR_TARGET_OS))
         #blob.close()
         #stage3()
      #else:
      #   print(color.BOLD+"\n      1. Use default value")
      #   print(color.END+"      2. Custom value...")
      #   print(color.END+"      3. Back")
      #   print(color.END+"      ?. Help")
      #   print(color.END+"      Q. Exit\n   ")
      #   stageSelect = str(input(color.BOLD+"Select> "+color.END))
      #
      #   if stageSelect == "1":
            #cpydLog("ok",str("Using default value of "+str(defaultValue)))
      #      USR_TARGET_OS = defaultValue
      #      blob = open("./blobs/USR_TARGET_OS.apb","w")
      #      blob.write(str(USR_TARGET_OS))
      #      blob.close()
      #      currentStage = 3
      #      stage3()

      #   elif stageSelect == "2":
      #      customValue = 1
      #      stage2()

      #   elif stageSelect == "3":
      #      currentStage = 1
      #      stage1()
         
      #   elif stageSelect == "?":
      #      clear()
      #      print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
      #      print("   Continue in your browser\n")
      #      print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
      #      os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#2-set-target-os > /dev/null 2>&1')
      #      time.sleep(6)
      #      clear()
      #      stage2()
            
      #   elif stageSelect == "q" or stageSelect == "Q":
      #      exit   
         
      #   else:
      #      stage2()

   def stage1():
      global USR_CFG
      global customValue
      global currentStage
      cpydLog("ok",str("Stage 1 sequence initiated"))
      # remove stale blobs
      cpydLog("ok",str("Removing stale blobs"))
      os.system("mv -f ./blobs/*.apb ./blobs/stale/")
      os.system("mv -f /blobs/CDN_CONTROL ./blobs/stale/")
      defaultValue = "boot.sh"
      clear()

      print("\n   "+color.BOLD+"Name your config file"+color.END)
      print("   Step 1")
      print("\n   This is simply the name of your config file. \n   You can name it whatever you want. It's used to boot your\n   VM and will be the basis of this AutoPilot configuration."+color.END)
      if customValue == 1:
         cpydLog("info",str("Custom value requested, setting up"))
         print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+"boot.sh"+color.END)
         print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<filename>"+color.YELLOW+".sh"+color.END+"\n   Enter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         cpydLog("wait",("Waiting for user input"))
         customInput = str(input(color.BOLD+"Value> "+color.END))
         cpydLog("ok",("User input received"))
         USR_CFG = customInput
         cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
         currentStage = 2
         customValue = 0
         blob = open("./blobs/USR_CFG.apb","w")
         blob.write(USR_CFG)
         blob.close()
         stage2()

      else:
         print("\n   "+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+"boot.sh"+color.END)
         print(color.BOLD+"\n      1. Use default value")
         print(color.END+"      2. Custom value...")
         print(color.END+"\n      ?. Help")
         print(color.END+"      Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            cpydLog("ok",str("Using default value of "+str(defaultValue)))
            USR_CFG = "boot.sh"
            blob = open("./blobs/USR_CFG.apb","w")
            blob.write(USR_CFG)
            blob.close()
            currentStage = 2
            stage2()

         elif stageSelect == "2":
            customValue = 1
            stage1()
         
         elif stageSelect == "?":
            clear()
            cpydLog("ok",("Contacting xdg-open with URL"))
            print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING STAGE HELP PAGE IN DEFAULT BROWSER"+color.END,"")
            print("   Continue in your browser\n")
            print("\n   I have attempted to open this stage's help page in\n   your default browser. Please be patient.\n\n   You will be returned to the last screen in 5 seconds.\n\n\n\n\n")
            os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot#1-name-your-config-file > /dev/null 2>&1')
            time.sleep(6)
            clear()
            stage1()

         elif stageSelect == "q" or stageSelect == "Q":
            exit
         
         else:
            stage1()


   global PROC_PREPARE
   global PROC_CHECKBLOBS
   global PROC_GENCONFIG
   global PROC_LOCALCOPY
   global PROC_FETCHDL
   global PROC_GENHDD
   global PROC_APPLYPREFS
   global PROC_FIXPERMS
   global PROC_CLEANUP
   global startTime

   PROC_PREPARE = 0
   PROC_CHECKBLOBS = 0
   PROC_GENCONFIG = 0
   PROC_LOCALCOPY = -1
   PROC_FETCHDL = -1
   PROC_GENHDD = 0
   PROC_APPLYPREFS = 0
   PROC_FIXPERMS = 0
   PROC_CLEANUP = 0


   def handoff():
      global PROC_PREPARE
      global PROC_CHECKBLOBS
      global PROC_GENCONFIG
      global PROC_LOCALCOPY
      global PROC_FETCHDL
      global PROC_GENHDD
      global PROC_APPLYPREFS
      global PROC_FIXPERMS
      global PROC_CLEANUP
      global PROC_LOCALCOPY_CVTN 
      global PROC_GENXML
      global startTime

      startTime = 0

      PROC_PREPARE = 0
      PROC_CHECKBLOBS = 0
      PROC_GENCONFIG = 0
      PROC_LOCALCOPY = -1
      PROC_LOCALCOPY_CVTN = 0
      PROC_FETCHDL = -1
      PROC_GENHDD = 0
      PROC_APPLYPREFS = 0
      PROC_FIXPERMS = 0
      PROC_CLEANUP = 0
      PROC_GENXML = 0
      cpydLog("info",("Handoff started, user preferences saved"))
      cpydLog("ok",("───────────────── STARTING AUTOPILOT AUTOFLOW ─────────────────"))

      clear()
      time.sleep(2)

      startTime = timeit.default_timer()

      if USR_BOOT_FILE == "-1":
         PROC_FETCHDL = 0
         PROC_LOCALCOPY = -1
      elif USR_BOOT_FILE != "-2":
         PROC_FETCHDL = -1
         PROC_LOCALCOPY = 0

      def throwError():
         clear()
         cpydLog("error",(errorMessage))
         print("\n   "+color.BOLD+color.RED+"✖ FAILED"+color.END)
         print("   Unable to continue")
         print("\n   Sorry, something happened and AutoPilot cannot recover. \n   You may try again, or start over from the beginning.\n   If you think this was a bug, please report it on GitHub."+color.END)
         print("\n   "+color.BOLD+color.RED+"ERROR:",color.END+color.BOLD,errorMessage,color.END)
         print(color.BOLD+"\n      1. Try again")
         print(color.END+"      2. Start over")
         print(color.END+"      Q. Cancel and Quit\n")
         detectChoice = None
         stageSelectE = str(input(color.BOLD+"Select> "+color.END))
         clear()
         if stageSelectE == "1":
            time.sleep(2)
            handoff()

         elif stageSelectE == "2":
            os.system("./scripts/autopilot.py")

         elif stageSelectE == "q" or stageSelectE == "Q":
            exit

      def refreshStatusGUI():
         clear()
         cpydLog("ok",("Updating status UI"))
         print("   "+"\n   "+color.BOLD+"Status"+color.END)
         print("   "+"AutoPilot is performing the requested actions.")
         print("   "+"\n   This may take a few moments."+color.END)
         print("   "+"\n   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)

         if PROC_PREPARE == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Preparing files"+color.END)
         elif PROC_PREPARE == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Preparing files"+color.END)
         elif PROC_PREPARE == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Preparing files"+color.END)

         if PROC_CHECKBLOBS == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Checking preferences"+color.END)
         elif PROC_CHECKBLOBS == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Checking preferences"+color.END)
         elif PROC_CHECKBLOBS == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Checking preferences"+color.END)

         if PROC_GENCONFIG == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Generating config script"+color.END)
         elif PROC_GENCONFIG == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Generating config script"+color.END)
         elif PROC_GENCONFIG == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Generating config script"+color.END)
         
         if USR_CREATE_XML == "True":
            if PROC_GENXML == 0:
               print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Convert to domain XML file"+color.END)
            elif PROC_GENXML == 1:
               print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Convert to domain XML file"+color.END)
            elif PROC_GENXML == 2:
               print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Convert to domain XML file"+color.END)

         if PROC_LOCALCOPY == 0 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Copying recovery image into place"+color.END)
         elif PROC_LOCALCOPY == 1 and PROC_LOCALCOPY_CVTN == 0 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Copying recovery image into place"+color.END)
         elif PROC_LOCALCOPY == 1 and PROC_LOCALCOPY_CVTN == 1 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.END+"Copying recovery image into place"+color.END)
         elif PROC_LOCALCOPY == 2 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Copying recovery image into place"+color.END)

         if PROC_LOCALCOPY_CVTN == 1:
            print("      "+color.BOLD+"      ↳ "+"Converting image format"+color.END)
         

         if PROC_FETCHDL == 0 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Downloading recovery image"+color.END)
         elif PROC_FETCHDL == 1 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Downloading recovery image"+color.END)
         elif PROC_FETCHDL == 2 and USR_BOOT_FILE != "-2":
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Downloading recovery image"+color.END)

         if PROC_GENHDD == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Creating virtual hard disk"+color.END)
         elif PROC_GENHDD == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Creating virtual hard disk"+color.END)
         elif PROC_GENHDD == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Creating virtual hard disk"+color.END)
         elif PROC_GENHDD == 3:
            print("      "+color.BOLD+color.CYAN+"● ",color.END+color.END+"Creating virtual hard disk"+color.END)

         if PROC_APPLYPREFS == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Applying preferences"+color.END)
         elif PROC_APPLYPREFS == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Applying preferences"+color.END)
         elif PROC_APPLYPREFS == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Applying preferences"+color.END)

         if PROC_FIXPERMS == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Fixing up permissions"+color.END)
         elif PROC_FIXPERMS == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Fixing up permissions"+color.END)
         elif PROC_FIXPERMS == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Fixing up permissions"+color.END)

         if PROC_CLEANUP == 0:
            print("      "+color.BOLD+color.RED+"● ",color.END+color.END+"Cleaning up"+color.END)
         elif PROC_CLEANUP == 1:
            print("      "+color.BOLD+color.YELLOW+"● ",color.END+color.BOLD+"Cleaning up"+color.END)
         elif PROC_CLEANUP == 2:
            print("      "+color.BOLD+color.GREEN+"● ",color.END+color.END+"Cleaning up"+color.END)

         print("   "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
         if PROC_FETCHDL != 1:
            print("\n\n\n")

      refreshStatusGUI()
      time.sleep(3)

      def apcPrepare():    # PREPARE
         global PROC_PREPARE
         global USR_TARGET_OS
         global USR_SCREEN_RES
         PROC_PREPARE = 1
         cpydLog("info",("STARTING PREPARE PHASE"))
         global errorMessage
         errorMessage = "Couldn't prepare files. You may have insufficient\n           permissions or damaged files."
         refreshStatusGUI()
         cpydLog("info",("Setting up environment"))
         os.system("cp resources/baseConfig resources/config.sh")
         cpydLog("ok",("Copied baseConfig into live working file"))
         time.sleep(1)
         cpydLog("info",("Setting up OpenCore image"))
         if os.path.exists("boot/OpenCore.qcow2"):
            cpydLog("warn",("Existing OpenCore image found"))
            cpydLog("info",("Backing up existing image to ./boot/"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))))
            backupOCPath = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
            os.system("mkdir boot/"+backupOCPath)
            os.system("mv boot/*.qcow2 boot/"+backupOCPath+"/")
            os.system("mv boot/*.plist boot/"+backupOCPath+"/")
            os.system("mv boot/EFI boot/"+backupOCPath+"/EFI")
            cpydLog("ok",("Existing image backed up to ./boot/"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))))
            #os.system("rm -rf boot/EFI")
            time.sleep(2)
         cpydLog("info",("Selecting appropriate OpenCore image"))
         if USR_TARGET_OS <= 1015 and USR_TARGET_OS >= 1013:
            cpydLog("ok",("Selected OLD OpenCore image"))
            cpydLog("info",("Copying OpenCore image in place"))
            os.system("cp resources/oc_store/compat_old/OpenCore.qcow2 boot/OpenCore.qcow2")
            os.system("cp resources/oc_store/compat_old/config.plist boot/config.plist")
            os.system("cp -R resources/oc_store/compat_old/EFI boot/EFI")
            cpydLog("ok",("OpenCore image copied"))
         elif USR_TARGET_OS <= 1012 and USR_TARGET_OS >= 108:
            cpydLog("ok",("Selected NEW LEGACY OpenCore image"))
            cpydLog("info",("Copying OpenCore image in place"))
            os.system("cp resources/oc_store/legacy_new/OpenCore.qcow2 boot/OpenCore.qcow2")
            cpydLog("ok",("OpenCore image copied"))
         elif USR_TARGET_OS <= 1012 and USR_TARGET_OS <= 107:
            cpydLog("ok",("Selected OLD LEGACY OpenCore image"))
            cpydLog("info",("Copying OpenCore image in place"))
            os.system("cp resources/oc_store/legacy_old/OpenCore.qcow2 boot/OpenCore.qcow2")
            cpydLog("ok",("OpenCore image copied"))
         else:
            cpydLog("ok",("Selected NEW OpenCore image"))
            cpydLog("info",("Copying OpenCore image in place"))
            os.system("cp resources/oc_store/compat_new/OpenCore.qcow2 boot/OpenCore.qcow2")
            os.system("cp resources/oc_store/compat_new/config.plist boot/config.plist")
            os.system("cp -R resources/oc_store/compat_new/EFI boot/EFI")
            cpydLog("ok",("OpenCore image copied"))
         
         cpydLog("info",("Copying OVMF code into place"))
         os.system("cp resources/ovmf/OVMF_CODE.fd ovmf/OVMF_CODE.fd")
         os.system("cp resources/ovmf/OVMF_VARS.fd ovmf/OVMF_VARS.fd")
         cpydLog("info",("Copying OVMF vars for resolution "+str(USR_SCREEN_RES)))
         os.system("cp resources/ovmf/OVMF_VARS_"+USR_SCREEN_RES+".fd ovmf/OVMF_VARS.fd")
         cpydLog("ok",("OVMF files copied"))

         # NOW COPY A DUPLICATE TO LOCAL STORE FOR RESTORATION WITH SETTINGS PRESERVATION
         cpydLog("info",("Creating local OVMF variable store"))
         os.system("cp resources/ovmf/OVMF_VARS_"+USR_SCREEN_RES+".fd ovmf/user_store/OVMF_VARS.fd")
         
         cpydLog("info",("Performing integrity check"))
         integrityConfig = 1
         if os.path.exists("resources/config.sh"):
            integrityConfig = integrityConfig + 0
         else:
            integrityConfig = integrityConfig - 1
            cpydLog("error",("Integrity check FAILED for config file"))
            throwError()

         if os.path.exists("boot/OpenCore.qcow2"):
            integrityConfig = integrityConfig + 0
         else:
            integrityConfig = integrityConfig - 1
            cpydLog("error",("Integrity check FAILED for OpenCore image"))
            throwError()
         
         if os.path.exists("ovmf/OVMF_CODE.fd"):
            integrityConfig = integrityConfig + 0
         else:
            integrityConfig = integrityConfig - 1
            cpydLog("error",("Integrity check FAILED for OVMF"))
            throwError()
         cpydLog("ok",("Integrity check PASSED"))

         PROC_PREPARE = 2
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         refreshStatusGUI()

      def apcBlobCheck():  # CHECK BLOBS
         global PROC_CHECKBLOBS
         PROC_CHECKBLOBS = 1
         cpydLog("info",("STARTING INTEGRITY PHASE"))
         global errorMessage
         errorMessage = "The integrity of the wizard preference files\n           could not be verified."
         integrity = 1
         refreshStatusGUI()
         time.sleep(4)
         if os.path.exists("blobs/USR_ALLOCATED_RAM.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_ALLOCATED_RAM blob integrity failure"))
            #print("DEBUG: FOUND")
         if os.path.exists("blobs/USR_BOOT_FILE.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_BOOT_FILE blob integrity failure"))
         if os.path.exists("blobs/USR_CFG.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CFG blob integrity failure"))
         if os.path.exists("blobs/USR_CPU_CORES.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CPU_CORES blob integrity failure"))
         if os.path.exists("blobs/USR_CPU_FEATURE_ARGS.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CPU_FEATURE_ARGS blob integrity failure"))
         if os.path.exists("blobs/USR_CPU_MODEL.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CPU_MODEL blob integrity failure"))
         if os.path.exists("blobs/USR_CPU_THREADS.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CPU_THREADS blob integrity failure"))
         if os.path.exists("blobs/USR_HDD_SIZE.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_HDD_SIZE blob integrity failure"))
         if os.path.exists("blobs/USR_NETWORK_DEVICE.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_NETWORK_DEVICE blob integrity failure"))
         if os.path.exists("blobs/USR_TARGET_OS.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_TARGET_OS blob integrity failure"))
         if os.path.exists("blobs/USR_MAC_ADDRESS.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_MAC_ADDRESS blob integrity failure"))
         if os.path.exists("blobs/USR_SCREEN_RES.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_SCREEN_RES blob integrity failure"))
         if os.path.exists("blobs/USR_CREATE_XML.apb"):
            integrity = integrity + 0
         else:
            integrity = integrity - 1
            cpydLog("error",("USR_CREATE_XML blob integrity failure"))

         if integrity == 1:
            cpydLog("ok",("Integrity check PASSED"))
            
            PROC_CHECKBLOBS = 2
            cpydLog("ok",("Updated stage status, handing off to next stage"))
            refreshStatusGUI()
         else:
            cpydLog("fatal",("Integrity of work is damaged, killing flow"))
            throwError()

      def apcGenConfig():  # GENERATE CONFIG
         global PROC_GENCONFIG
         PROC_GENCONFIG = 1
         cpydLog("info",("STARTING GENERATION PHASE"))
         global PROC_GENXML
         global USR_CFG
         global customValue
         global customInput
         global errorMessage
         errorMessage = "The config file could not be written to.\n           You may have insufficient permissions."
         integrityCfg3 = 1
         
         def existingWarning():
            global USR_CFG
            global customValue
            global customInput
            cpydLog("warn",("Existing file with name "+str(USR_CFG)+" detected, asking the user"))
            clear()
            print("\n   "+color.BOLD+color.YELLOW+"⚠ PROBLEM DETECTED"+color.END)
            print("   Resolve the issue to continue")
            print("\n   This is not an error and can be resolved with your input. \n   You must select an option to continue. Once selected,\n   the process can continue from where it was left."+color.END)
            if customValue == 1:
               cpydLog("info",str("Custom value requested, setting up"))
               print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"A boot script with the name you selected exists."+color.END)
               print(color.BOLD+color.PURPLE+"\n   FORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<filename>"+color.YELLOW+".sh"+color.END+"\n   Enter a new file name. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
               cpydLog("wait",("Waiting for user input"))
               customInput = str(input(color.BOLD+"Value> "+color.END))
               cpydLog("ok",("User input received"))
               
               USR_CFG = customInput
               cpydLog("ok",str("Custom value was set to "+str(customInput)))               #+".sh" #<--- change required prefix/suffix
               currentStage = 2
               customValue = 0
               blob = open("./blobs/USR_CFG.apb","w")
               blob.write(USR_CFG)
               blob.close()
               apcGenConfig()

            else:
               print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"A boot script with the name you selected exists."+color.END)
               print(color.BOLD+"\n      1. Automatically rename existing file")
               print(color.END+"      2. Choose a new name")
               print(color.END+"      3. Overwrite")
               print(color.END+"      Q. Cancel and Quit\n")
               stageSelect = str(input(color.BOLD+"Select> "+color.END))
            
               if stageSelect == "1":
                  cpydLog("info",str("Renaming existing config file"))
                  os.system("mv ./"+USR_CFG+" ./"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"_"+USR_CFG)
                  
                  if os.path.exists("./"+USR_CFG_XML):
                     os.system("mv ./"+USR_CFG_XML+" ./"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"_"+USR_CFG_XML)
                  
                  apcGenConfig()

               elif stageSelect == "2":
                  customValue = 1
                  existingWarning()

               elif stageSelect == "3":
                  cpydLog("warn",("Overwriting "+str(USR_CFG)))
                  refreshStatusGUI() 

               elif stageSelect == "q" or stageSelect == "Q":
                  exit
                  exit
                  exit

         workdir = os.getcwd()
         cpydLog("info",("Working directory was captured as "+str(workdir)))

         refreshStatusGUI()
         cpydLog("info",("Scanning for file conflict"))
         time.sleep(4)
         if os.path.exists("./"+USR_CFG) or os.path.exists("./"+USR_CFG_XML):
            customInput = 0
            customValue = 0
            existingWarning()

         cpydLog("info",("Beginning variable injection"))
         with open("resources/config.sh","r") as file:
            configData = file.read()
         configData = configData.replace("$USR_CPU_SOCKS",str(USR_CPU_SOCKS))
         configData = configData.replace("$USR_CPU_CORES",str(USR_CPU_CORES))
         configData = configData.replace("$USR_CPU_THREADS",str(USR_CPU_TOTAL_F))
         configData = configData.replace("$USR_CPU_MODEL",str(USR_CPU_MODEL))
         configData = configData.replace("$USR_CPU_FEATURE_ARGS",str(USR_CPU_FEATURE_ARGS))
         configData = configData.replace("$USR_ALLOCATED_RAM",str(USR_ALLOCATED_RAM))
         configData = configData.replace("$USR_REPO_PATH",workdir)
         configData = configData.replace("$USR_NETWORK_DEVICE",str(USR_NETWORK_DEVICE))
         if USR_TARGET_OS >= 1013:
            configData = configData.replace("$USR_NAME","macOS "+str(USR_TARGET_OS_F))
            configData = configData.replace("$USR_ID","macOS")
         else:
            configData = configData.replace("$USR_NAME","Mac OS X "+str(USR_TARGET_OS_F))
            configData = configData.replace("$USR_ID","Mac OS X")
         configData = configData.replace("baseConfig",str(USR_CFG))
         configData = configData.replace("$USR_CFG",str(USR_CFG))
         configData = configData.replace("$USR_MAC_ADDRESS",str(USR_MAC_ADDRESS))
         configData = configData.replace("$USR_SCREEN_RES",str(USR_SCREEN_RES))
         cpydLog("ok",("Variable injection complete"))

         cpydLog("info",("Stamping with ULTMOS version"))
         configData = configData.replace("ULTMOS=0.0.0","ULTMOS="+str(version))
         cpydLog("ok",("Marked working script as using ULTMOS v"+str(version)))
         cpydLog("info",("Checking if Discord rich presence is available"))
         output_stream1 = os.popen("pip show pypresence")
         vfcPresence = output_stream1.read()
         if "Name: pypresence\n" in vfcPresence:
            vfcPresence = 1
            cpydLog("ok",("Discord rich presence is available, will enable in script"))
            configData = configData.replace("DISCORD_RPC=1","DISCORD_RPC=1")
         else:
            vfcPresence = 0
            cpydLog("warn",("Discord rich presence appears unavailable, will NOT enable in script"))
            configData = configData.replace("DISCORD_RPC=1","DISCORD_RPC=0")

         cpydLog("info",("Adding OS ID marker"))
         configData = configData.replace("$USR_OS_NAME",str(USR_TARGET_OS_NAME))


         cpydLog("info",("Setting up BaseSystem image attachment"))
         if USR_BOOT_FILE == "-2":
            cpydLog("warn",("Detaching BaseSystem from script, user skipped"))
            configData = configData.replace("-drive id=BaseSystem,if=none,file=\"$REPO_PATH/BaseSystem.img\",format=raw","#-drive id=BaseSystem,if=none,file=\"$REPO_PATH/BaseSystem.img\",format=raw")
            configData = configData.replace("-device ide-hd,bus=sata.4,drive=BaseSystem","#-device ide-hd,bus=sata.4,drive=BaseSystem")
         with open ("resources/config.sh","w") as file:
            cpydLog("info",("Writing changes"))
            file.write(configData)
            cpydLog("ok",("Changes written to file"))

         cpydLog("info",("Performing integrity check"))
         with open("resources/config.sh","r") as file:
            configDataTest = file.read()
         if "ALLOCATED_RAM=\""+str(USR_ALLOCATED_RAM) in configDataTest:
            integrityCfg3 = 0
         else:
            cpydLog("error",("Integrity check FAILED"))
            integrityCfg3 - 19
         cpydLog("ok",("Integrity check PASSED"))
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         refreshStatusGUI()
         PROC_GENCONFIG = 2
         time.sleep(1)

         


         # USE CONVERSION TOOL CODE TO GENERATE XML
         cpydLog("info",("Checking XML creation preferences"))
         if USR_CREATE_XML == "True":
            cpydLog("ok",("XML creation requested, WILL be generating XML"))
            PROC_GENXML = 1
            refreshStatusGUI()
            cpydLog("info",("Pointing XML conversion tool to live script"))
            apFilePath = "resources/config.sh"
            with open("./"+apFilePath,"r") as source:
               apFileS = source.read()
               apVars = (re.findall(r'"([^"]*)"', apFileS))
               apFilePathNoExt = apFilePath.replace(".sh","")
               cpydLog("info",("Preparing live working XML"))
            os.system("cp ./resources/baseDomain"+" ./"+apFilePathNoExt+".xml")
            cpydLog("ok",("Base XML ready for live working"))
            with open("./"+apFilePathNoExt+".xml","r") as file1:
                  cpydLog("info",("Parsing XML"))
                  cpydLog("warn",("XML conversion tool APC integration doesn't support blob caching yet"))
                  apFileM = file1.read()
                  apFileM = apFileM.replace("baseDomain",str(apFilePathNoExt+".xml"))
                  apFileM = apFileM.replace("#    THIS DOMAIN FILE SHOULD NOT BE EDITED BY THE USER!    #","    APC-RUN_"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"\n \n    THIS FILE WAS GENERATED USING AUTOPILOT.")
                  apFileM = apFileM.replace("#                                                          #\n","")
                  apFileM = apFileM.replace("	#    It is intended to be used by the XML import wizard.   #\n","")
                  apFileM = apFileM.replace("#    To use the wizard, run the included \"main.py\" file;   #\n","")
                  apFileM = apFileM.replace("#                                                          #"," ")
                  apFileM = apFileM.replace("#                       $ ./main.py                        #"," \n     To be used with virsh / virt-manager.")
                  apFileM = apFileM.replace("#    ./main.py","")
                  apFileM = apFileM.replace("############################################################."," ")

                  apVars[19] = "macOS "+apVars[19]

                  cpydLog("info",("Converting to XML format"))
                  apFileM = apFileM.replace("$USR_NAME",apVars[19]+"")
                  apFileM = apFileM.replace("$USR_UUID",str(uuid.uuid4()))

                  # CONVERT MEMORY TO VIRSH FORMAT
                  apMemCvt = apVars[5].replace("G","")
                  apMemCvt = int(apMemCvt)
                  apMemCvt = apMemCvt * 1048576

                  # GET WD
                  workdir = os.getcwd()

                  # CONVERT THREADS TO VIRSH FORMAT
                  apThreadsCvt = apVars[8]
                  apThreadsCvt = int(apThreadsCvt)
                  #apThreadsCvt = round(apThreadsCvt / 2)

                  # CONVERT VCPUS TO VIRSH FORMAT
                  apTotalCvt = apVars[7]
                  apTotalCvt = int(apTotalCvt)
                  apTotalCvt = round(apTotalCvt * apThreadsCvt)

                  # CONVERT OS VERSION TO VIRSH FORMAT
                  apOSCvt = apVars[2]
                  apOSCvt = apOSCvt.replace("macOS ","")
                  apOSCvt = apOSCvt.replace("Mac OS X ","")
                  apOSCvt = apOSCvt.replace(".","")

                  apFileM = apFileM.replace("$USR_MEMORY",str(apMemCvt))
                  apFileM = apFileM.replace("$USR_CPU_CORES",apVars[7])
                  apFileM = apFileM.replace("$USR_CPU_TOTAL",str(apTotalCvt))
                  apFileM = apFileM.replace("$USR_CPU_THREADS",str(apThreadsCvt))
                  apFileM = apFileM.replace("$USR_CPU_MODEL",apVars[9])
                  apFileM = apFileM.replace("$OVMF_DIR","ovmf")
                  apFileM = apFileM.replace("$REPO_DIR",workdir)
                  apFileM = apFileM.replace("$USR_CPU_ARGS",apVars[10])
                  apFileM = apFileM.replace("$USR_CPU_CORES",apVars[7])
                  apFileM = apFileM.replace("$USR_NETWORK_ADAPTER",apVars[17])
                  apFileM = apFileM.replace("$USR_MAC_ADDRESS",apVars[18])
                  apFileM = apFileM.replace("$USR_OS_VERSION",apOSCvt)
                  apFileM = apFileM.replace("$USR_OS_NAME",apVars[19])
                  apFileM = apFileM.replace("$USR_HEADER","Converted from "+str(apVars[3]))
                  apFileM = apFileM.replace("$REPO_VERSION",version)
                  apFileM = apFileM.replace("$XML_FILE",apVars[3].replace(".sh",".xml"))
                  apFileM = apFileM.replace("$AP_FILE",apVars[3])
                  apFileM = apFileM.replace("$AP_RUNTIME",str(datetime.today().strftime('%H:%M:%S %d/%m/%Y')))
                  apFileM = apFileM.replace("$AP_FLOW","Yes")
                  apFileM = apFileM.replace("$AP_AUTO","N/A")
                  apFileM = apFileM.replace("$AP_BLOB","N/A")
                  
                  cpydLog("ok",("Converted to XML structure"))
            # apFileM = apFileM.replace("$USR_",apVars[])
            
            file1.close
            cpydLog("info",("Writing changes"))
            with open("./"+apFilePathNoExt+".xml","w") as file:
                  file.write(apFileM)
                  cpydLog("ok",("Changes written to file"))
            time.sleep(2)
            cpydLog("ok",("Updated stage status, handing off to next stage"))
            PROC_GENXML = 2
            refreshStatusGUI()
            time.sleep(3)
         else:
            cpydLog("ok",("XML creation skipped by user, ignoring"))
            cpydLog("ok",("Updated stage status, handing off to next stage"))


      def apcFetchDL():  # FETCH RECOVERY ONLINE
         global PROC_FETCHDL
         global USR_TARGET_OS_F
         global USR_TARGET_OS_ID
         cpydLog("info",("STARTING REMOTE RECOVERY PHASE"))
         

         PROC_FETCHDL = 1
         global errorMessage
         errorMessage = "The download script could not be executed.\n           You may have insufficient permissions or damaged files."
         integrityImg = 1
         refreshStatusGUI()
         time.sleep(2)
         cpydLog("info",("Setting target OS to "+str(USR_TARGET_OS)))
         print(color.BOLD+"   Downloading macOS",str(USR_TARGET_OS_F)+"...")
         if len(USR_TARGET_OS_ID) > 1:
            cpydLog("ok",("OS ID is valid, sending to dlosx script"))
            os.system("./scripts/dlosx-arg.py -s "+USR_TARGET_OS_ID)
         else:
            cpydLog("warn",("OS ID is NOT valid, running dlosx without passthrough"))
            os.system("./scripts/dlosx.py")
         #subprocess.Popen(cmd).wait()
         #print(os.path.getsize("./BaseSystem.img"))
         cpydLog("info",("Checking BaseSystem with a size of "+str(os.path.getsize("./BaseSystem.img"))))
         if os.path.exists("./BaseSystem.img") and os.path.getsize("./BaseSystem.img") > 2401920:
            integrityImg = 1
            cpydLog("ok",("Integrity check PASSED"))
         else:
            integrityImg = 0
            cpydLog("error",("Integrity check FAILED"))
            errorMessage = "The image download failed.\n           Please check your internet connection."
            throwError()
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         PROC_FETCHDL = 2
         refreshStatusGUI()
         time.sleep(3)

      def apcLocalCopy():  # FETCH RECOVERY LOCALLY
         global PROC_LOCALCOPY
         global PROC_LOCALCOPY_CVTN
         PROC_LOCALCOPY = 1
         PROC_LOCALCOPY_CVTN = 0
         cpydLog("info",("STARTING LOCAL RECOVERY PHASE"))
         global errorMessage
         errorMessage = "The local recovery image could not be found,\n           or it cannot be accessed."
         integrityImg = 1
         refreshStatusGUI()
         time.sleep(2)
         cpydLog("info",("Copying "+str(USR_BOOT_FILE)+" to repository directory"))
         os.system("cp "+USR_BOOT_FILE+" ./")
         cpydLog("info",("Setting up file name"))
         os.system("mv ./*.dmg BaseSystem.dmg")
         os.system("mv ./*.img BaseSystem.img")

         if os.path.exists("./BaseSystem.dmg"):
            cpydLog("warn",("BaseSystem image is still in the DMG format, will convert now"))
            PROC_LOCALCOPY_CVTN = 1
            refreshStatusGUI()
            time.sleep(1)
            os.system("resources/dmg2img ./BaseSystem.dmg > /dev/null 2>&1")
            cpydLog("info",("Finished converting, removing source DMG"))
            os.system("rm ./BaseSystem.dmg")
            time.sleep(1)
            cpydLog("ok",("Updated subphase status, returning to parent"))
            PROC_LOCALCOPY_CVTN = 0
            refreshStatusGUI()
            time.sleep(1)

         cpydLog("info",("Performing integrity check"))
         if os.path.exists("./BaseSystem.img"):
            integrityImg = 1
            cpydLog("ok",("Integrity check PASSED"))
         else:
            integrityImg = 0
            cpydLog("error",("Integrity check FAILED"))
            throwError()
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         PROC_LOCALCOPY = 2
         refreshStatusGUI()
         time.sleep(3)



         

      def apcGenHDD():  # CREATE VIRTUAL HARD DISK FILE
         global PROC_GENHDD
         global USR_HDD_SIZE
         global USR_HDD_SIZE_B
         PROC_GENHDD = 1
         cpydLog("info",("STARTING HARDDISK PHASE"))
         global errorMessage
         errorMessage = "The virtual hard disk file could not be created.\n           You may have insufficient permissions."
         integrityImg = 1
         refreshStatusGUI()
         time.sleep(2)
         cpydLog("info",("Scanning for file conflict"))
         def existingWarning1():
            clear()
            cpydLog("warn",("Existing file with name HDD.qcow2 detected, asking the user"))
            print("\n   "+color.BOLD+color.YELLOW+"⚠ PROBLEM DETECTED"+color.END)
            print("   Resolve the issue to continue")
            print("\n   This is not an error and can be resolved with your input. \n   You must select an option to continue. Once selected,\n   the process can continue from where it was left."+color.END)
            print("\n   "+color.BOLD+color.YELLOW+"PROBLEM:",color.END+"A virtual hard disk with the name \"HDD.qcow2\" already exists."+color.END)
            print(color.BOLD+"\n      1. Automatically rename existing file")
            print(color.END+"      2. Use existing file")
            print(color.END+color.RED+"      X. Delete"+color.END)
            print(color.END+"      Q. Cancel and Quit\n")
            cpydLog("wait",("Waiting for user input"))
            stageSelect = str(input(color.BOLD+"Select> "+color.END))
            cpydLog("ok",("User input received"))
            if stageSelect == "1":
               #cpydLog("ok",str("Using default value of "+str(defaultValue)))
               global PROC_GENHDD
               cpydLog("ok",("Moving HDD.qcow2"+" to "+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"_HDD.qcow2"))
               os.system("mv ./HDD.qcow2"+" ./"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"_HDD.qcow2")
               PROC_GENHDD = 2
               cpydLog("ok",("Resetting phase status and re-sparking"))
               apcGenHDD()

            elif stageSelect == "2":
               cpydLog("ok",("Using existing hard disk file"))
               PROC_GENHDD = 3
               refreshStatusGUI() 

            elif stageSelect == "x" or stageSelect == "X":
               cpydLog("warn",("Deleting HDD.qcow2"))
               os.system("rm HDD.qcow2")
               PROC_GENHDD = 2
               apcGenHDD()

            elif stageSelect == "q" or stageSelect == "Q":
               cpydLog("fatal",("User quit"))
               exit

         USR_HDD_SIZE_B = int(USR_HDD_SIZE.replace("G","")) * 1000000000 + 209756160



         if os.path.exists("./HDD.qcow2"):
            existingWarning1()
         else:
            cpydLog("info",("Generating hard disk image file"))
            os.system("qemu-img create -f qcow2 HDD.qcow2 "+str(USR_HDD_SIZE_B)+"B > /dev/null 2>&1")
            time.sleep(3)
            PROC_GENHDD = 2

         # Hard disk creation error catcher - thanks Cyber!
         if not os.path.exists("./HDD.qcow2"):
            cpydLog("error",("Hard disk image file generation failed"))
            errorMessage = "The virtual hard disk file could not be created.\n           Did you install QEMU + tools?"
            throwError()
         else:
            cpydLog("ok",("Hard disk image file generation verified"))
            PROC_GENHDD = 2
         
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         refreshStatusGUI()
         time.sleep(2)

      def apcApplyPrefs():  # APPLY USER PREFERENCES
         global PROC_APPLYPREFS
         global USR_CFG
         PROC_APPLYPREFS = 1
         cpydLog("info",("STARTING APPLY PHASE"))
         global errorMessage
         errorMessage = "Could not apply preferences to generated files.\n           You may have insufficient permissions."
         integrityImg = 1
         refreshStatusGUI()
         time.sleep(2)
         
         if os.path.exists("resources/config.sh"):
            cpydLog("ok",("Integrity check PASSED"))
            integrityImg = 1
         else:
            cpydLog("error",("Integrity check FAILED"))
            integrityImg = 0
            throwError()
         

         with open("resources/config.sh","r") as file:
            cpydLog("info",("Dumping contents of baseConfig to memory"))
            configData = file.read()
         cpydLog("info",("Stripping warning headers"))
         configData = configData.replace("baseConfig",str(USR_NAME))
         configData = configData.replace("#    THIS CONFIG FILE SHOULD NOT BE EDITED BY THE USER!    #","#   APC-RUN_"+str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))+"\n#\n#   THIS FILE WAS GENERATED USING AUTOPILOT.")
         configData = configData.replace("#                                                          #\n","")
         configData = configData.replace("# It is intended to be used by the automatic setup wizard. #\n","")
         configData = configData.replace("#    To use the wizard, run the included \"main.py\" file;   #\n","")
         configData = configData.replace("#                                                          #","#")
         configData = configData.replace("#                       $ ./main.py                        #","#\n#   To boot this script, run the following command:\n#   $ ./"+str(USR_CFG))
         configData = configData.replace("#    ./main.py","")
         configData = configData.replace("############################################################.","#")
         cpydLog("info",("Generating epoch timestamp"))
         configData = configData.replace("GEN_EPOCH=000000000","GEN_EPOCH="+str(int(time.time())))
         cpydLog("ok",("Epoch timestamped as "+str(int(time.time()))))
         with open ("resources/config.sh","w") as file:
            cpydLog("info",("Writing to file"))
            file.write(configData)

         with open("resources/config.sh","r") as file:
            configDataTest = file.read()
         if "#   THIS FILE WAS GENERATED USING AUTOPILOT." in configDataTest:
            integrityImg + 0
            cpydLog("ok",("Header verification complete"))
         else:
            integrityImg - 1
            cpydLog("error",("Header verification failed"))
            throwError()

         cpydLog("info",("Moving working file into place"))
         os.system("mv resources/config.sh ./"+USR_CFG)
         

         if USR_CREATE_XML == "True":
            os.system("mv resources/config.xml ./"+USR_CFG_XML)
            if os.path.exists("./"+USR_CFG_XML):
               integrityImg = 1
            else:
               integrityImg = 0
               throwError()
         
         if os.path.exists("./"+USR_CFG):
            cpydLog("ok",("Moved working file into "+USR_CFG+" successfully"))
            integrityImg = 1
         else:
            cpydLog("error",("Could not move working file into "+USR_CFG))
            integrityImg = 0
            throwError()
         
         PROC_APPLYPREFS = 2
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         refreshStatusGUI()
         time.sleep(2)
      
      def apcFixPerms():  # FIX PERMISSIONS
         global PROC_FIXPERMS
         global USR_CFG
         PROC_FIXPERMS = 1
         cpydLog("info",("STARTING PERMISSIONS PHASE"))
         global errorMessage
         errorMessage = "Could not set permissions on generated files.\n           You can attempt to do this manually."
         integrityImg = 1
         refreshStatusGUI()
         time.sleep(2)
         cpydLog("info",("Setting execute permissions"))
         os.system("chmod +x ./"+USR_CFG)
         cpydLog("info",("Setting readwrite permissions"))
         os.system("chmod +rw ./BaseSystem.img")
         cpydLog("ok",("Permissons set for new user files"))
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         PROC_FIXPERMS = 2
         refreshStatusGUI()
         time.sleep(2)
         
      def apcCleanUp():  # CLEAN BLOBS AND TEMP
         global PROC_CLEANUP
         global USR_CFG
         global errorMessage
         PROC_CLEANUP = 1
         refreshStatusGUI()
         cpydLog("info",("STARTING CLEANUP PHASE"))
         time.sleep(1)

         cpydLog("info",("Copying current session blobs into user backdir"))
         os.system("cp blobs/*.apb blobs/user/")
         cpydLog("info",("Marking blobs as stale"))
         cpydLog("info",("Moving blobs into stale folder"))
         os.system("mv blobs/*.apb blobs/stale/")
         cpydLog("ok",("Blob cleanup complete"))
         cpydLog("ok",("Updated stage status, handing off to next stage"))
         PROC_CLEANUP = 2
         refreshStatusGUI()
         time.sleep(1)

      apcPrepare()
      apcBlobCheck()
      apcGenConfig()
      if PROC_FETCHDL == 0 and USR_BOOT_FILE != "-2":
         cpydLog("ok",("User requested a new macOS recovery image, arming downloader"))
         apcFetchDL()
      elif PROC_LOCALCOPY == 0 and USR_BOOT_FILE != "-2":
         cpydLog("ok",("User is using their own macOS recovery image, disarming downloader"))
         cpydLog("ok",("Switching to local copy mode"))
         apcLocalCopy()
      apcGenHDD()
      apcApplyPrefs()
      apcFixPerms()
      apcCleanUp()
      cpydLog("info",("Stopping timer"))
      stopTime = timeit.default_timer()
      time.sleep(3)
      

      cpydLog("info",("Updating variable definition"))
      global USR_CPU_SOCKS
      global USR_CPU_CORES
      global USR_CPU_THREADS
      global USR_CPU_MODEL
      global USR_CPU_FEATURE_ARGS
      global USR_ALLOCATED_RAM
      global USR_REPO_PATH
      global USR_NETWORK_DEVICE
      global USR_ID
      global USR_NAME
      global USR_CFG
      global USR_TARGET_OS
      global USR_HDD_SIZE
      global USR_TARGET_OS_F
      global USR_CPU_TOTAL_F
      global USR_CFG_XML
      global USR_CREATE_XML
      global customValue

      exTime = round(stopTime - startTime)
      cpydLog("ok",("Timer was stopped with a recorded time of "+str(exTime)+" seconds in live mode"))
      clear()
      cpydLog("ok",("AutoPilot stages complete, displaying user summary screen"))
      cpydLog("ok",("───────────────── AUTOPILOT COMPLETE! SESSION TIME WAS "+str(exTime)+" SEC ─────────────────"))
      print("   "+"\n   "+color.BOLD+color.GREEN+"✔ SUCCESS"+color.END)
      print("   "+"All processes finished successfully")
      if USR_CREATE_XML != "True": print("   "+"\n   Your customised boot file is now ready.\n   You can now start using macOS."+color.END)
      else: print("   "+"\n   Your customised files are now ready.\n   You can now start using macOS."+color.END)
      print("   "+"\n   "+color.BOLD+"────────────────────────────────────────────",color.END)
      if USR_CREATE_XML == "True": print("   "+color.BOLD+color.PURPLE+"FILES    ",color.END+color.END+USR_CFG+color.END+", "+USR_CFG_XML)
      else: print("   "+color.BOLD+color.PURPLE+"FILE     ",color.END+color.END+USR_CFG+color.END)
      print("   "+color.BOLD+color.RED+"COMMAND  ",color.END+color.END+"$ ./"+USR_CFG,color.END)
      print("   "+color.BOLD+color.CYAN+"TIME    ",color.END+color.END,str(exTime),"seconds",color.END+"")
      print("   "+color.BOLD+"────────────────────────────────────────────",color.END)
      print("   "+color.BOLD+"\n   Created by Coopydood"+color.END)
      print("   "+"Helpful? Consider supporting the project on GitHub! <3"+color.END)
      
      if USR_CREATE_XML == "True":
         cpydLog("info",("XML generation was part of AP flow, offering import experience"))
         print(color.BOLD+"\n      1. Import XML...")
         print(color.END+"         Import the",USR_CFG_XML,"file into virsh.\n")
         print("    "+color.END+"  2. Boot")
         print("    "+color.END+"  3. Main menu")
      else:
         cpydLog("info",("XML generation was not included in AP flow, offering direct boot"))
         print(color.BOLD+"\n      1. Boot")
         print(color.END+"         Run your",USR_CFG,"file now.\n")
         print("    "+color.END+"  2. Open in default editor")
         print("    "+color.END+"  3. Main menu")
      print("    "+color.END+"  Q. Exit\n")
      cpydLog("wait",("Waiting for user input"))
      stageSelect = str(input(color.BOLD+"Select> "+color.END))
      cpydLog("ok",("User input received"))
      customValue = 0
      if USR_CREATE_XML == "True":
         if stageSelect == "1":
            cpydLog("info",("Handing off to XML importer experience flow"))
            #cpydLog("ok",str("Using default value of "+str(defaultValue)))
            clear()
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            
            os.system("./scripts/extras/xml-convert.py --import "+USR_CFG_XML)
         
         elif stageSelect == "2":
            cpydLog("info",("Handing off to QEMU; booting "+USR_CFG))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            os.system("./"+USR_CFG)

         elif stageSelect == "3":
            cpydLog("info",("Returning to main menu"))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            os.system("./main.py")

         elif stageSelect == "q" or stageSelect == "Q":
            cpydLog("fatal",("User quit"))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            exit

      else:
         if stageSelect == "1":
            #cpydLog("ok",str("Using default value of "+str(defaultValue)))
            clear()
            cpydLog("info",("Handing off to QEMU; booting "+USR_CFG))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            os.system("./"+USR_CFG)
           
         
         elif stageSelect == "2":
            cpydLog("info",("Attempting to open "+USR_CFG+"; contacting xdg-open"))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            os.system("xdg-open ./"+USR_CFG)
            

         elif stageSelect == "3":
            cpydLog("info",("Returning to main menu"))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            os.system("./main.py")

         elif stageSelect == "q" or stageSelect == "Q":
            cpydLog("fatal",("User quit"))
            cpydLog("fatal",("Bye"))
            cpydLog("fatal","───────────────── END OF LOGFILE ─────────────────")
            exit

            


   stage1()

if detectChoice == "1":
   cpydLog("ok",("───────────────── STARTING INTERROGATION SEQUENCE ─────────────────"))
   autopilot()
elif detectChoice == "?":
   cpydLog("info",("Attempting to contact xdg-open with URL"))
   clear()
   print("\n\n   "+color.BOLD+color.GREEN+"✔  OPENING AUTOPILOT HELP IN DEFAULT BROWSER"+color.END,"")
   print("   Continue in your browser\n")
   print("\n   I have attempted to open the AutoPilot help in\n   your default browser. Please be patient.\n\n   You will be returned to AutoPilot in 5 seconds.\n\n\n\n\n")
   os.system('xdg-open https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot > /dev/null 2>&1')
   time.sleep(6)
   clear()
   cpydLog("ok",("Returning to AP menu"))
   os.system('./scripts/autopilot.py')
elif detectChoice == "2":
    cpydLog("info",("Returning to main menu"))
    os.system('./main.py')

elif detectChoice == "q" or detectChoice == "Q":
    cpydLog("fatal",("User quit"))
    exit
else:
   cpydLog("warn",("Nothing caught, using default startup"))
   startup()