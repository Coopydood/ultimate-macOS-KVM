---
title: Remote Desktop
---


## Remote Access and Desktop

### Both to and from the guest

#### Introduction

Various remote access and remote desktop methods provide a way to interact with both your host OS and guest OS, *to and from* either side. This document will go over a couple of methods you can use, and which are best for specific scenarios you may find yourself in. Let's go!

***

#### Access? Desktop? Wat?!

First of all, I'll quickly define what I mean by "remote access" and "remote desktop". 

**Remote Access** refers to simply accessing the machine over the network remotely - such as Secure Shell (SSH) or a variety of filesharing methods.

**Remote Desktop** refers to actually *viewing* what's being graphically displayed on the machine - through both physical and virtual display outputs. With this, you can also directly control the machine's mouse and keyboard inputs through your own, if permitted.

***

#### Secure Shell (SSH)

The quickest and most simple way to remote access into a machine is through SSH. 

SSH allows you to use a terminal emulator on a remote device - such as your phone - to directly execute commands on the target machine. It's essentially like opening a terminal window on your host machine, but displayed on another machine.

It's especially useful for those with only a single GPU or display - or when passing through an entire USB controller - as you can start and stop virtual machines using commands remotely, even when your host OS is headless.

|             **What it's good for**            | **What it isn't good for** |
|:---------------------------------------------:|:--------------------------:|
|       Starting and stopping running VMs       |        File transfer       |
| Editing config files through the command line |      GUI applications      |
|        Rebooting your host if necessary       |                            |

***

#### Samba File Sharing (SMB)

Samba is the most simple and diverse way to access and share files between a variety of OSes. 

You can use Samba to set up SMB shares, that can then be accessed from virtually any operating system, regardless of filesystem. For example, you can set up a share on your Linux host, and access it from within the macOS VM. It can even be set up as read-only if you prefer.

This is really useful for sharing a unified fileset between your host and guest, or multiple guests. Being able to quickly grab a file from your downloads or a line of code from a project folder is very handy!

|    **What it's good for**   | **What it isn't good for** |
|:---------------------------:|:--------------------------:|
|        File transfer        |     Network congestion     |
| Accessing files from any OS |          Bandwidth         |
|      Wide compatibility     |         Bufferbloat        |

***

#### ShareMouse

This is a cross-platform program that lets you share your mouse cursor between machines and OSes seamlessly.

Many other tools also exist that have similar functionality.

|   **What it's good for**   | **What it isn't good for** |
|:--------------------------:|:--------------------------:|
|         Continuity         |         Low latency        |
|         Ease of use        |         Performance        |
| Share the same USB devices |          Stability         |

***

#### Virtual Network Computing (VNC)

VNC is a widely-used and reliable remote desktop protocol. It provides cross-platform desktop viewing and control, and has support built in to several OSes, with virtually all OSes having both a VNC client and server application developed for it.

VNC is reliable over local networks, and can be port forwarded to access remotely on sufficient internet connections. 

For example, macOS has a VNC server built into the OS. You can enable it in *System Preferences > Sharing > Remote Desktop*.

| **What it's good for** | **What it isn't good for** |
|:----------------------:|:--------------------------:|
|  Basic remote desktop  |     Intensive workloads    |
|       Reliability      |           Gaming           |
|      Compatibility     |       Resource usage       |

***

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ef278407-a14f-4ae7-bc23-3f635687db65" width="25%"> 

<sub>Written and maintained by **Coopydood**. </sub>
<br><sub>You can [contribute](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs) to documentation, too!</sub>