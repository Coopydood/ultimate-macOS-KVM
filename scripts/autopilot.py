#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# AUTOPILOT BY COOPYDOOD

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

#parser = argparse.ArgumentParser("gpu-check")
#parser.add_argument("-a", "--auto", dest="auto", help="Detect GPU(s) automatically",action="store_true")
#parser.add_argument("-m", "--manual", dest="manual", help="Enter GPU model manually", metavar="<model>", type=str)
#parser.add_argument("-f", "--force", dest="forceModel", metavar="<model>", help="Override auto-detected GPU with a custom model. Pretty useless, mostly for debugging.", type=str)

#args = parser.parse_args()

detectChoice = 1
latestOSName = "Ventura"
latestOSVer = "13"
runs = 0

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

def startup():
    global detectChoice
    print("\n\nWelcome to"+color.BOLD+color.PURPLE,"AutoPilot"+color.END,"(BETA)")
    print("Created by",color.BOLD+"Coopydood\n"+color.END)
    print("\nThe purpose of this script is to automatically guide you through \nthe process of",color.BOLD+"creating and running a basic macOS VM",color.END+"using settings \nbased on answers to a number of questions. \n\nMany of the values can be left to default - especially if you are unsure.\nIt won't be perfect, but it's supposed to make it as"+color.BOLD,"easy as possible.\n"+color.END)
    print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-macOS-KVM")
    print("\nContinue whenever you're ready, or return to the main menu.")
    print(color.BOLD+"\n   1. Start")
    print(color.END+"      Begin creating a new QEMU-based macOS config file \n")
    print(color.END+"   2. Main menu")
    print(color.END+"   3. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

def clear(): print("\n" * 150)

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
   
   global currentStage
   currentStage = 1
   
   global customValue
   customValue = 0

   def generate():
      print(color.BOLD+color.PURPLE+"Not implemented yet! I'm working on it- I swear!\n"+color.END)

   def stage10():
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

      USR_ALLOCATED_RAM_F = USR_ALLOCATED_RAM.replace("G","")
      USR_HDD_SIZE_F = USR_HDD_SIZE.replace("G","")
      USR_CPU_TOTAL = USR_CPU_CORES * USR_CPU_THREADS
      USR_CPU_TOTAL_F = str(USR_CPU_TOTAL)

      USR_TARGET_OS_F = USR_TARGET_OS / 100

      clear()
      print("    "+"\n    "+color.BOLD+"Generate config file"+color.END)
      print("    "+"Review your preferences")
      print("    "+"\n    The config wizard is complete.\n    You should review your preferences below and make sure\n    they are satisfactory. When ready, generate the config."+color.END)
      print("    "+"\n    "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
      print("    "+color.BOLD+color.PURPLE+"FILE    ",color.END+color.BOLD+USR_CFG+color.END)
      print("    "+color.BOLD+color.GREEN+"OS      ",color.END+color.BOLD+"macOS",USR_TARGET_OS_F,color.END)
      print("    "+color.BOLD+color.CYAN+"CPU     ",color.END+color.BOLD+USR_CPU_MODEL+",",USR_CPU_CORES,"cores,",USR_CPU_THREADS,"threads","("+USR_CPU_TOTAL_F+")"+color.END)
      print("    "+color.BOLD+color.CYAN+"        ",color.END+color.BOLD+USR_CPU_FEATURE_ARGS+color.END)
      print("    "+color.BOLD+color.CYAN+"RAM     ",color.END+color.BOLD+USR_ALLOCATED_RAM_F+" GB"+color.END)
      print("    "+color.BOLD+color.CYAN+"DISK    ",color.END+color.BOLD+USR_HDD_SIZE_F+" GB (dynamic)"+color.END)
      print("    "+color.BOLD+color.CYAN+"NETWORK ",color.END+color.BOLD+USR_NETWORK_DEVICE+color.END+"")
      print("    "+color.BOLD+"──────────────────────────────────────────────────────────────",color.END)
      print(color.BOLD+"\n       1. Generate!")
      print("    "+color.END+"   2. Back")
      print("    "+color.END+"   X. Start Over")
      print("    "+color.END+"   Q. Exit\n")
      stageSelect = str(input(color.BOLD+"Select> "+color.END))
   
      if stageSelect == "1":
         generate()

      elif stageSelect == "2":
         stage9()

      elif stageSelect == "x" or stageSelect == "X":
         currentStage = 1
         stage1()
         
      elif stageSelect == "q" or stageSelect == "Q":
         exit   

   def stage9():
      global USR_NETWORK_DEVICE
      global customValue
      global currentStage
      global USR_TARGET_OS

      if USR_TARGET_OS >= 1014:
         defaultValue = "e1000-82545em"
      else:
         defaultValue = "vmxnet3"

      clear()
      print("\n"+color.BOLD+"Set network adapter model"+color.END)
      print("Step 9")
      print("\nSet the model of the virtual network adapter. \nThe default below has been selected based on your target OS,\nso there shouldn't be a need to change it."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<model name>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:",color.YELLOW+""+color.END+color.BOLD+"<model name>"+color.YELLOW+""+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_NETWORK_DEVICE = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_NETWORK_DEVICE","w")
         blob.write(USR_NETWORK_DEVICE)
         blob.close()
         stage10()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_NETWORK_DEVICE = defaultValue
            blob = open("./blobs/USR_NETWORK_DEVICE","w")
            blob.write(USR_NETWORK_DEVICE)
            blob.close()
            currentStage = currentStage + 1
            stage10()

         elif stageSelect == "2":
            customValue = 1
            stage9()

         elif stageSelect == "3":
            currentStage = 1
            stage8()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage8():
      global USR_HDD_SIZE
      global customValue
      global currentStage
      defaultValue = "80G"

      clear()
      print("\n"+color.BOLD+"Set hard disk capacity"+color.END)
      print("Step 8")
      print("\nSet the maximum virtual hard disk size (capacity). \nChange this based on how much storage you think you'll need.\nNOTE: The file will grow dynamically, and is not allocated in full."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
         print(color.BOLD+color.PURPLE+"\nFORMAT:",color.YELLOW+""+color.END+color.BOLD+"<number>"+color.YELLOW+"G"+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_HDD_SIZE = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_HDD_SIZE","w")
         blob.write(USR_HDD_SIZE)
         blob.close()
         stage9()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_HDD_SIZE = defaultValue
            blob = open("./blobs/USR_HDD_SIZE","w")
            blob.write(USR_HDD_SIZE)
            blob.close()
            currentStage = currentStage + 1
            stage9()

         elif stageSelect == "2":
            customValue = 1
            stage8()

         elif stageSelect == "3":
            currentStage = 1
            stage7()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage7():
      global USR_ALLOCATED_RAM
      global customValue
      global currentStage
      defaultValue = "4G"

      clear()
      print("\n"+color.BOLD+"Set amount of allocated RAM"+color.END)
      print("Step 7")
      print("\nSet how much memory the guest can use. \nAs a general rule and for max performance, use no\nmore than half of your total host memory."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
         print(color.BOLD+color.PURPLE+"\nFORMAT:",color.YELLOW+""+color.END+color.BOLD+"<number>"+color.YELLOW+"G"+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_ALLOCATED_RAM = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_ALLOCATED_RAM","w")
         blob.write(USR_ALLOCATED_RAM)
         blob.close()
         stage8()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_ALLOCATED_RAM = defaultValue
            blob = open("./blobs/USR_ALLOCATED_RAM","w")
            blob.write(USR_ALLOCATED_RAM)
            blob.close()
            currentStage = currentStage + 1
            stage8()

         elif stageSelect == "2":
            customValue = 1
            stage7()

         elif stageSelect == "3":
            currentStage = 1
            stage6()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage6():
      global USR_CPU_FEATURE_ARGS
      global customValue
      global currentStage
      defaultValue = "+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"

      clear()
      print("\n"+color.BOLD+"Set CPU feature arguments"+color.END)
      print("Step 6")
      print("\nSet the virtual CPU's feature arguments. \nDo not change this unless you know what you're doing.\nThe default is more than enough for most people."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
         print(color.BOLD+color.PURPLE+"\nFORMAT:",color.YELLOW+"+"+color.END+color.BOLD+"<arg>"+color.YELLOW+","+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_CPU_FEATURE_ARGS = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_FEATURE_ARGS","w")
         blob.write(USR_CPU_FEATURE_ARGS)
         blob.close()
         stage7()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_CPU_FEATURE_ARGS = defaultValue
            blob = open("./blobs/USR_CPU_FEATURE_ARGS","w")
            blob.write(USR_CPU_FEATURE_ARGS)
            blob.close()
            currentStage = currentStage + 1
            stage7()

         elif stageSelect == "2":
            customValue = 1
            stage6()

         elif stageSelect == "3":
            currentStage = 1
            stage5()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage5():
      global USR_CPU_MODEL
      global customValue
      global currentStage
      defaultValue = "Penryn"

      clear()
      print("\n"+color.BOLD+"Set CPU model"+color.END)
      print("Step 5")
      print("\nSet the model of the virtual CPU. \nUnless your host CPU is supported in macOS, leave this alone.\nUse \"host\" to expose the host CPU model to the guest."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+defaultValue+color.END)
      if customValue == 1:
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<model name>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_CPU_MODEL = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_MODEL","w")
         blob.write(USR_CPU_MODEL)
         blob.close()
         stage6()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_CPU_MODEL = defaultValue
            blob = open("./blobs/USR_CPU_MODEL","w")
            blob.write(USR_CPU_MODEL)
            blob.close()
            currentStage = currentStage + 1
            stage6()

         elif stageSelect == "2":
            customValue = 1
            stage5()

         elif stageSelect == "3":
            currentStage = 1
            stage4()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage4():
      global USR_CPU_THREADS
      global customValue
      global currentStage
      defaultValue = 2

      clear()
      print("\n"+color.BOLD+"Set number of CPU threads"+color.END)
      print("Step 4")
      print("\nSet the desired number of virtual CPU threads. \nLike cores, more threads can dramatically improve guest performance if\nyour host can handle it."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      if customValue == 1:
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = int(input(color.BOLD+"Value> "+color.END))
         USR_CPU_THREADS = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_THREADS","w")
         blob.write(str(USR_CPU_THREADS))
         blob.close()
         stage5()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_CPU_THREADS = defaultValue
            blob = open("./blobs/USR_CPU_THREADS","w")
            blob.write(str(USR_CPU_THREADS))
            blob.close()
            currentStage = currentStage + 1
            stage5()

         elif stageSelect == "2":
            customValue = 1
            stage4()

         elif stageSelect == "3":
            currentStage = 1
            stage3()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage3():
      global USR_CPU_CORES
      global USR_TARGET_OS
      global customValue
      global currentStage
      defaultValue = 2


      if USR_TARGET_OS >= 11 and USR_TARGET_OS <= 99:
         USR_TARGET_OS = USR_TARGET_OS * 100

      clear()
      print("\n"+color.BOLD+"Set number of CPU cores"+color.END)
      print("Step 3")
      print("\nSet the desired number of virtual CPU cores. \nMore cores can dramatically improve guest performance if\nyour host can handle it."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      if customValue == 1:
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
      #   print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = int(input(color.BOLD+"Value> "+color.END))
         USR_CPU_CORES = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = currentStage + 1
         customValue = 0
         blob = open("./blobs/USR_CPU_CORES","w")
         blob.write(str(USR_CPU_CORES))
         blob.close()
         stage4()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_CPU_CORES = defaultValue
            blob = open("./blobs/USR_CPU_CORES","w")
            blob.write(str(USR_CPU_CORES))
            blob.close()
            currentStage = currentStage + 1
            stage4()

         elif stageSelect == "2":
            customValue = 1
            stage3()

         elif stageSelect == "3":
            currentStage = 1
            stage2()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage2():
      global USR_TARGET_OS
      global customValue
      global currentStage
      defaultValue = 1015

      clear()
      print("\n"+color.BOLD+"Set target OS"+color.END)
      print("Step 2")
      print("\nThis is only really important for networking. \nIf you are installing macOS Mojave (10.14) or later, you can leave this alone.\nIf you are installing macOS High Sierra (10.13) or earlier, enter it as a custom value."+color.END)
      print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD,defaultValue,color.END)
      if customValue == 1:
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<number>"+color.YELLOW+""+color.END+"\nEnter a custom value.\n\n")
         customInput = int(input(color.BOLD+"Value> "+color.END))
         USR_TARGET_OS = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = 3
         customValue = 0
         blob = open("./blobs/USR_TARGET_OS","w")
         blob.write(str(USR_TARGET_OS))
         blob.close()
         stage3()
      else:
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   3. Back")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_TARGET_OS = defaultValue
            blob = open("./blobs/USR_TARGET_OS","w")
            blob.write(str(USR_TARGET_OS))
            blob.close()
            currentStage = 3
            stage3()

         elif stageSelect == "2":
            customValue = 1
            stage2()

         elif stageSelect == "3":
            currentStage = 1
            stage1()
            
         elif stageSelect == "q" or stageSelect == "Q":
            exit   

   def stage1():
      global USR_CFG
      global customValue
      global currentStage

      clear()

      print("\n"+color.BOLD+"Name your config file"+color.END)
      print("Step 1")
      print("\nThis is simply the name of your config file. \nYou can name it whatever you want. It's used to boot your\nVM and will be the basis of this AutoPilot configuration."+color.END)
      if customValue == 1:
         print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+"boot.sh"+color.END)
         print(color.BOLD+color.PURPLE+"\nFORMAT:"+color.YELLOW+""+color.END+color.BOLD,"<filename>"+color.YELLOW+".sh"+color.END+"\nEnter a custom value. You",color.UNDERLINE+color.BOLD+"must"+color.END,"include any text in"+color.YELLOW,"yellow"+color.END+".\n\n")
         customInput = str(input(color.BOLD+"Value> "+color.END))
         USR_CFG = customInput               #+".sh" #<--- change required prefix/suffix
         currentStage = 2
         customValue = 0
         blob = open("./blobs/USR_CFG","w")
         blob.write(USR_CFG)
         blob.close()
         stage2()

      else:
         print("\n"+color.BOLD+color.CYAN+"DEFAULT:",color.END+color.BOLD+"boot.sh"+color.END)
         print(color.BOLD+"\n   1. Use default value")
         print(color.END+"   2. Custom value...")
         print(color.END+"   Q. Exit\n")
         stageSelect = str(input(color.BOLD+"Select> "+color.END))
      
         if stageSelect == "1":
            USR_CFG = "boot.sh"
            blob = open("./blobs/USR_CFG","w")
            blob.write(USR_CFG)
            blob.close()
            currentStage = 2
            stage2()

         elif stageSelect == "2":
            customValue = 1
            stage1()

         elif stageSelect == "q" or stageSelect == "Q":
            exit

   stage1()

if detectChoice == 1:
   autopilot()
elif detectChoice == 2:
    os.system('./setup.py')

elif detectChoice == 3:
    exit
