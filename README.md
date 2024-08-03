<a href="https://coopydood.github.io/ultimate-macOS-KVM"><img src="https://github.com/Coopydood/ultimate-macOS-KVM/blob/492731ef1d95d2da534c660b001550f4d76a6c68/resources/images/bannerAlphaBasic.png?raw=true" alt="ultimate-macOS-KVM" width="500"/></a>

### v0.12.2

Helping you build the ultimate macOS virtual machine, powered by KVM.

**[What's new?](https://github.com/Coopydood/ultimate-macOS-KVM/releases/latest)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;**[Switch to dev branch... ⎋](https://github.com/Coopydood/ultimate-macOS-KVM/tree/dev)

<br>

[![ULTMOS VERSION](https://img.shields.io/github/v/release/Coopydood/ultimate-macOS-KVM?style=for-the-badge&color=1793D1&logo=github&logoColor=white&label=)](https://github.com/Coopydood/ultimate-macOS-KVM/releases/latest) [![GitHub](https://img.shields.io/github/license/Coopydood/ultimate-macOS-KVM?label=Licence&logo=unlicense&logoColor=white&style=for-the-badge)](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/LICENSE) [![GitHub repo size](https://img.shields.io/github/repo-size/Coopydood/ultimate-macOS-KVM?color=07b55b&label=Size&logo=envoy-proxy&logoColor=white&style=for-the-badge)](https://github.com/Coopydood/ultimate-macOS-KVM) [![Discord](https://img.shields.io/discord/574943603466436628?color=7d86ff&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/WzWkSsT)

***

<img align="left" width="100" height="100" src="https://github.com/user-attachments/assets/7b9b72ee-5a89-49b4-ae17-7a188ed533ab">
<img align="left" src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/8f69f9b9-cf23-4e8b-adf3-95862a23e2ba" height=153 width=2 />

<h3>macOS Sequoia Support<br><sub>Available Now</sub></h3>

macOS Sequoia has not yet been tested extensively, but it has been **confirmed to install and boot with the current version of ULTMOS** on the latest macOS developer beta.

<br>

**AutoPilot now has an additional option for macOS Sequoia beta!** <br>Please feel free to try out the macOS Sequoia beta with ULTMOS and leave feedback on how it went! 

However, you should **NOT** use macOS Sequoia as your main virtual setup - and should be used for test purposes only. You have been warned!

You can download the latest recovery image below for use with AutoPilot. The file is hosted on the [Archive.org website](https://archive.org/details/macos-sequoia).

<br>

<p align="center"><a href="https://archive.org/download/macos-sequoia/Latest/BaseSystem.dmg"><img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/a8f1cb8f-5ddd-45cc-8598-032180035607" height="38"></a><br><sub> <b>BaseSystem.dmg</b> (1.3 GB)<br>Or, you can also download the <a href="https://archive.org/download/macos-sequoia/macos-sequoia_archive.torrent">torrent</a>.</sub></p>

***

## 👋》Introduction

Tired of all the restraints and poor performance of macOS VMs in hypervisors like VirtualBox or VMware? Well, the story changes when you run your virtual machines in **kernel space**. Welcome to the world of **K**ernel **V**irtual **M**achines.

You might be new to QEMU/KVM, or a long-time veteran - either way, this project aims to help you build a macOS virtual machine that can take full advantage of the power of KVM - but in a user-friendly and approachable way.

Scripts? Configs? QEMU arguments? A *"qcow"* file? *Moo?* If you need a little help wrapping your head around this stuff, feel free to check out the [FAQs](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/FAQs) for some quick knowledge on the basics.

<br>
<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/0205f5fe-9278-4f8f-8d5c-d3707f695f52" alt="ultimate-macOS-KVM" width="1400"/>

<br>
<p align="center"><i>The latest macOS Sequoia beta running on ULTMOS.</i></p>

***

## 💎》Features

<ul>
<li><b>Modern macOS Support <a href="https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Supported-Guest-OSes">⎋</a></b></li> 
Experience the latest macOS has to offer with built-in support from macOS High Sierra to macOS Sonoma, and even try out the latest macOS Sequoia beta!

<li><b>AutoPilot <a href="https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot">⎋</a></b></li> 
Automatically generates a valid, customised, and ready-to-use QEMU config script in seconds.

<li><b>VFIO-PCI Passthrough Assistant <a href="https://github.com/Coopydood/ultimate-macOS-KVM/wiki/VFIO%E2%80%90PCI-Passthrough-Assistant">⎋</a></b></li>
Advanced passthrough tinkering made easy with auto-detection and configuration walkthroughs.

<li><b>USB Passthrough Assistant</b></li>
Allows you to select any of your host's attached USB devices for use with the macOS guest, and automatically configures them.

<li><b>OpenCore Configuration Assistant</b></li>
Automatically mount and edit your OpenCore image from your host, using Network Block Devices.

<li><b>GenSMBIOS Integration</b></li>
Auto-generate a new SMBIOS and serial number directly onto the virtual OpenCore image with full GenSMBIOS + ULTMOS integration.

<li><b>Boot Argument Assistant + AutoPatch</b></li>
Easily edit the macOS boot arguments of your OpenCore image, and even automatically apply relevant patches for your setup (e.g. AMD RX 5000 series black screen patch).

<li><b>Automatic System Checks</b></li>
Several check scripts can be used to make sure your system is correctly prepared for both passthrough and non-passthrough KVM.

<li><b>GPU Compatibility Checker</b></li>
Detects GPUs in your host system and checks them against a list of known compatible and incompatible macOS GPUs, providing a summary including any extra card-specific quirks.

<li><b>VFIO-IDs and IOMMU Helpers</b></li>
Auto-detects and lists IOMMU groups, VFIO-IDs, and checks if devices are stubbed to kernel driver correctly.

<li><b>Convert to XML for virt-manager <a href="https://github.com/Coopydood/ultimate-macOS-KVM/wiki/XML-Converter">⎋</a></b></li>
Easily convert any AutoPilot-generated QEMU scripts into an importable XML file for virt-manager (GUI). VFIO-PCI passthrough and USB configurations are also converted.
</ul>

> [!TIP]
> Click the [**⎋**]() icon next to a feature to read more about it in greater detail.



<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ac766b58-5e66-4b70-9742-8e318f065fc2" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ee451491-35fa-436e-957b-888d2f7d488e" width="45%"></img>

***

## 🎲》Requirements

As with all other virtual machines / hypervisors, you don't need an *uber-powerful* PC, but you should expect guest performance to be relative to your host's. Performance *can* change dramatically based on guest properties, such as virtual cores, allocated memory, and virtual CPU threads - but it really does boil down to how beefy your host's hardware is.

Here's a table with my best judgment on minimum, recommended, and best system requirements:


|                 |                   **Minimum**                  |                           **Recommended**                          |                                 **Optimal**                                 |                                   My Setup                                   |
|-----------------|:----------------------------------------------:|:------------------------------------------------------------------:|:---------------------------------------------------------------------------:|:----------------------------------------------------------------------------:|
| **OS**          |                    linux-5.x                   |                             Linux Mint                             |                                  Arch Linux                                 |                                  Arch Linux                                  |
| **Motherboard** |             Virtualisation<br>UEFI             |        Virtualisation<br>UEFI<br>IOMMU<br>Intel VT-d / AMD-V       | Virtualisation<br>UEFI<br>IOMMU<br>Intel VT-d / AMD-V<br>Isolated PCI Lanes | ROG STRIX Z490-E GAMING<br>UEFI<br>IOMMU<br>Intel VT-d<br>Isolated PCI lanes |
| **CPU**         | ~2014 Intel / AMD<br>Virtualisation<br>2 cores | Intel i5 / Ryzen 5<br>Virtualisation<br>4-8 cores<br>Hyperthreaded |     Intel i9 / Ryzen 9<br>Virtualisation<br>8-16 cores<br>Hyperthreaded     |               Intel Core i9-10900K<br>10 cores<br>Hyperthreaded              |
| **Memory**      |                      4 GB                      |                                16 GB                               |                                    32 GB+                                   |                               64 GB                              |
| **Disk Type**   |                    SATA HDD                    |                              SATA SSD                              |                                   NVMe SSD                                  |                               NVMe SSD                               |
| **Disk Space**  |                      40 GB                     |                               120 GB                               |                                   500 GB+                                   |                                    500 GB                                    |
| **Resolution**  |                    1280x720                    |                              2560x1440                             |                                  3840x2160                                  |                               2560x1440                              |
| **GPU (VFIO)**  |                        -                       |                             AMD RX 580                             |                                AMD RX 6600 XT                               |                                  AMD RX 5700 XT                                  |

> [!NOTE]
> The recommended and optimal specifications are for reference only.


<details><summary><h4>macOS Guest Feature Support Matrix</h4></summary>

|                          	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/bd4a791d-1ac2-4a9a-8ee0-22e4d5f88cd3"> | <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/184bb2ef-c447-4cbd-b07c-8b4b096e3944">     	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/cd8029e8-c256-4295-9908-37809d64dcfe">     	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/79a7a051-0f5a-419e-8544-b51b1572d3b9">     	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/7d341cce-4370-4430-b3d5-bf1868afe4a3">     	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/4829ebb4-ce7f-4ecf-8309-d691c9361f6b">     	| <img align="center" width="35" height="35" src="https://github.com/Coopydood/OpenCore-Z490E-CometLake/assets/39441479/aa49b5ba-6cca-4dab-bcfc-6bf21909e738">      	| <img align="center" width="35" height="35" src="https://github.com/user-attachments/assets/7b9b72ee-5a89-49b4-ae17-7a188ed533ab">      	|
|--------------------------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:---------:|:---------:|
|            **AutoPilot** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|     **Auto<br>Download** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✕    	|
|    **Online<br>Install** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|   **Offline<br>Install** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
|       **QEMU<br>Script** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓¹   	|    ✓¹    	|    ✓¹    	|
|      **Virt<br>Manager** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ?²  	|    ?²   	|    ?²   	|
|   **GPU<br>Passthrough** 	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓¹   	|    ✓¹    	|    ✓¹    	|
| **VirtIO<br>Networking** 	|    ✕   	|    ✕   	|    ?³   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|
| **VirtIO<br>Storage** 	|    ✕   	|    ✕   	|    ✓   	|    ✓   	|    ✓   	|    ✓   	|    ✓    	|    ✓    	|


¹ <sup>If trying to boot macOS Ventura and later with GPU passthrough, you may need to do so using Virtual Machine Manager. The QEMU script may have issues with GPU passthrough.<sup>

² <sup>macOS Ventura and later have been known to have issues booting    *without* GPU passthrough in Virtual Machine Manager.</sup>

³ <sup>I have no idea whether or not VirtIO networking works on macOS Catalina.</sup>

<br>

> [!NOTE]
> This table is a very **loose** representation of the current state of macOS versions and their support with ULTMOS / QEMU / KVM. It's more for reference and shouldn't be taken seriously.
>
> If you find something is wrongly marked, please feel free to update it.
</details>


***

## 📦》Dependencies
The project requires several other packages to function properly, while others can be optionally installed to enhance your experience. 

All of the dependencies, both required and optional, are listed below.

> [!IMPORTANT]
> The package names listed below are examples on an Arch-based system. Your distro may be different!

<b>Required</b>
<ul>
<li><b>Sudo</b> 》 <code>sudo</code></li>
<li><b>Git</b> 》 <code>git</code></li>
<li><b>Wget</b> 》 <code>wget</code></li>
<li><b>QEMU</b> 》 <code>qemu-full</code></li>
<li><b>Libvirt</b> 》 <code>libvirt</code></li>
<li><b>DNSmasq</b> 》 <code>dnsmasq</code></li>
<li><b>Python</b> 》 <code>python</code></li>
</ul>
<b>Optional</b>
<ul>
<li><b>Virtual Machine Manager (GUI)</b> 》 <code>virt-manager</code></li>
<li><b>Virsh</b> 》 <code>virsh</code></li>
<li><b>Discord Rich Presence (pypresence)</b> 》 <code>python-pypresence</code> or, using pip, install <code>pypresence</code></li>
<li><b>Network Block Device (NBD)</b> 》 <code>nbd</code> required for mounting the OpenCore image for editing on host system
</ul>

> [!WARNING]
> You **must** have all of the required dependencies installed before using this project. 

>[!NOTE]
> As of [v0.12.0](https://github.com/Coopydood/ultimate-macOS-KVM/releases/tag/v0.12.0), some libraries, such as ``pypresence``, are bundled with the project by default and require no further user action or installation.

> [!TIP]
> Optional dependencies can enhance your experience, such as using your VM in a GUI, or showing what macOS version you're currently running on your Discord profile.
>
> Your experience is automatically adapted based on the dependencies you have installed. For example, if you have ``pypresence`` installed, Discord rich presence will be enabled automatically on AutoPilot scripts.

***

## 🐧》Oh, and you NEED Linux.

Shocker; KVM is a module built into the *Linux kernel*, not **Windows Subsystem for Linux** or some UNIX-like terminal. You need a <ins>full install</ins> of at least base Linux **on your host**. Don't try any of that VM inception shenanigans.

The easiest way to do this is by grabbing some mainstream Linux distro, like **Ubuntu, Linux Mint, Manjaro, EndeavourOS** - among many, many others. You can theoretically pick any one you like. *I use Arch BTW.*

> [!NOTE]
> Testing of ULTMOS on different distrobutions is underway - but please note that is has been primarily developed and tested on **Arch** and **Debian**-based systems.

***

## 🛫》Getting Started

It's easy to get up and running. Simply clone the repo using ``git``.
Make sure you have **all** [dependencies](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/README.md#requirements) installed before getting started.

```sh
git clone https://github.com/Coopydood/ultimate-macOS-KVM
```

> [!TIP]
> Alternatively, you can download the latest release [here](https://github.com/Coopydood/ultimate-macOS-KVM/archive/refs/heads/main.zip).

<br>

Okay, so you've cloned my repo, and `cd`'d into the directory. Great!
Now, before running the script - and to avoid the subsequent and inevitable gotcha - you should enable the ``libvirtd`` daemon first if it hasn't been already. Here's an example for Arch-based systems:

```sh
sudo systemctl enable libvirtd
```
> [!WARNING]
> This command requires superuser privileges.

<br>

and/or check the status of the daemon with

```sh
systemctl status libvirtd
```

***

## 🧭》Usage

Okay, now you're ready to use **ultimate-macOS-KVM**. Use the ``main.py`` file.

This is your main menu / central hub for the project and everything can be accessed from here. 

```sh
./main.py
```
> [!CAUTION]
> Most sub-scripts included in the project should *not* be run on their own. Always use ``main.py`` unless the script was user-generated or stated otherwise.

***

## 🖥️》I'm here for GPU passthrough

...and you've come to the right place. ultimate-macOS-KVM includes several handy built-in tools to make VFIO-PCI passthrough (including GPUs) as pain-free as possible. Please see the documentation on how to get started with these tools.

> [!TIP]
> If you're looking for single GPU passthrough, DarknessRafix has an *excellent* guide that walks you through the process of setting this up using ULTMOS. You can read it [here](https://gitlab.com/DarknessRafix/macosvmgpupass).

Oh, and speaking of...

***

## 📖》Documentation

More detailed write-ups on the project and the scripts included, as well as some tutorials can be found on this [repo's wiki](https://github.com/Coopydood/ultimate-macOS-KVM/wiki).

This is continually updated and made better as the project develops. Feel free to help out and [write your own!](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs)

Changelogs can be found on the [releases](https://github.com/Coopydood/ultimate-macOS-KVM/releases) page.

> [!TIP]
> All documentation and changelogs are included in the [docs folder](https://github.com/Coopydood/ultimate-macOS-KVM/tree/main/docs) for offline reading.

***

## 🛟》Help and Troubleshooting

Alongside the tutorial and explanation documents, this project includes troubleshooting guides for a wide variety of issues - ranging from project issues such as those in *AutoPilot*, or other issues such as GPU passthrough.

You can search for your problem and find solutions in the [**Issues and Troubleshooting**](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Issues-and-Troubleshooting) section of the project wiki.

> [!NOTE]
> If an unexpected problem with the ULTMOS project itself arises, it may be a bug, and can be reported [here](https://github.com/Coopydood/ultimate-macOS-KVM/issues/new).

***

## ⬇️》Updates

This project has been designed to be updated and made better over time.

As you use it to generate your personal files, having to re-clone the entire repo yourself while preserving your files would be a right pain in the backside. Therefore, there's an automated updater script built right in that you can use to safely update in-place to newer versions of this project, without affecting any of your personal config files, virtual hard drives, or anything else not part of the project files. And, if an update dramatically changes directory structures from your current version, the updater automatically disables its in-place update mechanism to prevent data loss.

Of course, if you're just testing the project, then a "clean install" is probably still preferable.

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/b3578d2d-3d31-41a6-a7f0-85a857ef1f5b" width="60%"></img>

***

## 🖼️》Gallery

Here's a few screenshots showing **ultimate-macOS-KVM** in action!

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/34ef4e38-557b-491f-9c3b-a57c9f03b81d" width="90%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/aedd04b6-3334-482d-adbe-d3809238a652" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/593e8388-8b2d-4b12-99b4-1dbd7802dea8" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/a7a60115-865a-4939-ab8f-e726a3d488a6" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/1802c1d2-7d35-4e70-9ab2-13820ef7e3a9" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/1fd0add5-c0c8-46a1-8897-3b80c37f98a1" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/8380632b-dceb-41e7-acb0-b2bd15cbf575" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/b32c2701-a934-42ce-ab69-06b1ae350f1b" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ee451491-35fa-436e-957b-888d2f7d488e" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/c4e394c3-a666-4aab-9aa7-b40b1e84d977" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/feb19dce-7a9a-4527-884c-8b2f2d445e2f" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/4a8b5249-3029-49d3-8539-229b3c179816" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/4e7678f3-5ee4-4e69-93a7-d9ba9881cea7" width="45%"></img>
<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/dd012a63-415a-4b87-b096-feabdd3f8a5e" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/32d2992d-a39a-4b34-976b-5e7ee5d5c926" width="45%"></img> 

> [!TIP]
> More screenshots of ULTMOS in action can be found included in the [docs](https://github.com/Coopydood/ultimate-macOS-KVM/tree/main/docs/screenshots) folder!

***

## ☢️》Disclaimer

This is my way of giving back to the QEMU, KVM, and VFIO community. Please don't expect much as this is a passion project and not a priority in my life.

- I'm not responsible for any time you waste using this project.
- I'm not responsible if you make an oopsie whoopsie.
- I have no affiliation with OpenCore and have no developmental experience with it.
- Expect headaches. Some severe.
- You need a LOT of patience. I mean it. Despite me trying to alleviate some of the hassles, you WILL run into [stupid gotchas](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Issues-and-Troubleshooting) that require trial and error out of my control.
- I'm by no means an expert on this stuff nor would I claim to be.
- I've simply made *what I had to go through **easier** for you*. Hopefully.
- Yes, my Python is pretty bad. But if it works, it works.

> [!CAUTION]
> Do NOT run anything as ``sudo`` unless absolutely necessary. If you have an urge to then you need to break that habit _**asap.**_ <br><br>
> Most of my scripts do not require superuser privileges, however, the ones that do are clearly marked with a yellow ⚠️ next to the operation requiring such permissions.
  
***

## ⚖️》Legal

> [!WARNING]
> This project contains a string of text known as an OS Key (OSK). 

Apple uses this key to make it more difficult for non-Macintosh computers to run macOS, by requiring the key to be provided by the SMBIOS. 

This OS key is widely available on the Internet and is no longer considered a "secret", and was even included in a [public court document](http://www.rcfp.org/sites/default/files/docs/20120105_202426_apple_sealing.pdf).

Apple has attempted to classify the OSK as a trade secret but has ultimately failed in doing so. As a result, it is freely included within this project, as with [OSX-KVM](https://github.com/kholia/OSX-KVM).

***

## ❤️》Sponsors

These awesome people were generous enough to donate financially to help fuel the 3AM misadventures this project is made from. Thank you so much!

<!-- sponsors --><a href="https://github.com/WaveringAna"><img src="https://images.weserv.nl/?url=https://github.com/WaveringAna.png?v=1&h=100&w=100&fit=cover&mask=circle&maxage=7d" height="50px" width="50px" alt="WaveringAna"></a><a href="https://github.com/SaRoKu"><img src="https://images.weserv.nl/?url=https://github.com/SaRoKu.png?v=1&h=100&w=100&fit=cover&mask=circle&maxage=7d" height="50px" width="50px" alt="SaRoKu"></a><!-- sponsors -->

<br><br>
<sup>If you find this project helpful, and want to support development, you can <a href="https://github.com/sponsors/Coopydood">sponsor it</a>! Any and all donations are incredibly appreciated and never expected or required! </sup>

***

<img align="left" width="100" height="100" src="https://dortania.github.io/docs/latest/Logos/Logo.png">

<h3>Powered by OpenCore<br><sub>Version 0.9.7</sub></h3>

This project would not be possible without the incredible work of the [OpenCore development team](https://github.com/Acidanthera). Thank you to everyone involved! ❤️


***

## 🤝》Credits & Greetz

While I am the creator of these automation/ease-of-use scripts, this project is not possible without both the prior and current works of some very talented people. The people who have tested the project are also included.

- **[Dortania](https://github.com/Dortania)** 》 Extensive documentation and Hackintosh development.
- **[Kholia](https://github.com/kholia)** 》 Development of scripts and documentation. ultimate-macOS-KVM is intended as an extension to [OSX-KVM](https://github.com/kholia/OSX-KVM).
- **[thenickdude](https://github.com/thenickdude)** 》 Personal support throughout my KVM misadventures and countless community contribs.
- **[vit9696](https://github.com/vit9696)** 》 Author of many macOS hacks including kexts, and other source material used in this project. Probably knows the macOS boot process better than Apple.
- **[vu1tur](to@vu1tur.eu.org)** 》 Open source dmg to img conversion tool; used and bundled in this project.
- **[Eversiege](https://github.com/eversiege)** 》 Support and testing, та мій улюблений українець. Also made the project's main [website](https://coopydood.github.io/ultimate-macOS-KVM).
- **[CyberneticSquid](https://github.com/cyberneticsquid)** 》 Testing for me at stupid-o'-clock because he's a cool Aussie.
- **[Cake](https://github.com/cam-jm)** 》 Another Aussie testing for me in the middle of my sleep-deprived nights, with a slight obsession over cake.
- **[Hyperchromiac](https://github.com/hyperchromiac)** 》 My personal constitution-munching American. Legend has it that I live in his attic, although even I'm not sure. Love this guy either way.
- **[Kaz](https://github.com/Eaz11)** 》 Other than his brilliant English accent's pronunciations (including "macOS Syria"), he's done extensive testing. Say hi to your nephew for me.
- **[GigantTech](https://twitter.com/TechGigant)** 》 Moderately annoying German guy that I convinced to install Linux subsequently letting him test my project. It's free real estate!
- **[Hummenix](https://github.com/Hummenix)** 》Testing of ULTMOS across different Linux distros. 
- **[CorpNewt](https://github.com/CorpNewt)** 》Creator of GenSMBIOS and many other Hackintosh essentials.
- **[Acidanthera](https://github.com/Acidanthera)** 》The group behind OpenCore, Lilu, WhateverGreen, and MUCH more.
- **[DarknessRafix]()** 》Extensive testing of the project and the author of some excellent ULTMOS guides! Oh, and was the very first person to install macOS Sequoia on ULTMOS - even before me.

***



<p align="center">
  <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/39d78d4b-8ce8-44f4-bba7-fefdbf2f80db" width="10%"> </img>
</p>
