---
title: Frequently Asked Questions (FAQs)
---

## Frequently Asked Questions (FAQs)
### Some of the most asked questions, including the basics

#### Introduction

Scripts? Configs? QEMU arguments? A *"qcow"* file? Moo? If you need a little help wrapping your head around this stuff, this is the right document! Find a question from the list below and click the dropdown to see my expertly-crafted answer.

***
<details><summary><h5>What is the purpose of this project?</h5></summary>

*ultimate-macOS-KVM* was created to try and ease the complications of creating a macOS virtual machine through KVM, including some of the more advanced tasks, like GPU passthrough.

</details>

<details><summary><h5>How does this work?</h5></summary>

Written in Python, this project uses various scripts to automate the creation and management of a macOS virtual machine, using QEMU and KVM. 

The scripts are run in terminal-space. Scripts included in the project intended on being used by the user present with terminal UIs (TUIs), creating a friendly approach to the command line. 

</details>

<details><summary><h5>It's for noobs, right?</h5></summary>

It can be, sure. But *ultimate-macOS-KVM* is designed for everyone. You may well be a noob, and that's okay, but you might also be a professional **nerd** who knows everything about everything. Either way, this project was made for you. 

While there is a focus on user-friendliness, there are plenty of advanced features and functionality present within the project. For example, did you know that the built in updater can upgrade and downgrade to *any version* of the project using command arguments? Neither did I!

Furthermore, it's as f*ck-up-proof as possible, with tools designed to help you recover from such misadventures without losing valuable files, such as a soft reset of the virtual NVRAM, which can be used to fix common bootloader issues. Or, for the hardcore misintellectual, you can even download and reset the *entire* project from *within* the project. Pure mental- *for* the pure mental.

</details>

<details><summary><h5>Why should I use this?</h5></summary>

Idk. But, if you're reading this you're clearly interested, so I'll try convince you. 

The main "selling point" of the project is probably **AutoPilot**, which is a massive script that can do the following:

- Guide the user through virtual hardware setup, including explanations
- Automatically changes the recommended defaults based on several factors, including the choices you make
- Load preset files for express setup, no options needed (in development)
- Plenty of granular options for advanced users
- Automatically downloads macOS for you, or you can supply your own image
- __Have a fully-functional KVM-powered macOS VM in under 5 minutes__
- Sleep deprive the developer of the project

Additionally, as mentioned in the last section (which I know you read), there's crisis-management built right in, for all those f*cky-wuckies you might have. The project includes a suite of restoration tools that help you attempt virtual machine boot recovery without losing your install and anything in it.

</details>

<details><summary><h5>Can my computer run this?</h5></summary>

Does it run Crysis? Yes? You're wrong. Anyway, the answer is *probably*. 

Any recent Linux kernel has KVM built right in, meaning you don't have to do any extra setup on that front. 

> [!IMPORTANT]
> You **must** be booting in UEFI mode, and **NOT** legacy BIOS mode. Secure Boot should also ideally be disabled.

CSM and ROM-BAR may need to be enabled / disabled based on your specific system. See the [gotchas page](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Gotchas) for more on this.

All you need to do is install the dependencies and have your hardware meet the requirements, both listed [here](https://github.com/Coopydood/ultimate-macOS-KVM#requirements). Then, just follow the small guide included [here](https://github.com/Coopydood/ultimate-macOS-KVM#getting-started). You can choose any Linux distro that you want, but individual installations of packages will likely differ between different distros (apt, pacman, rpm, etc.).

There are also a few automatic system checkers built in, included in the `./scripts/extras/` folder and can be run seperately from the project - or using the included submenu in v0.9.0 or later. These can check the following:

- Whether your system is ready for basic KVM
- If your system is set up for VFIO-PCI passthrough
- The compatibility of your installed GPUs with macOS
- IOMMU grouping
- VFIO-PCI kernel driver device bindings
- VFIO-PCI IDs of installed hardware

</details>

<details><summary><h5>What is a "qcow2" file?</h5></summary>

Moof! (Clarus reference, anyone?)

A ``.qcow2`` file is simply a virtual hard disk file used mainly by QEMU/KVM. 

The VMware equivalent would be a ``.vmdk`` file.

The VirtualBox equivalent would be a ``.vdi`` or ``.vdk`` file.

</details>

<details><summary><h5>What are QEMU arguments?</h5></summary>

WHY HAS MY DAD BEEN GONE SO LONG? WORKING WITH QEMU AGAIN?!
NO MICHAEL! HE JUST WENT TO GET THE MILK-

Oh, sorry, not that kind of QEMU argument!

The QEMU arguments are simply the list of variables passed on to the ``qemu-system-x86_64`` program, used to set up your virtual machine. 

The arguments themselves shouldn't be edited by the user, as they've been pre-programmed to work out-of-the-box.

They look similar to this:

```
args=(
-global ICH9-LPC.acpi-pci-hotplug-with-bridge-support=off
-enable-kvm -m "$ALLOCATED_RAM" -cpu "$CPU_MODEL",kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on,"$CPU_FEATURE_ARGS"
-machine q35
-usb -device usb-kbd -device usb-tablet #USB_DEV
-smp "$CPU_THREADS",cores="$CPU_CORES",sockets="$CPU_SOCKETS"
-device usb-ehci,id=ehci
-device qemu-xhci,id=xhci
-device pcie-root-port,bus=pcie.0,slot=1,x-speed=16,x-width=32
...
)
```

</details>

<details><summary><h5>What do you mean by "scripts" and "configs"?</h5></summary>

When the project mentions "scripts", it means either *the Python files used to run the program*, or *the user-generated shell scripts used to boot a virtual machine.*

When the project mentions "configs", it's typically referring to *files generated by AutoPilot*, in the form of shell scripts ending in ``.sh``. These were generated based on your specific configuration, hence the naming. 

</details>

<details><summary><h5>How do I enable/disable Discord rich presence?</h5></summary>

To show off your AutoPilot progress or virtual machine status on your Discord profile, you have to enable **Discord rich presence**.

> [!NOTE]
> You must have the ``pypresence`` dependency installed. This can be done via a system wide package, ``python-pypresence``, or by using ``pip install pypresence`` for external environments.

The project will detect whether or not this is installed when you run AutoPilot, and marks the generated script accordingly. If you create an AutoPilot script with the dependency installed, your generated script will automatically have Discord rich presence enabled, and you don't have to do anything.

If you install the dependency **after** generating a script - don't worry, it's still easy to enable. Simply open your generated boot script, and look at the ULTMOS variable block. Find the following line:

```sh
DISCORD_RPC=0
```

To enable rich presence, change ``0`` to ``1``, and vice versa to disable it.

If you don't want to show your status when running AutoPilot itself, you can manually run the AutoPilot script with a disable argument:

```sh
$ ./scripts/autopilot.py --disable-rpc
```

</details>

<details><summary><h5>I'm here for GPU (or any PCI) passthrough!</h5></summary>

Great! The project can assist you with this too.

There's a built-in tool called the **VFIO-PCI Passthrough Assistant**, which - similarly to *AutoPilot* - guides you through the process of configuring your devices for VFIO-PCI passthrough.

The full guide for this tool and passthrough in general can be found [here](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Passthrough).

</details>



<details><summary><h5>What's inside all the folders?</h5></summary>

Well, fun stuff, but there's some that you shouldn't touch unless you'd like to help improve the project. 

Everything in the ``resources`` folder should be left alone, as the project needs the stuff in here to function properly. Editing or misplacing these files will likely break the project. If you think this has happened by accident or through your reckless behaviour, you can use the built in restoration script to restore the project files back to their working state, without losing your data or having to re-clone the repository. Don't worry, your stupidity is safe with me.

The files in the aptly-named ``scripts`` folder are, well, the scripts themselves. Same principle as the `resources` folder - no touchy unless you know how to touchy.

Files in the ``boot`` folder are generated after running AutoPilot. They consist of the OpenCore boot image and its unpackaged files. You can't really edit these even if you wanted to, except from the OpenCore image, which **you should do** from within macOS. A guide on this can be found [here](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/OpenCore).

The ``blobs`` folder contains nothing until AutoPilot is run. This is where AutoPilot stores your choices, instead of using variables. This way, if the process is interrupted for some reason, it can be resumed using the existing files. The contents of these files may also be dictated by an *AutoPilot preset* that you loaded. Do NOT delete the blobs in the ``user`` folder, as these are accessed by other areas of the project. The blobs in the ``stale`` folder are unused and are stored simply in case the user wants to back them up, but can be safely deleted at any time.

The ``roms`` folder contains one example GPU VBIOS (AMD Radeon RX 550 Sapphire Pulse), and any other you've used or dumped with the project. If you supply a ROM file in the VFIO-PCI passthrough assistant for example, it will be copied from its original location to this folder for use with QEMU. The original ROM file is not touched. If you use the built-in VBIOS dump tool, the output file is also placed in this folder automatically. You may need to patch a GPU's VBIOS, and this can be done to any ROM file in this folder directly if you wish. The files in this folder can be safely deleted as long as they are no longer used by a script you've made with AutoPilot. If you don't use passthrough, this folder isn't relevant to you.

The ``ovmf`` folder is also populated only after running AutoPilot. This folder holds the OVMF boot code file, and your customised OVMF variable file - holding information such as boot order, screen resolution, etc. The files in here have a tendancy to become unusable after heavy usage, but this can be easily resolved. However, do **NOT** remove or replace the files yourself. Use the built-in OVMF restore tool, which can be accessed from the main menu.

Oh, hi mum! I'm on the ``docs`` folder! Well, there's not much to this one as you've evidently already found it, but this folder contains several useful(?) documents surrounding both the project itself and other aspects of using KVM. If you find the way I write documents fills you with a burning hatrid-filled rage, you can delete these files if you want... But, I'll know. I'm like Santa- always watching.

And finally, the ``internal`` folder. If you see this, run. You shouldn't have it. Oh and by the way, I'll know if you do. ;)

</details>

<details><summary><h5>Can I edit the boot config I made with AutoPilot?</h5></summary>

Yes, you can. AutoPilot is designed to create a new boot script based on your preferences, but you may desire to change these over time without using AutoPilot again, and it has been designed to allow you to do so. 

The values that can be safely changed by the user are all placed at the top of the generated boot script, like this:

```sh
ALLOCATED_RAM="8G"
CPU_SOCKETS="1"
CPU_CORES="2"
CPU_THREADS="4"
CPU_MODEL="host"
CPU_FEATURE_ARGS="+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"
```

As you can see, the values you would have chosen during AutoPilot are inserted into each argument as a string. You can edit the value inside the string (i.e. "8G"), but do **NOT** edit the variable itself (i.e. ALLOCATED_RAM=). In this example, if you wanted to change the virtual RAM from 8 GB to 16 GB, you'd change

```sh
ALLOCATED_RAM="8G"
``` 

to

```sh
ALLOCATED_RAM="16G"
```

and this would take effect in the VM's configuration the next time it is run.

Anything below the variables should not be changed, except the designated lines used to attach the macOS recovery image to the VM, or the lines used to enable VNC. You can remove these lines after you've installed macOS, which will stop "macOS Base System" from appearing in your boot menu. To do this, remove the following lines from your config file:

```sh
############## REMOVE THESE LINES AFTER MACOS INSTALLATION ###############
-drive id=BaseSystem,if=none,file="/home/aaaaaaa/sexytime/BaseSystem.dmg",format=raw
-device ide-hd,bus=sata.4,drive=BaseSystem
##########################################################################
```

> [!NOTE]
> You may prefer to comment-out the lines instead, in case you need to re-attach the base system image again later.

</details>

<details><summary><h5>Can I use VNC?</h5></summary>

If you would prefer to connect to the virtual display using VNC, you can do so! The virtual machine can open a virtual display as a VNC server, running on port ``5900`` of your local host. Uncomment the ``-vnc`` line (remove the # at the start) of your boot config file to enable this:

```sh
################ UNCOMMENT IF YOU WANT TO USE VNC MONITOR ################
-vnc 0.0.0.0:1,password=on -k en-us
##########################################################################
```

You can then connect to the virtual machine's display using a VNC client, at ``127.0.0.1:5900``, or even remotely using your local/external IP. If you want to connect from outside your network, please make sure you have all the necessary security and hardening before doing this. Basically; don't let me sneak in.

</details>

***
I hope you liked reading this document and found it somewhat useful (and maybe even funny). Eversiege watched me write it and liked it, so it's obviously good.

***

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ef278407-a14f-4ae7-bc23-3f635687db65" width="25%"> 

<sub>Written and maintained by **Coopydood**. </sub>
<br><sub>You can [contribute](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs) to documentation, too!</sub>