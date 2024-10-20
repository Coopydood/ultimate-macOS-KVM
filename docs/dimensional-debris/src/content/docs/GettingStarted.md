---
title: Getting Started
---


## Cloning and Permissions
It's easy to get up and running. Simply clone the repo, fix permissions, and run.
Make sure you have **all** [dependencies](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/README.md#requirements) installed before getting started.

***

> [!WARNING]
> As of v0.9.0, the main menu file is now `main.py`. This wiki has been updated to reflect this change.
> If you are on an older project version (<= v0.8.6), this file will still be named `setup.py`.
***

```
git clone https://github.com/Coopydood/ultimate-macOS-KVM
cd ultimate-macOS-KVM
chmod +x main.py
```
or, do all this with a one-liner:
```
git clone https://github.com/Coopydood/ultimate-macOS-KVM && cd ultimate-macOS-KVM && chmod +x main.py
```

***

## Starting Up
To begin using the project, run the `main.py` file found in the root of the repo directory. It can be run using the following command:
```
./main.py
```
This is your central hub - a macOS-KVM swiss army knife per se. You should use this script to access any other parts of the project, as the other script files **are not intended to be run directly by the user**.

When using the script, make sure you are cd'd into the `ultimate-macOS-KVM` repo directory first. Example:
```
[name@hostname ~]$ cd ultimate-macOS-KVM
[name@hostname ultimate-macOS-KVM]$ ./main.py
```

***
> [!IMPORTANT]
> Do *not* use `sudo`. If you're in the habit of running everything with superuser permissions - break that habit before it breaks you.
> None of my scripts require `sudo` or root permissions. The only exception to this would be when running a config script *with a physical PCI device passed through using VFIO-PCI*, as this may require superuser permissions as you're dealing with physical devices.

***

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ef278407-a14f-4ae7-bc23-3f635687db65" width="25%"> 

<sub>Written and maintained by **Coopydood**. </sub>
<br><sub>You can [contribute](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs) to documentation, too!</sub>