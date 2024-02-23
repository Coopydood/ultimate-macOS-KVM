## Issues and Troubleshooting
### Common issues and how to fix them

#### Introduction

You know those computery things that make you facepalm and want to give up because you have no idea why it's happening to you, and all at 3AM running on no sleep? Yeah, I know I do, and I'll be referring to these god-forsaken moments as "gotchas". Because they gotcha. Then sprinkled on some sleep deprivation for good measure. 

This document contains numerous issues that you may encounter when using both this project and macOS itself - ranging from AutoPilot to GPU passthrough issues. This document is a better, more organised version of the old ``Gotchas.md`` file.

> [!NOTE]
> This document will be updated frequently.

***

#### Main Menu

These are issues you may encounter when first running the project via the ``main.py`` script.

<details><summary><h5>main.py: Permission denied</h5></summary>

**NOTE:** As of v0.9.8, files are packaged as executable by default, and do not require additional permission modifications.

Awww, you little donkey. You forgot to make it executable.

```sh
$ chmod +x ./main.py
```

*sigh*. I did say it was for noobs. Dammit.

</details>

<details><summary><h5>Virtual machine detected, functionality may be limited</h5></summary>

Exactly what it says on the tin. However, it **is** just a warning. 

You can still access all aspects of the project, but they probably won't work unless you have nested virtualisation enabled, and even then, good luck with performance.

If this message appears in error, and it is your host machine, please [submit an issue on GitHub](https://github.com/Coopydood/ultimate-macOS-KVM/issues/new), providing your system specifications in the issue.

</details>

<details><summary><h5>Incompatible OS detected</h5></summary>

Yeaaaaah, no. Your little misadventure was just busted before it began.

As of [v0.9.5](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-5.md), an OS platform check is performed when running this project, and may prevent you from running `main.py`. This simply means that *you aren't using Linux*. And, you *need* Linux, as pointed out [here](https://github.com/Coopydood/ultimate-macOS-KVM#oh-and-you-need-linux). 

This is because KVM - the premise of this whole project - is a part of the Linux kernel.

If this message appears in error, and you *are* running a distrobution of Linux, please [submit an issue on GitHub](https://github.com/Coopydood/ultimate-macOS-KVM/issues/new), providing your system specifications in the issue.

If you're **sure** this is an error, you can bypass this check with the `--skip-os-check` argument, like so:

```sh
$ ./main.py --skip-os-check
```

> [!WARNING]
> Doing so with an unsupported OS may have unexpected consequences, and ones I am not prepared to take responsibility for. The check is implemented for a reason - although mostly to save you the disappointment.

</details>

***

#### AutoPilot

These are various issues you may encounter throughout the built-in AutoPilot tool.

<details><summary><h5>AutoPilot can't create a virtual hard disk file</h5></summary>

You probably don't have ``qemu-tools`` installed.

However, if the issue persists, you can try making the HDD file yourself:
```sh
$ qemu-img create -f qcow2 HDD.qcow2 <size>G 
```

then try running AutoPilot again. It will detect the disk file and ask if you want to use it.

</details>

<details><summary><h5>AutoPilot exits silently during user questions</h5></summary>

This is likely due to an "extreme value" being entered. 

For example, if the question had menu answer options of ``1``, ``2``, ``3``, ``?``, and ``Q`` - but you entered ``4``, this would cause the input to get confused and simply *yeet*.

Because my Python skillz are nothing short of terrible, extreme handling wasn't implemented until [v0.9.5](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-5.md), and even then it may not work fully.

</details>

***

#### Installing macOS

These are issues related to the macOS installation process.

<details><summary><h5>macOS recovery: an internet connection is required</h5></summary>

Make sure your network adapter model is set correctly in your config file. You may want to try with the ``vmxnet3`` virtual network device.

Also make sure that the virtual network is started. You can do this with 

```sh
$ sudo virsh net-start default
```

</details>

<details><summary><h5>macOS Ventura (13.X) fails to install or upgrade, with various errors</h5></summary>

This was a [known issue](https://github.com/Coopydood/ultimate-macOS-KVM/issues/10), and has been resolved:

This issue does NOT affect users who changed their CPU model from the default. For example, if you manually changed your CPU model to ``host``, this does not affect you.

**FOR NEW USERS:** as of [v0.9.6](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-6.md), this issue has been fixed, and new files generated with AutoPilot will use the new model by default, which can be used to install Ventura.

**FOR EXISTING USERS:** for users of **v0.9.5** or earlier, you have a couple options:
***
1. If you have an existing AutoPilot config that you have used for a while, with many customisations of your own, it may be best to just change the CPU model. Do this by finding the following line in your boot script:
```sh
CPU_MODEL="Penryn"
```
and change it to
```sh
CPU_MODEL="Haswell-noTSX"
```

***

2. Generate a new AutoPilot config file. While this does mean you have to go through AutoPilot again, there are a number of benefits. Generating a new AP config ensures you have the latest structure updates, and the best compatibility with the rest of the project:

    - You can **keep your existing config file**, either by choosing a different name, or by backing up your old one when prompted
    - You can **keep and use your existing virtual hard disk file**. When AP gets to the `Creating virtual hard disk` stage, you'll automatically be notified about the existing HDD file, and you'll have the option to use the file in the new config.
    - Your **OpenCore boot image will be replaced**, but your old OpenCore image will **automatically get backed up to a timestamped folder, in the `boot` folder**. If you've made customisations to the OpenCore image, you can move the old one back into place after AP finishes.
    - The **virtual NVRAM will be reset**, but this is safe. In [v0.9.2](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-2.md) and later, you can even select your screen resolution as an AutoPilot stage - meaning you won't lose any resolution changes you may have made.

***
~~While this is investigated, please do not try to install or upgrade to macOS Ventura, as this may be unrecoverable until resolved. Stick to **macOS Monterey (12)** or earlier for now.~~ 

~~The most stable tested OS is **macOS Big Sur (11)**.~~

~~If you'd like to help the investigation, any and all testing is greatly appreciated, and can be submitted as a comment to the issue linked above.~~

</details>

<details><summary><h5>No disks available during macOS installation</h5></summary>

If you're in macOS Recovery and trying to use the installer, you'll get to a screen asking you to select a disk.

If this screen only shows "macOS Base System" (greyed out), then it simply means you have not formatted the virtual disk yet. 

This can be done by using **Disk Utility** from the macOS Recovery menu. 

Select the ``QEMU HARDDISK`` entry from the sidebar with the storage capacity corresponding to what you chose during AutoPilot - be careful not to erase the small OpenCore partition. 

When selected, click "Erase" from the centre-top header, and enter a name for the new disk; this can be whatever you want. The default is ``Untitled``, so you can be classy and call it ``Titled``, or if you want to emulate a real Mac, call it ``Macintosh HD``. It's up to you. 

For the filesystem, leave ``APFS`` as the selected option, unless you particularly want to use Mac OS Extended.

Then, simply quit Disk Utility and return to the macOS installer. On the disk selection screen, your newly-formatted disk should appear as a selectable option. Click it, and then click ``Install``. Done!

</details>

***

#### macOS Post-Install

These are issues related to the macOS after it has been fully installed.

<details><summary><h5>Very long boot time on macOS Ventura and later  (<code>"PCIEnumerationWaitTime is 900"</code> etc.)</h5></summary>

There may be a bug present in the macOS verbose system that temporarily hangs the boot process for a very long time - sometimes upwards of 10 minutes in some cases.

This can almost be classed as a red-herring - as most users would assume their system has crashed at this point - when in actual fact letting it sit will eventually get it to boot.

**However, you can fix this boot time by removing the ``-v`` boot argument.** After disabling verbose boot (``-v``), boot times in my case went from >5 minutes to under 30 seconds. Wow!


</details>

<details><summary><h5>Black screen or reset after install when using AMD RX 5xxx / 6xxx (Navi) GPUs</h5></summary>

This is likely due to a missing boot argument required for display out on RX 5000 and RX 6000 series cards.

You need to add the following boot argument to the OpenCore image:
```
agdpmod=pikera
```


As of [**v0.11.0**](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-11-0.md) and later, the OpenCore image can be patched automatically using the **AutoPatch** functionality included in the **macOS Boot Argument Editor** tool - located in ``Extras > macOS Boot Argument Editor``.

Alternatively, such as on older versions, this can be done from within macOS using **OpenCore Configurator**. If you used the **VFIO-PCI Passthrough Assistant** to configure passthrough, you can use the generated ``<name>-noPT.sh`` file to temporarily boot macOS without passthrough enabled - allowing you to make the necessary changes.

</details>

<details><summary><h5>Kernel: <code>Couldn't alloc class "AppleKeyStoreTest"</code></h5></summary>

Being stuck here after passing through a GPU on macOS Ventura and later may actually be deceptive. 

Either the system has in fact panicked, or **it may still be booting in the background**. No, really!

If you're "stuck" at ``Couldn't alloc class "AppleKeyStoreTest"``, wait up to 5 minutes. There may be a bug present in the macOS verbose system that prevents any more output after a certain stage.

**You can fix this boot time by removing the ``-v`` boot argument.**

Found by @DomTrues.

</details>

***

#### QEMU and virt-manager

These are issues you may run into when using both QEMU scripts and virt-manager (virsh) domains.

<details><summary><h5>qemu-system-x86_64: warning: Number of SMP cpus requested (X) exceeds the recommended cpus supported by KVM (X)</h5></summary>

This is caused by incorrect virtual CPU topology. You may have set an invalid number of virtual CPU cores and/or threads.

Please read [this document](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot) on the wiki to learn what values you should use.

</details>

<details><summary><h5>vfio 0000:00:00.0: failed to open /dev/vfio/X: Permission denied</h5></summary>

This is what happens when trying to run a script file that contains PCI passthrough as a regular user.

Thankfully, this is of course an easy fix. You'll need to run the script as superuser;

```sh
$ sudo ./boot.sh
```
</details>

<details><summary><h5>Unknown PCI header type "127" (vendor reset bug)</h5></summary>

Sometimes, when stopping or resetting a virtual machine with an AMD GPU passed through, the "reset" mechanism used to detach the GPU from the virtual machine fails.

This is due to a problem known as the **vendor reset bug**. It affects a large variety of AMD GPUs, and is a firmware-level flaw.

Unfortunately, after seeing this message, the only way to use the GPU again with a VM (even the same one) is to restart the host entirely. Even this might be difficult, as the shutdown process may hang when trying to reset the GPU before power off. Make sure you save all your work, and allow as many system processes to exit as possible, and then hard-reset the host.

Although annoying, it's pretty benign. You can install ``vendor-reset`` using the ``vendor-reset-dkms-git`` package, which will likely not eliminate the issue entirely, but prevents it happening as often. 

It's also worth noting that some cards are affected worse than others, so occurance of the issue may vary.


</details>

***

#### VFIO-PCI and Passthrough

These are issues related to PCI device passthrough using VFIO-PCI. This includes GPU issues.

<details><summary><h5>Black screen or reset on AMD RX 5xxx / 6xxx (Navi) GPUs
</h5></summary>

This is likely due to a missing boot argument required for display out on RX 5000 and RX 6000 series cards.

You need to add the following boot argument to the OpenCore image:
```
agdpmod=pikera
```


As of [**v0.11.0**](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-11-0.md) and later, the OpenCore image can be patched automatically using the **AutoPatch** functionality included in the **macOS Boot Argument Editor** tool - located in ``Extras > macOS Boot Argument Editor``.

Alternatively, such as on older versions, this can be done from within macOS using **OpenCore Configurator**. If you used the **VFIO-PCI Passthrough Assistant** to configure passthrough, you can use the generated ``<name>-noPT.sh`` file to temporarily boot macOS without passthrough enabled - allowing you to make the necessary changes.

</details>


***

#### Miscellaneous

Other issues related to the project or macOS that don't fit into any of the other categories.

<details><summary><h5>Repository file integrity damaged</h5></summary>

When using AutoPilot, the restore tools suite, system checkers, or the built-in updater tool, you may encounter an error regarding repo file integrity.

This indicates that critical files needed for the project to operate were not found when searched for by the running script.

Please check that you have not moved or deleted core files, such as those in the ``resources`` folder. 

To repair the repo integrity, you may have to use the online-based restore tool, that can be accessed by typing ``X`` at the restore tools menu.

</details>

<details><summary><h5>XML converstion tool crashes when converting AutoPilot script, or has incorrect values</h5></summary>

Even if the AutoPilot script **is** valid, it may still be incompatible. 

This is because the underlying structure of AP config files was changed in [v0.9.2](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-2.md), and the XML conversion tool looks for this structure.

> [!WARNING]
> Therefore, any AutoPilot config files created using **v0.9.1 or earlier** should **NOT** be used with the XML conversion tool. 

Support for updating legacy AP files may come in the future, but for now it is recommended that you simply create a new AP config. **You can keep your data** - just have your existing ``HDD.qcow2`` file in the root ``ultimate-macOS-KVM`` folder, and when AutoPilot reaches the hard disk creation stage, you'll be given the option to use the existing HDD file. You can also skip the macOS image stage if macOS is already installed.

</details>



<details><summary><h5>Who the hell is Eversiege?</h5></summary>

You may have seen the name ``Eversiege`` pop up throughout the project. Who is it you ask?

[Ask him.](https://github.com/eversiege)

It's not like I know.

</details>

***

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ef278407-a14f-4ae7-bc23-3f635687db65" width="25%"> 

<sub>Written and maintained by **Coopydood**. </sub>
<br><sub>You can [contribute](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs) to documentation, too!</sub>