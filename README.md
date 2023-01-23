# ultimate-macOS-KVM
Helping you build the ultimate macOS virtual machine, powered by KVM.

## Requirements

## Features
<ul>
<li><b>AutoPilot</b></li>
Automatically generates a valid, customised, and ready-to-use QEMU config script in seconds.

<li><b>Automatic System Checks</b></li>
Several check scripts can be used to make sure your system is correctly prepared for both passthrough and non-passthrough KVM.

<li><b>GPU Compatibility Checker</b></li>
Detects GPUs in your host system and checks them against a list of known compatible and incompatible macOS GPUs, providing a summary including any extra card-specific quirks.

<li><b>VFIO-IDs and IOMMU Helpers</b></li>
Auto-detects and lists IOMMU groups, VFIO-IDs, and checks if devices are stubbed to kernel driver correctly.

<li><b>VFIO-PCI Passthrough Assistant</b></li>
Advanced passthrough tinkering made easy with auto-detection and configuration walkthroughs.

<li><b>Import to virt-manager</b></li>
Easily convert any AutoPilot-generated QEMU scripts into an importable XML file for virt-manager (GUI).

</ul>

## Installation
It's easy to get up and running. Simply clone the repo, fix permissions, and run.
Make sure you have **all** dependencies installed before using.

```
git clone https://github.com/Coopydood/ultimate-macOS-KVM
cd ultimate-macOS-KVM
chmod +x setup.py
```
or, do all this with a one-liner:
```
git clone https://github.com/Coopydood/ultimate-macOS-KVM && cd ultimate-macOS-KVM && chmod +x setup.py
```
## Setup
Okay, so you've cloned my repo, cd'd into the directory, and made the ``setup.py`` file executeable. Great! 
Now, before running the script - and to avoid the subsequent and inevitable gotcha - you should enable the ``libvirtd`` daemon first if it hasn't been already:
```
sudo systemctl enable libvirtd
```
and/or check the status of the daemon with
```
systemctl status libvirtd
```

Okay, now you're ready to use **ultimate-macOS-KVM**. Use the main ``setup.py`` file. This is your main menu / central hub for the project and everything can be accessed from here. Most sub-scripts included in the project should *not* be run on their own.
```
./setup.py
```

## Documentation
More detailed write-ups on the project and the scripts included, as well as some tutorials can be found on this repo's wiki.
[I'm working on it...](https://github.com/Coopydood/ultimate-macOS-KVM/wiki)

## Disclaimer
This is my way of giving back to the QEMU, KVM, and VFIO community. Please don't expect much as this is a passion-project and not a priority in my life.
- I'm not responsible for any time you waste using this project.
- I'm not responsible if you make an oopsie whoopsie. 
- Do NOT run anything as ``sudo``. If you have an urge to then you need to break that habit __**asap.**__ None of my scripts require superuser priviledges.
- Expect headaches. Some severe.
- You need a LOT of patience. I mean it. Despite trying to alleviate some of the hassle, you WILL run into stupid gotchas that require trial and error out of my control. 
- I'm by no means an expert on this stuff nor would I claim to be.
- I've simply made *what I had to go through* **easier** for you. Hopefully.
- Yes, my Python is pretty bad. But if it works, it works.
