## main.py
This file acts as the project's main menu and should be used for all of your endeavors. 

![Main menu of ultimate-macOS-KVM v0.9.0](https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/7ebc2d8d-98a8-4d29-918c-efaa3e2ec06e)

This section will highlight each option and briefly explain what it does without going into detail.

***
## 1. AutoPilot
This is what I'd consider to be the "meat and potatoes" of the project - but that might be biased considering it's what took me the longest to make...
Anyway, AutoPilot is an advanced script designed to completely automate the generation of a fully valid QEMU boot script - customised to exactly your specifications.

AutoPilot lets you configure the following:
* Script name
* Target OS
* CPU cores
* CPU threads
* CPU model
* CPU feature args 
* Allocated RAM
* Virtual hard disk capacity
* Network adapter model
* MAC address
* Bootable macOS recovery image

For more information on AutoPilot, see [this page](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot).

***
## 2. Download macOS...
Adapted from **vit9696**'s `fetch-macOS-v2.py` script, this option lets you easily select and download the base recovery image for your desired version of macOS. I've modified this script to work with this project specifically, but the changes are minor and all credit should go to vit9696 for their work on this script.

The file downloaded is in the **.dmg** format, which for the purpose of booting a VM, is completely useless. So, I've adapted the script to automatically launch **dmg2img**, a small program that extracts Apple DMG files into **.img** files - which *can* be booted.

It's also worth noting that the file downloaded is **not** the full installer image, but rather the relatively small **BaseSystem.dmg** used for macOS recovery. The BaseSystem file download is typically under 800 MB. To install macOS, you will need an internet connection - with the total download size from recovery itself often exceeding 10 GB. 

***
## 3. System compatibility checks...
This menu contains a few scripts designed to automatically test your system configuration and check it for any issues that may prevent you from using features such as KVM itself or VFIO-PCI passthrough. Your installed GPU(s) can also be checked for compatibility with macOS from this menu too.

***
## 4. VFIO-PCI passthrough tools...
Another menu that presents a list of useful tools that can assist in the preparation and configuration of VFIO-PCI passthrough of physical PCI devices, such as GPUs or audio cards. This menu also lets you start the **VFIO-PCI passthrough assistant** - an easy, guided way to get your system set up for successful passthrough.

This toolset can also be accessed from the Extras menu, as this main menu shortcut may be removed in a later version.

***
## E. Extras...
What it says on the tin, really. This menu contains loads of other goodies, such as the AutoPilot extension script - **VFIO-PCI Passthrough Assistant** - which aims to make passing through devices a more seamless experience by walking you through each step and making the relevant changes to your config file for you. 

You can also do other things here such as **resetting your OpenCore image**, or resetting **the entire repo** for those oopsie-whoopsie moments.

For more information on Exras, see [this page](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Extras).

***
## U. Check for updates...
This project has been designed to be updated and made better over time.

As you use it to generate your personal files, having to re-clone the entire repo yourself while preserving your files would be a right pain in the backside. 

Therefore, there's an automated updater script built right-in that you can use to safely update in-place to newer versions of this project, without affecting any of your personal config files, virtual hard drives, or anything else not part of the project files. And, if an update dramatically changes directory structures from your current version, the updater automatically disables its in-place update mechanism to prevent data loss.

Of course, if you're just testing the project, then a "clean install" is probably still preferable.