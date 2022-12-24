# GPU-CHECK v0.1 BY COOPYDOOD

"""
This script was created by Coopydood as part of the ultimate-osx-kvm project.
You are free to distribute this script however you see fit as long as credit is given.
Enjoy!

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-osx-kvm
Signature: 4CD28348A3DD016F

"""





import os
import time
import subprocess
import re 
import json
import sys
import argparse

parser = argparse.ArgumentParser("gpu-check")
parser.add_argument("-a", "--auto", dest="auto", help="Detect GPU(s) automatically",action="store_true")
parser.add_argument("-m", "--manual", dest="manual", help="Enter GPU model manually", metavar="<model>", type=str)
parser.add_argument("-f", "--force", dest="forceModel", metavar="<model>", help="Override auto-detected GPU with a custom model. Pretty useless, mostly for debugging.", type=str)

args = parser.parse_args()

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
    print("Welcome to"+color.BOLD+color.YELLOW,"gpu-check v0.1"+color.END,"(BETA)")
    print("Created by",color.BOLD+"Coopydood\n"+color.END)
    print("\nThe purpose of this script is to prepare you for GPU passthrough by \nchecking your exact system's GPU model against a macOS compatibility \nlist created and provided by"+color.BOLD,"Dortania.\n"+color.END)
    print(color.BOLD+"\n"+"Profile:"+color.END,"https://github.com/Coopydood")
    print(color.BOLD+"   Repo:"+color.END,"https://github.com/Coopydood/ultimate-osx-kvm")
    print("\nI can attempt to check what GPU you have automatically, or you can manually enter it.\nWhich would you prefer?")
    print(color.BOLD+"\n1. Detect automatically (recommended)")
    print(color.END+"2. Enter manually")
    print(color.END+"3. Exit\n")
    detectChoice = int(input(color.BOLD+"Select> "+color.END))

       


def clear(): print("\n" * 150)


def autoRun():
    print("Running auto detection script...")
    time.sleep(1)
    clear()

    output_stream = os.popen('lspci -v | grep "VGA"')
    vgaGrep = output_stream.read().splitlines()
   # print(vgaGrep)

    output_stream1 = os.popen('lspci | grep "VGA" | cut -d" " -f 1')
    vgaGrepIDs = output_stream1.read().splitlines()
   # print(vgaGrepIDs)


    vgaGrepT = []

    for x in vgaGrep:
        #val = x.split('[', 1)[1].split(']')
        a = "aaaa"
        val = re.findall('\[.*?\]', x)
        vgaGrepT.append(val)
    gpuList = open("./gpulist.json")
    data = json.load(gpuList)
    model = str(vgaGrep)

    # EXPERIMENTAL VENDOR SEGMENTATION 
    """
    vendorList = []

    if "NVIDIA" in model:
        vendorList.append("nvidia")
    if "AMD" or "ATI" in model:
        vendorList.append("amd")
    else:
        vendorList.append("other")

    #vendorList = str(vendorList)
    #vendorList = vendorList.replace('[','').replace(']','').replace(' ','')

    #vendorList = "['amd'],['nvidia']" #DEBUG

    for vendX in vendorList:
        gpus = [y for y in data['gpuList'][vendX]]
        gpuCount = 0
        for gpu in gpus:
            if (gpu["name"]) in model:
                gpuCount = gpuCount + 1
    """

    if args.forceModel is not None:
        model = args.forceModel

    #model = "[DEBUG]" #<-- Uncomment to override GPU for testing

    gpus = [y for y in data['gpuList']]
    gpuCount = 0
    for gpu in gpus:
        if (gpu["name"]) in model:
            gpuCount = gpuCount + 1

    if gpuCount >= 2:
        print("I"+color.BOLD+color.GREEN,"successfully"+color.END,"detected"+color.BOLD,gpuCount,"GPUs"+color.END,"in your system:\n")
    elif gpuCount == 1:
        print("I"+color.BOLD+color.GREEN,"successfully"+color.END,"detected"+color.BOLD,gpuCount,"GPU"+color.END,"in your system:\n")
    else:
        print("I"+color.BOLD+color.RED,"failed"+color.END,"to detect any GPUs in your system.\nSomething has went very wrong somewhere, or your GPU is weirder than you are.\nPerhaps try entering your GPU model"+color.BOLD,"manually"+color.END,"by selecting the second option instead.\n")

    for gpu in gpus:
        if (gpu["name"]) in model:
            gpuName = gpu["fullName"]
            gpuSupport = gpu["supported"]
            gpuVendor = gpu["vendor"]
            gpuMinOS = gpu["minOS"]
            gpuMaxOS = gpu["maxOS"]
            gpuQuirks = gpu["quirks"]

            if gpuMinOS == "-1":
                gpuMinOS = "N/A"

            if gpuQuirks == "0":
                gpuQuirks = "This GPU should work fine."
            elif gpuQuirks == "-1":
                gpuQuirks = "This GPU is NOT supported in macOS at all. Sorry :["

            gpuMaxOSF = "N/A"
            if "10.2" in gpuMaxOS:
                gpuMaxOSF = "Jaguar ("+gpuMaxOS+")"
            elif "10.3" in gpuMaxOS:
                gpuMaxOSF = "Panther ("+gpuMaxOS+")"
            elif "10.4" in gpuMaxOS:
                gpuMaxOSF = "Tiger ("+gpuMaxOS+")"
            elif "10.5" in gpuMaxOS:
                gpuMaxOSF = "Leopard ("+gpuMaxOS+")"
            elif "10.6" in gpuMaxOS:
                gpuMaxOSF = "Snow Leopard ("+gpuMaxOS+")"
            elif "10.7" in gpuMaxOS:
                gpuMaxOSF = "Lion ("+gpuMaxOS+")"
            elif "10.8" in gpuMaxOS:
                gpuMaxOSF = "Mountain Lion ("+gpuMaxOS+")"
            elif "10.9" in gpuMaxOS:
                gpuMaxOSF = "Mavericks ("+gpuMaxOS+")"
            elif "10.10" in gpuMaxOS:
                gpuMaxOSF = "Yosemite ("+gpuMaxOS+")"
            elif "10.11" in gpuMaxOS:
                gpuMaxOSF = "El Capitan ("+gpuMaxOS+")"
            elif "10.12" in gpuMaxOS:
                gpuMaxOSF = "Sierra ("+gpuMaxOS+")"
            elif "10.13" in gpuMaxOS:
                gpuMaxOSF = "High Sierra ("+gpuMaxOS+")"
            elif "10.14" in gpuMaxOS:
                gpuMaxOSF = "Mojave ("+gpuMaxOS+")"
            elif "10.15" in gpuMaxOS:
                gpuMaxOSF = "Catalina ("+gpuMaxOS+")"
            elif "11" in gpuMaxOS:
                gpuMaxOSF = "Big Sur ("+gpuMaxOS+")"
            elif "12" in gpuMaxOS:
                gpuMaxOSF = "Monterey ("+gpuMaxOS+")"
            elif "13" in gpuMaxOS:
                gpuMaxOSF = "Ventura ("+gpuMaxOS+")"
            
            gpuMinOSF = "N/A"
            if "10.2" in gpuMinOS:
                gpuMinOSF = "Jaguar ("+gpuMinOS+")"
            elif "10.3" in gpuMinOS:
                gpuMinOSF = "Panther ("+gpuMinOS+")"
            elif "10.4" in gpuMinOS:
                gpuMinOSF = "Tiger ("+gpuMinOS+")"
            elif "10.5" in gpuMinOS:
                gpuMinOSF = "Leopard ("+gpuMinOS+")"
            elif "10.6" in gpuMinOS:
                gpuMinOSF = "Snow Leopard ("+gpuMinOS+")"
            elif "10.7" in gpuMinOS:
                gpuMinOSF = "Lion ("+gpuMinOS+")"
            elif "10.8" in gpuMinOS:
                gpuMinOSF = "Mountain Lion ("+gpuMinOS+")"
            elif "10.9" in gpuMinOS:
                gpuMinOSF = "Mavericks ("+gpuMinOS+")"
            elif "10.10" in gpuMinOS:
                gpuMinOSF = "Yosemite ("+gpuMinOS+")"
            elif "10.11" in gpuMinOS:
                gpuMinOSF = "El Capitan ("+gpuMinOS+")"
            elif "10.12" in gpuMinOS:
                gpuMinOSF = "Sierra ("+gpuMinOS+")"
            elif "10.13" in gpuMinOS:
                gpuMinOSF = "High Sierra ("+gpuMinOS+")"
            elif "10.14" in gpuMinOS:
                gpuMinOSF = "Mojave ("+gpuMinOS+")"
            elif "10.15" in gpuMinOS:
                gpuMinOSF = "Catalina ("+gpuMinOS+")"
            elif "11" in gpuMinOS:
                gpuMinOSF = "Big Sur ("+gpuMinOS+")"
            elif "12" in gpuMinOS:
                gpuMinOSF = "Monterey ("+gpuMinOS+")"
            elif "13" in gpuMinOS:
                gpuMinOSF = "Ventura ("+gpuMinOS+")"

            if "Ti" in model:
                gpuName = gpuName + " Ti"

            if "SUPER" in model:
                gpuName = gpuName + " Super"

            if "XT" in model:
                gpuName = gpuName + " XT" 

            print(color.BOLD+gpuName+color.END)
            print("───────────────────────────────")
            if gpuSupport == True:
                print(color.BOLD+color.GREEN+"●",color.END+"Supported\n")
            elif gpuSupport == False:
                print(color.BOLD+color.RED+"●",color.END+"Unsupported\n")
            else:
                print(color.BOLD+color.YELLOW+"●",color.END+"Problematic\n")
            
            if gpuMaxOS == "9999":
                print(color.BOLD+"Maximum macOS:"+color.END,"Latest /",latestOSName,"("+latestOSVer+")")
            elif gpuMaxOS == "-1":
                print(color.BOLD+"Maximum macOS:"+color.END,"N/A")
            else:
                print(color.BOLD+"Maximum macOS:"+color.END,gpuMaxOSF)

            if gpuMinOS == "-1":
                print(color.BOLD+"Minimum macOS:"+color.END,"N/A")
            else:
                print(color.BOLD+"Minimum macOS:"+color.END,gpuMinOSF)
            
            print("\n"+color.BOLD+"Additional Information"+color.END)
            print(gpuQuirks)

            print("\n")
            exit

def manualRun():
    clear()
    if args.manual is not None:
        model = args.manual
    else:
        print(color.BOLD+"Enter your GPU manually\n")
        print("\nYou have chosen to"+color.BOLD,"enter your GPU model manually."+color.END)
        print("To do this, simply type the model of your GPU and hit the ENTER key. You do not\nhave to include the vendor name.\n")
        print(color.BOLD+"  Example:"+color.END+" If you had an",color.BOLD+"AMD Radeon RX 550")
        print(color.END+"           You would type"+color.BOLD,"RX 550")
        print(color.BOLD+color.CYAN+"\nTIP:"+color.END,"You can see a list of GPUs installed in your system by running "+color.BOLD+"lspci -v | grep \"VGA\"")
        print(color.BOLD+"\n")
        gpuList = open("./gpulist.json")
        data = json.load(gpuList)
        model = str(input(color.BOLD+"Model> "+color.END))

        if "RX" in model:
            model = "Radeon "+model
    clear()

    gpus = [y for y in data['gpuList']]
    gpuCount = 0
    for gpu in gpus:
        if (gpu["name"]) in model:
            gpuCount = gpuCount + 1

    if gpuCount == 1:
        print("I"+color.BOLD+color.GREEN,"successfully"+color.END,"found a match for "+color.BOLD+"\""+model+"\""+color.END+" in the database:\n")
    else:
        print("I"+color.BOLD+color.RED,"failed"+color.END,"to find a match for "+color.BOLD+"\""+model+"\""+color.END+" in the database.\nPlease check your"+color.BOLD,"spelling"+color.END,"and ensure you're not imagining a GPU's existence.\n")
        exit

    for gpu in gpus:
        if (gpu["name"]) in model:
            gpuName = gpu["fullName"]
            gpuSupport = gpu["supported"]
            gpuVendor = gpu["vendor"]
            gpuMinOS = gpu["minOS"]
            gpuMaxOS = gpu["maxOS"]
            gpuQuirks = gpu["quirks"]

            if gpuMinOS == "-1":
                gpuMinOS = "N/A"

            if gpuQuirks == "0":
                gpuQuirks = "This GPU should work fine."
            elif gpuQuirks == "-1":
                gpuQuirks = "This GPU is NOT supported in macOS at all. Sorry :["

            gpuMaxOSF = "N/A"
            if "10.2" in gpuMaxOS:
                gpuMaxOSF = "Jaguar ("+gpuMaxOS+")"
            elif "10.3" in gpuMaxOS:
                gpuMaxOSF = "Panther ("+gpuMaxOS+")"
            elif "10.4" in gpuMaxOS:
                gpuMaxOSF = "Tiger ("+gpuMaxOS+")"
            elif "10.5" in gpuMaxOS:
                gpuMaxOSF = "Leopard ("+gpuMaxOS+")"
            elif "10.6" in gpuMaxOS:
                gpuMaxOSF = "Snow Leopard ("+gpuMaxOS+")"
            elif "10.7" in gpuMaxOS:
                gpuMaxOSF = "Lion ("+gpuMaxOS+")"
            elif "10.8" in gpuMaxOS:
                gpuMaxOSF = "Mountain Lion ("+gpuMaxOS+")"
            elif "10.9" in gpuMaxOS:
                gpuMaxOSF = "Mavericks ("+gpuMaxOS+")"
            elif "10.10" in gpuMaxOS:
                gpuMaxOSF = "Yosemite ("+gpuMaxOS+")"
            elif "10.11" in gpuMaxOS:
                gpuMaxOSF = "El Capitan ("+gpuMaxOS+")"
            elif "10.12" in gpuMaxOS:
                gpuMaxOSF = "Sierra ("+gpuMaxOS+")"
            elif "10.13" in gpuMaxOS:
                gpuMaxOSF = "High Sierra ("+gpuMaxOS+")"
            elif "10.14" in gpuMaxOS:
                gpuMaxOSF = "Mojave ("+gpuMaxOS+")"
            elif "10.15" in gpuMaxOS:
                gpuMaxOSF = "Catalina ("+gpuMaxOS+")"
            elif "11" in gpuMaxOS:
                gpuMaxOSF = "Big Sur ("+gpuMaxOS+")"
            elif "12" in gpuMaxOS:
                gpuMaxOSF = "Monterey ("+gpuMaxOS+")"
            elif "13" in gpuMaxOS:
                gpuMaxOSF = "Ventura ("+gpuMaxOS+")"
            
            gpuMinOSF = "N/A"
            if "10.2" in gpuMinOS:
                gpuMinOSF = "Jaguar ("+gpuMinOS+")"
            elif "10.3" in gpuMinOS:
                gpuMinOSF = "Panther ("+gpuMinOS+")"
            elif "10.4" in gpuMinOS:
                gpuMinOSF = "Tiger ("+gpuMinOS+")"
            elif "10.5" in gpuMinOS:
                gpuMinOSF = "Leopard ("+gpuMinOS+")"
            elif "10.6" in gpuMinOS:
                gpuMinOSF = "Snow Leopard ("+gpuMinOS+")"
            elif "10.7" in gpuMinOS:
                gpuMinOSF = "Lion ("+gpuMinOS+")"
            elif "10.8" in gpuMinOS:
                gpuMinOSF = "Mountain Lion ("+gpuMinOS+")"
            elif "10.9" in gpuMinOS:
                gpuMinOSF = "Mavericks ("+gpuMinOS+")"
            elif "10.10" in gpuMinOS:
                gpuMinOSF = "Yosemite ("+gpuMinOS+")"
            elif "10.11" in gpuMinOS:
                gpuMinOSF = "El Capitan ("+gpuMinOS+")"
            elif "10.12" in gpuMinOS:
                gpuMinOSF = "Sierra ("+gpuMinOS+")"
            elif "10.13" in gpuMinOS:
                gpuMinOSF = "High Sierra ("+gpuMinOS+")"
            elif "10.14" in gpuMinOS:
                gpuMinOSF = "Mojave ("+gpuMinOS+")"
            elif "10.15" in gpuMinOS:
                gpuMinOSF = "Catalina ("+gpuMinOS+")"
            elif "11" in gpuMinOS:
                gpuMinOSF = "Big Sur ("+gpuMinOS+")"
            elif "12" in gpuMinOS:
                gpuMinOSF = "Monterey ("+gpuMinOS+")"
            elif "13" in gpuMinOS:
                gpuMinOSF = "Ventura ("+gpuMinOS+")"

            if "Ti" in model:
                gpuName = gpuName + " Ti"

            if "SUPER" in model:
                gpuName = gpuName + " Super"

            if "XT" in model:
                gpuName = gpuName + " XT" 

            print(color.BOLD+gpuName+color.END)
            print("───────────────────────────────")
            if gpuSupport == True:
                print(color.BOLD+color.GREEN+"●",color.END+"Supported\n")
            elif gpuSupport == False:
                print(color.BOLD+color.RED+"●",color.END+"Unsupported\n")
            else:
                print(color.BOLD+color.YELLOW+"●",color.END+"Problematic\n")
            
            if gpuMaxOS == "9999":
                print(color.BOLD+"Maximum macOS:"+color.END,"Latest /",latestOSName,"("+latestOSVer+")")
            elif gpuMaxOS == "-1":
                print(color.BOLD+"Maximum macOS:"+color.END,"N/A")
            else:
                print(color.BOLD+"Maximum macOS:"+color.END,gpuMaxOSF)

            if gpuMinOS == "-1":
                print(color.BOLD+"Minimum macOS:"+color.END,"N/A")
            else:
                print(color.BOLD+"Minimum macOS:"+color.END,gpuMinOSF)
            
            print("\n"+color.BOLD+"Additional Information"+color.END)
            print(gpuQuirks)

            print("\n")
            exit

if args.manual is not None and runs == 0:
        runs = 1
        manualRun()
elif args.auto is not False and runs == 0:
        runs = 1
        autoRun()  
else:
    runs = 1
    startup()


    if detectChoice == 1:
        autoRun()
    elif detectChoice == 2:
        manualRun()
    else:
        exit


