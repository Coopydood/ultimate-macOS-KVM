<a href="https://coopydood.github.io/ultimate-macOS-KVM"><img src="https://github.com/Coopydood/ultimate-macOS-KVM/blob/492731ef1d95d2da534c660b001550f4d76a6c68/resources/images/bannerAlphaBasic.png?raw=true" alt="ultimate-macOS-KVM" width="500"/></a>

### v0.10.4

Helping you build the ultimate macOS virtual machine, powered by KVM.

*[What's new?](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-10-4.md)*

[![ULTMOS VERSION](https://img.shields.io/github/v/release/Coopydood/ultimate-macOS-KVM?style=for-the-badge&color=1793D1&logo=github&logoColor=white&label=)](https://github.com/Coopydood/ultimate-macOS-KVM/releases/latest) [![GitHub](https://img.shields.io/github/license/Coopydood/ultimate-macOS-KVM?label=Licence&logo=unlicense&logoColor=white&style=for-the-badge)](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/LICENSE) [![GitHub repo size](https://img.shields.io/github/repo-size/Coopydood/ultimate-macOS-KVM?color=07b55b&label=Size&logo=envoy-proxy&logoColor=white&style=for-the-badge)](https://github.com/Coopydood/ultimate-macOS-KVM) [![Discord](https://img.shields.io/discord/574943603466436628?color=7d86ff&label=Discord&logo=discord&logoColor=white&style=for-the-badge)](https://sl.coopydood.com/discord)

***

## Introduction

Tired of all the restraints and poor performance of macOS VMs in hypervisors like VirtualBox or VMware? Well, the story changes when you run your virtual machines in **kernel space**. Welcome to the world of **K**ernel **V**irtual **M**achines.

You might be new to QEMU/KVM, or a long-time veteran - either way, this project aims to help you build a macOS virtual machine that can take full advantage of the power of KVM - but in a user-friendly and approachable way.

Scripts? Configs? QEMU arguments? A *"qcow"* file? *Moo?* If you need a little help wrapping your head around this stuff, feel free to check out the [FAQs](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/FAQs) for some quick knowledge on the basics.

<br>
<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/1244b64e-95b2-469a-8271-43c56e72b065" alt="ultimate-macOS-KVM" width="1400"/>
<p align="center"><i>SussyMac v2.0 - Full virtual Hackintosh setup powered by ULTMOS.</i></p>

***

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

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ac766b58-5e66-4b70-9742-8e318f065fc2" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ee451491-35fa-436e-957b-888d2f7d488e" width="45%"></img>

***

## Requirements

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

***

## Dependencies
The project requires several other packages to function properly, while others can be optionally installed to enhance your experience. 

All of the dependencies, both required and optional, are listed below.

<b>Required</b>
<ul>
<li><b>Git</b> 》 <code>git</code></li>
<li><b>Wget</b> 》 <code>wget</code></li>
<li><b>QEMU</b> 》 <code>qemu-base</code> / <code>qemu-full</code></li>
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

> [!NOTE]
> Optional dependencies can enhance your experience, such as using your VM in a GUI, or showing what macOS version you're currently running on your Discord profile.
>
> Your experience is automatically adapted based on the dependencies you have installed. For example, if you have ``pypresence`` installed, Discord rich presence will be enabled automatically on AutoPilot scripts.

***

## Oh, and you NEED Linux.

Shocker; KVM is a module built into the *Linux kernel*, not **Windows Subsystem for Linux** or some UNIX-like terminal. You need a <ins>full install</ins> of at least base Linux **on your host**. Don't try any of that VM inception shenanigans.

The easiest way to do this is by grabbing some mainstream Linux distro, like **Ubuntu, Linux Mint, Manjaro, endeavourOS** - among many, many others. You can pick any one you like. If it's Linux - you can use this project. *I use Arch BTW.*

> [!NOTE]
> Running this on Windows or macOS is as pointless as those ice cube dispensers on fridge doors...

***

## Getting Started

It's easy to get up and running. Simply clone the repo using ``git``.
Make sure you have **all** [dependencies](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/README.md#requirements) installed before getting started.

```sh
$ git clone https://github.com/Coopydood/ultimate-macOS-KVM
```

> [!NOTE]
> Alternatively, you can download the latest release [here](https://github.com/Coopydood/ultimate-macOS-KVM/archive/refs/heads/main.zip).

Okay, so you've cloned my repo, and `cd`'d into the directory. Great!
Now, before running the script - and to avoid the subsequent and inevitable gotcha - you should enable the ``libvirtd`` daemon first if it hasn't been already. Here's an example for Arch-based systems:

```sh
$ sudo systemctl enable libvirtd
```
> [!WARNING]
> This command requires superuser priviledges.

and/or check the status of the daemon with

```sh
$ systemctl status libvirtd
```

***

## Usage

Okay, now you're ready to use **ultimate-macOS-KVM**. Use the ``main.py`` file.

This is your main menu / central hub for the project and everything can be accessed from here. 

```sh
$ ./main.py
```
> [!IMPORTANT]
> Most sub-scripts included in the project should *not* be run on their own.

***

## I'm here for GPU passthrough

...and you've come to the right place. ultimate-macOS-KVM includes several handy built-in tools to make VFIO-PCI passthrough (including GPUs) as pain-free as possible. Please see the documentation on how to get started with these tools.

Oh, and speaking of...

***

## Documentation

More detailed write-ups on the project and the scripts included, as well as some tutorials can be found on this [repo's wiki](https://github.com/Coopydood/ultimate-macOS-KVM/wiki).

This is continually updated and made better as the project develops. Feel free to help out and [write your own!](https://github.com/Coopydood/ultimate-macOS-KVM/new/main/docs)

Or, you can find some in the included [docs folder](https://github.com/Coopydood/ultimate-macOS-KVM/tree/main/docs).

***

## Help and Troubleshooting Issues

Alongside the tutorial and explanation documents, this project includes troubleshooting guides for a wide variety of issues - ranging from project issues such as those in *AutoPilot*, or other issues such as GPU passthrough.

You can search for your problem and find solutions in the [**Issues and Troubleshooting**](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Issues-and-Troubleshooting) section of the project wiki.

> [!NOTE]
> If an unexpected problem with the ULTMOS project itself arises, it may be a bug, and can be reported [here](https://github.com/Coopydood/ultimate-macOS-KVM/issues/new).

***

## Updates

This project has been designed to be updated and made better over time.

As you use it to generate your personal files, having to re-clone the entire repo yourself while preserving your files would be a right pain in the backside. Therefore, there's an automated updater script built right in that you can use to safely update in-place to newer versions of this project, without affecting any of your personal config files, virtual hard drives, or anything else not part of the project files. And, if an update dramatically changes directory structures from your current version, the updater automatically disables its in-place update mechanism to prevent data loss.

Of course, if you're just testing the project, then a "clean install" is probably still preferable.

***

## Gallery

Here's a few screenshots showing **ultimate-macOS-KVM** in action!

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/02c6abd3-40b3-416b-ba1f-5979314ad2f9" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/8712cc11-e352-40ba-9373-d0da13c4bd89" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/5fa35111-1559-42d5-b8d2-87aa35d64489" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/1c10c6e0-263d-409c-996e-2d0fc5cf1287" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/232f3bae-b31b-4e18-bee9-8c03a472d5a0" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ac766b58-5e66-4b70-9742-8e318f065fc2" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/1fd0add5-c0c8-46a1-8897-3b80c37f98a1" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/8380632b-dceb-41e7-acb0-b2bd15cbf575" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/b32c2701-a934-42ce-ab69-06b1ae350f1b" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ee451491-35fa-436e-957b-888d2f7d488e" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/c4e394c3-a666-4aab-9aa7-b40b1e84d977" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/feb19dce-7a9a-4527-884c-8b2f2d445e2f" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/4a8b5249-3029-49d3-8539-229b3c179816" width="45%"></img> <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/4e7678f3-5ee4-4e69-93a7-d9ba9881cea7" width="45%"></img> 

***

## Disclaimer

This is my way of giving back to the QEMU, KVM, and VFIO community. Please don't expect much as this is a passion project and not a priority in my life.

- I'm not responsible for any time you waste using this project.
- I'm not responsible if you make an oopsie whoopsie.
- Do NOT run anything as ``sudo`` unless absolutely necessary. If you have an urge to then you need to break that habit _**asap.**_ Most of my scripts do not require superuser privileges, however, the ones that do are clearly marked with a yellow ⚠️ next to the operation requiring such permissions.
- Expect headaches. Some severe.
- You need a LOT of patience. I mean it. Despite me trying to alleviate some of the hassles, you WILL run into [stupid gotchas](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/Issues-and-Troubleshooting) that require trial and error out of my control.
- I'm by no means an expert on this stuff nor would I claim to be.
- I've simply made *what I had to go through **easier** for you*. Hopefully.
- Yes, my Python is pretty bad. But if it works, it works.
  
***

## Legal

> [!WARNING]
> This project contains a string of text known as an OS Key (OSK). 

Apple uses this key to make it more difficult for non-Macintosh computers to run macOS, by requiring the key to be provided by the SMBIOS. 

This OS key is widely available on the Internet and is no longer considered a "secret", and was even included in a [public court document](http://www.rcfp.org/sites/default/files/docs/20120105_202426_apple_sealing.pdf).

Apple has attempted to classify the OSK as a trade secret but has ultimately failed in doing so. As a result, it is freely included within this project, as with [OSX-KVM](https://github.com/kholia/OSX-KVM).

***

## Useful Links

Here are some external links to other resources that you might find useful.

- **[OSX-KVM](https://github.com/kholia/OSX-KVM)** 》 The original basis of this project, providing many resources for running macOS under KVM.
- **[Dortania's OpenCore Guide](https://dortania.github.io/OpenCore-Install-Guide/)** 》 An extensive website of documentation on Hackintosh systems as a whole, useful for troubleshooting issues on both physical and virtual machines.
- **[GPU Buyer's Guide](https://dortania.github.io/GPU-Buyers-Guide/)** 》 An excellent write up on Dortania's website to help you make informed GPU buying decisions for maximum success rates. This is the primary source of data used in the *GPU compatibility checker* script included in ULTMOS.
- **[LegacyOSXKVM](https://github.com/royalgraphx/LegacyOSXKVM)** 》 Documentation and resources on running legacy OS X versions. Legacy support in ULTMOS is based on this project.
- **[OpenCore Configurator](https://mackie100projects.altervista.org/download-opencore-configurator/)** 》 Download page for OCC, an application used to edit OpenCore configs from within macOS.  

> [!WARNING]
> These links and their contents are not authored, monitored, or maintained by Coopydood, and are not affiliated as such. They are provided for convenience purposes only.

***

## Credits & Greetz

While I am the creator of these automation/ease-of-use scripts, this project is not possible without both the prior and current works of some very talented people. The people who have tested the project are also included.

- **[Dortania](https://github.com/Dortania)** 》 Extensive documentation and Hackintosh development.
- **[Kholia](https://github.com/kholia)** 》 Development of scripts and documentation. ultimate-macOS-KVM is intended as an extension to [OSX-KVM](https://github.com/kholia/OSX-KVM).
- **[thenickdude](https://github.com/thenickdude)** 》 Personal support throughout my KVM misadventures and countless community contribs. Cheers.
- **[vit9696](https://github.com/vit9696)** 》 Author of many macOS hacks including kexts, and other source material used in this project. Probably knows the macOS boot process better than Apple.
- **[vu1tur](to@vu1tur.eu.org)** 》 Open source dmg to img conversion tool; used and bundled in this project.
- **[Eversiege](https://github.com/eversiege)** 》 Support and testing, та мій улюблений українець. Also made the project's main [website](https://coopydood.github.io/ultimate-macOS-KVM).
- **[CyberneticSquid](https://github.com/cyberneticsquid)** 》 Testing for me at stupid-o'-clock because he's a cool Aussie.
- **[Cake](https://github.com/cam-jm)** 》 Another Aussie testing for me in the middle of my sleep-deprived nights, with a slight obsession over cake.
- **[DomTrues](https://github.com/domtrues)** 》 My personal constitution-munching American. Legend has it that I live in his attic, although even I'm not sure. Love this guy either way.
- **[Kaz](https://github.com/Eaz11)** 》 Other than his brilliant English accent's pronunciations (including "macOS Syria"), he's done extensive testing. Say hi to your nephew for me.
- **[GigantTech](https://twitter.com/TechGigant)** 》 Moderately annoying German guy that I convinced to install Linux subsequently letting him test my project. It's free real estate!

***

<p align="center">
  <img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/39d78d4b-8ce8-44f4-bba7-fefdbf2f80db" width="10%"> </img>
</p>
