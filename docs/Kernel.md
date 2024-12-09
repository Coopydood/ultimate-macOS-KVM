## Preparing your host for passthrough
### Set up your kernel and devices

#### Introduction

In order to use several passthrough-related features of ULTMOS, such as the [VFIO-PCI Passthrough Assistant](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/VFIO%E2%80%90PCI-Passthrough-Assistant), you must first prepare your host OS and devices.

Depending on your setup, this is where our paths diverge...

***

## 1. Single GPU passthrough

If ALL of the following statements are true, this is the section you should use;
- You **do NOT** have an integrated GPU (CPU Graphics / iGPU), it is disabled, or unsupported by your host
- If an iGPU is present, you are unable to use it or it cannot be enabled
- You only have **one** dedicated graphics card in your system
- Your dedicated graphics card [is supported](https://dortania.github.io/GPU-Buyers-Guide/)
- You are prepared for trial and error
  
**Example:** You have a CPU model that does not include integrated graphics, but have a dedicated AMD graphics card, and use it as your primary graphics device. 

If you have determined that this matches your setup, you should follow **[this guide by DarknessRafix](https://gitlab.com/DarknessRafix/macosvmgpupass)**. It will guide you through setting up single GPU passthrough using ULTMOS.

> [!IMPORTANT]
> Please note that single GPU passthrough **is not currently supported natively by ULTMOS.** However, this is a planned feature for development in the near future.
>
> Despite being unsupported by ULTMOS, we are still more than happy to try and assist you with any issues you may encounter on the [Discord server](https://discord.gg/WzWkSsT). There are many people with ULTMOS single-GPU success stories in here!

***

## 2. Dedicated passthrough (recommended)

If ALL of the following statements are true **in one of the two scenarios below**, you should use this section instead;
- You have integrated graphics (iGPU) enabled and working, and can be used for output (such as Intel's "UHD Graphics")
- You additionally have a dedicated graphics card that [is supported](https://dortania.github.io/GPU-Buyers-Guide/)
- Your host system supports **IOMMU** (IO memory management unit) - this can be enabled on most modern BIOSes
  
**Example:** You have a system with an Intel CPU that has "UHD 630" integrated graphics, with accessible video outputs on your motherboard, AND you have a dedicated AMD graphics card.
  
### OR

- You **do NOT** have an integrated GPU (CPU Graphics / iGPU), it is disabled, or unsupported by your host
- You have **at least two** dedicated GPUs, and at least **one** of them [is supported](https://dortania.github.io/GPU-Buyers-Guide/)
- Your host system supports **IOMMU** (IO memory management unit) - this can be enabled on most modern BIOSes

**Example:** You have a system with a CPU model that does not include integrated graphics, but you have both an NVIDIA and an AMD GPU installed simultaneously. You want your NVIDIA card to be used by your host and your AMD card to be used by macOS. 

<br><br>

If you have determined that either scenario this matches your setup, you should continue reading **this document.**

This method is the officially supported method of passthrough in ULTMOS, and therefore the most reliable. It typically has a much higher success rate than single-GPU passthrough.

> [!WARNING]
> This method of passthrough **reserves** the entire device for exclusive use by the virtual machine. 
>
> **Your host will NOT be able to use the device!!!**


## 2.1 Kernel modules

Your Linux kernel must be set up to load a few extra *kernel modules* on boot. This can usually be done fairly easily by editing the configuration file responsible for generating your kernel image.

The modules we need to load are:
- ``vfio-pci``
- ``vfio``
- ``vfio-iommu-type1``
- ``kvmgt``

> [!IMPORTANT]
> The instructions for doing this vary across different Linux distros. The following instructions are an example for Arch Linux.

For example, on **Arch Linux** using **mkinitcpio**, the file we need to edit is located at ``/etc/mkinitcpio.conf``.

Open this file with an editor of your choice (such as ``vim`` or ``nano``), and, at the top of the file, locate the ``MODULES=(...)`` entry. The brackets may or may not have entries populated. An unmodified entry may look like this:

```
# MODULES
# The following modules are loaded before any boot hooks are
# run.  Advanced users may wish to specify all system modules
# in this array.  For instance:
#     MODULES=(piix ide_disk reiserfs)

MODULES=()
```

In the brackets, add the required modules, seperated by spaces. It should look like this:

```
# MODULES
# The following modules are loaded before any boot hooks are
# run.  Advanced users may wish to specify all system modules
# in this array.  For instance:
#     MODULES=(piix ide_disk reiserfs)

MODULES=(vfio-pci vfio vfio-iommu-type1 kvmgt)
```

Save this file, and then rebuild your kernel image:

```
sudo mkinitcpio -P
```
You do not have to reboot yet.

## 2.2 Kernel parameters

We now need to edit your kernel parameters. For most people, this can be done through your GRUB entries.

The default GRUB configuration file is located at ``/etc/default/grub``. However, we recommend using Grub Customizer instead as it provides a user-friendly GUI that allows for easy editing of multiple GRUB boot entries. See the tip below.

> [!TIP]
> You should duplicate your current Linux GRUB boot entry and label it as passthrough. This means you can choose whether or not to enable passthrough at boot. You can do this using Grub Customizer.
>
> Example of a GRUB boot menu entry list:
>
> - Arch Linux
> - Arch Linux (Passthrough)
> - Windows

On the boot entry you want to use for passthrough, find the ``linux`` line. An example of a default entry:

```
savedefault
	load_video
	set gfxpayload=2560x1440
	insmod gzio
	insmod part_gpt
	insmod fat
	search --no-floppy --fs-uuid --set=root B421-25A5
	linux	/vmlinuz-linux-zen root=UUID=57192c57-5e88-4e0f-be32-d4c7e5da3749 rw rootfstype=ext4
	initrd	/intel-ucode.img /initramfs-linux-zen.img
```

The relevant line here is

```
linux	/vmlinuz-linux-zen root=UUID=... rw rootfstype=ext4
```

At the end of this line, append the following entries:

**Intel CPU users**: ``intel_iommu=on iommu=pt``

**AMD CPU users**: ``amd_iommu=on iommu=pt``

It should then look like this:

```
linux	/vmlinuz-linux-zen root=UUID=... rw rootfstype=ext4 intel_iommu=on iommu=pt
```

If using Grub Customizer, save the changes. If you are editing GRUB manually, run ``sudo grub-mkconfig -o /boot/grub/grub.cfg``.

You should then reboot.

## 2.3 IOMMU groups