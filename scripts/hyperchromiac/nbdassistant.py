#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

# Vendor         : Hyperchromiac
# Provisioned by : Coopydood

# Import Required Modules
import os
import time
import sys
import subprocess
from datetime import datetime
sys.path.append('./resources/python')
from cpydColours import color
import argparse


version = open("./.version")
version = version.read()

enableLog = True

parser = argparse.ArgumentParser("autopilot")
parser.add_argument("--disable-logging", dest="disableLog", help="Disables the logfile",action="store_true")
parser.add_argument("-m","--mount", dest="mount", help="Immediately mount detected OC image",action="store_true")
parser.add_argument("-u","--unmount", dest="unmount", help="Immediately unmount detected OC image",action="store_true")
parser.add_argument("-q","--quiet", dest="quiet", help="Don't print any verbose information",action="store_true")

args = parser.parse_args()

global logTime
logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))

def clear(): print("\n" * 150)

if args.disableLog == True:
   enableLog = False

if enableLog == True: # LOG SUPPORT
   if not os.path.exists("./logs"):
      os.system("mkdir ./logs")

   logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))
   os.system("echo ULTMOS OCMA LOG "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/OCMA_RUN_"+logTime+".log")
   os.system("echo ──────────────────────────────────────────────────────────────"+" >> ./logs/OCMA_RUN_"+logTime+".log")

   def cpydLog(logStatus,logMsg,*args):
      logFile = open("./logs/OCMA_RUN_"+logTime+".log","a")
      
      if logStatus == "ok":      logStatus = "[  OK  ]: "
      if logStatus == "info":    logStatus = "[ INFO ]: "
      if logStatus == "warn":    logStatus = "[ WARN ]: "
      if logStatus == "error":   logStatus = "[ ERROR ]:"
      if logStatus == "fatal":   logStatus = "[ FATAL ]:"
      if logStatus == "wait":    logStatus = "[ WAIT ]: "
      if logStatus == "debug":   logStatus = "[ DEBUG ]:"
      entryTime = str(datetime.today().strftime('%H:%M:%S.%f'))
      entryTime = entryTime[:-3]
      entryLine = ("["+entryTime+"]"+str(logStatus)+" "+str(logMsg)+"\n")
      logFile.write(entryLine)
      logFile.close()
else:
   def cpydLog(logStatus,logMsg,*args):
      None

script = "nbdassistant.py"
scriptName = "OpenCore Configuration Assistant"
scriptID = "OCMA"
scriptVendor = "Hyperchromiac"


cpydLog("info",("ULTMOS v"+version))
cpydLog("info",(" "))
cpydLog("info",("Name       : "+scriptName))
cpydLog("info",("File       : "+script))
cpydLog("info",("Identifier : "+scriptID))
cpydLog("info",("Vendor     : "+scriptVendor))
cpydLog("info",(" "))
cpydLog("info",("Logging to ./logs/OCMA_RUN_"+logTime+".log"))

detectchoice = 0

def run_command(command):
    """Run a system command and return exit code, stdout, stderr"""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        exit_code = process.returncode
        return exit_code, stdout, stderr
    except Exception as e:
        return 1, "", str(e)

def check_nbd_mounted():
    """Check if NBD is already connected"""
    try:
        exit_code, stdout, stderr = run_command("lsblk")
        return "nbd0" in stdout
    except Exception as e:
        cpydLog("error", f"Error checking if NBD is mounted: {str(e)}")
        return False

def menu():
    global detectchoice
    # Get Terminal Size
    if args.quiet != True:
        os.system("clear")
    spaces = ""
    i = 0
    terminal_size = os.get_terminal_size()
    while i < terminal_size.lines:
        spaces = spaces + "\n"
        i += 1
    # Menu
    if args.mount != True and args.unmount != True:
        print(spaces + "   \033[1m\033[94mOPENCORE ASSISTANT\033[0m")
        print("   by \033[1mHyperchromiac\033[0m and \033[1mkunihir0\033[0m\n")
        print("   This script was created with the sole purpose of simplifying\n   the process of mounting and unmounting your OpenCore.qcow2\n   so you can make any modifications necessary. \033[37m(e.g. config.plist)\n\n\033[93m   It is highly recommended that you \033[91m\033[1mBACKUP\033[0m\033[93m your OpenCore.qcow2\n   in case you mess something up.\033[0m\n")
        print("   Select an option to continue.\n")
        print("      1. Mount OpenCore ⚠\n         This will mount your OpenCore.qcow2 with read-write permissions.\n         \033[93mWill prompt you for superuser permissions, which are required.\033[0m\n")
        print("      2. Unmount OpenCore ⚠\n         This will unmount your OpenCore.qcow2 so you can boot with your modifications.\n         \033[93mWill prompt you for superuser permissions, which are required.\033[0m\n")
        print("      B. Back...")
        print("      Q. Exit\n")
        cpydLog("info",("Awaiting user input."))
        detectchoice = input("\033[1mSelect> \033[0m")
    elif args.mount == True:
        detectchoice = 1
    elif args.unmount == True:
        detectchoice = 2
    else:
        cpydLog("fatal","Invalid argument passthrough")
        exit()

    if detectchoice == 1 or detectchoice == "1":
        # Check if OpenCore.qcow2 exists
        if not os.path.exists("boot/OpenCore.qcow2"):
            cpydLog("error", "OpenCore.qcow2 not found in boot directory")
            if args.quiet != True:
                print(spaces)
                print("\n   \033[91mError: OpenCore.qcow2 not found in boot directory.\033[0m")
                input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
            if args.mount != True and args.unmount != True:
                detectchoice = 0
                menu()
            return

        # Check if NBD is already mounted
        if check_nbd_mounted():
            cpydLog("warn", "NBD is already mounted. Unmount first.")
            if args.quiet != True:
                print(spaces)
                print("\n   \033[93mWarning: OpenCore image appears to be already mounted.\033[0m")
                print("   \033[93mPlease unmount it first using option 2.\033[0m")
                input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
            if args.mount != True and args.unmount != True:
                detectchoice = 0
                menu()
            return

        # Make sure boot/mnt directory exists
        os.system("mkdir -p boot/mnt")
        
        # Load NBD module
        clear()
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To mount the OpenCore image,\n   the script needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)

        os.system("sudo modprobe nbd")
        
        # Connect the OpenCore qcow2 image
        try:
            cpydLog("info", "Connecting OpenCore.qcow2 to NBD device")
            exit_code, stdout, stderr = run_command("sudo qemu-nbd --connect=/dev/nbd0 boot/OpenCore.qcow2")
            
            if exit_code != 0:
                cpydLog("error", f"Failed to connect qcow2 to NBD: {stderr}")
                if args.quiet != True:
                    print(spaces)
                    print("\n   \033[91mError: Failed to connect OpenCore.qcow2 to NBD device.\033[0m")
                    print(f"   \033[91m{stderr}\033[0m")
                    input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
                if args.mount != True and args.unmount != True:
                    detectchoice = 0
                    menu()
                return
                
            # Wait for device to be available
            time.sleep(3)
            
            # Get current user ID and group ID
            uid = os.getuid()
            gid = os.getgid()
            
            # Mount the partition with the correct permissions
            mount_cmd = f"sudo mount /dev/nbd0p1 boot/mnt -o uid={uid},gid={gid}"
            exit_code, stdout, stderr = run_command(mount_cmd)
            
            if exit_code != 0:
                cpydLog("error", f"Failed to mount OpenCore partition: {stderr}")
                if args.quiet != True:
                    print(spaces)
                    print("\n   \033[91mError: Failed to mount OpenCore partition.\033[0m")
                    print(f"   \033[91m{stderr}\033[0m")
                    input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
                
                # Clean up if mount failed
                run_command("sudo qemu-nbd --disconnect /dev/nbd0")
            else:
                if args.quiet != True:
                    print(spaces)
                    print("\n   \033[92mOperation completed successfully! \033[32m(mounted at ./boot/mnt/)\033[0m")
                    input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
                cpydLog("ok",("User has mounted OpenCore image."))
        except Exception as e:
            cpydLog("error", f"Error mounting OpenCore: {str(e)}")
            if args.quiet != True:
                print(spaces)
                print(f"\n   \033[91mError: {str(e)}\033[0m")
                input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
                
        if args.mount != True and args.unmount != True:
            detectchoice = 0
            menu()

    elif detectchoice == 2 or detectchoice == "2":
        # Check if NBD is mounted before attempting to unmount
        if not check_nbd_mounted():
            cpydLog("warn", "NBD is not mounted. Nothing to unmount.")
            if args.quiet != True:
                print(spaces)
                print("\n   \033[93mNothing to unmount. OpenCore image is not mounted.\033[0m")
                input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
            if args.unmount != True and args.unmount != True:
                detectchoice = 0
                menu()
            return
        
        # Unmount and disconnect
        cpydLog("info", "Unmounting boot/mnt directory")
        clear()
        print(color.YELLOW+color.BOLD+"\n   ⚠ "+color.END+color.BOLD+"SUPERUSER PRIVILEGES"+color.END+"\n   To mount the OpenCore image,\n   the script needs superuser to continue.\n\n   Press CTRL+C to cancel.\n"+color.END)
        
        unmount_result, unmount_stdout, unmount_stderr = run_command("sudo umount -R boot/mnt")
        
        if unmount_result != 0:
            cpydLog("warn", f"Failed to unmount boot/mnt: {unmount_stderr}")
            # Try forced unmount
            run_command("sudo umount -R -f boot/mnt")
        
        # Disconnect NBD
        cpydLog("info", "Disconnecting NBD device")
        run_command("sudo qemu-nbd --disconnect /dev/nbd0")
        
        # Remove the NBD module
        run_command("sudo rmmod nbd 2>/dev/null || true")
        
        if args.quiet != True:
            print(spaces)
            print("\n   \033[92mOperation completed. \033[32m(unmounted from ./boot/mnt/)\033[0m")
            input("\n\033[1m   Press [ENTER] to continue...\033[0m\n")
        cpydLog("ok",("User has unmounted OpenCore image."))
        
        if args.mount != True and args.unmount != True:
            detectchoice = 0
            menu()
    elif detectchoice == "B" or detectchoice == "b":
        print(spaces)
        os.system('./scripts/extras.py')
    elif detectchoice == "Q" or detectchoice == "q":
        exit()
    else:
        if len(detectchoice) > 3:
            print(spaces)
            print("   So... we wanna be a smartass. Well,\n   in the least respectful way possible...\n")
            print("                        /´¯¯`/)")
            print("                       /¯.../")
            print("                      /..../")
            print("                  /´¯/'..'/´¯¯`·¸")
            print("              /'/.../..../....../¨¯\\")
            print("             ('(....´...´... ¯~/'..')")
            print("              \\..............'...../")
            print("               \\....\\.........._.·´")
            print("                \\..............(")
            print("                 \\..............\\\n")
            cpydLog("fatal",("User is being belligerent."))
            input("\n\033[1m   Press [ENTER] to continue...\033[0m")
        else:
            cpydLog("ok",("User has fat fingered a mere script. Yeah, that extra character didn't work."))
        detectchoice = 0
        menu()

menu()
