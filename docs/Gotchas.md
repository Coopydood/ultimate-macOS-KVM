## Gotchas
### Things that will grab you by the balls unexpectedly

#### Introduction

You know those computery things that make you facepalm and want to give up because you have no idea why it's happening to you, and all at 3AM running on no sleep? Yeah, I know I do, and I'll be referring to these god-forsaken moments as "gotchas". Because they gotcha. Then sprinkled on some sleep deprivation for good measure. 

This document is for when you learn the definition above to be true, as a comforting guide through the stages of grief. Take a look and prepare yourself, or don't and hope that you don't need to come back here. But you will. Pinkie promise. :P

Please note this document will be updated frequently.

***
<details><summary><h5>main.py: Permission denied</h5></summary>

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

Doing so with an unsupported OS may have unexpected consequences, and ones I am not prepared to take responsibility for. The check is implemented for a reason - although mostly to save you the disappointment.

</details>

<details><summary><h5>AutoPilot can't create a virtual hard disk file</h5></summary>

You probably don't have ``qemu-tools`` installed.

</details>

<details><summary><h5>AutoPilot exits silently during user questions</h5></summary>

This is likely due to an "extreme value" being entered. 

For example, if the question had menu answer options of ``1``, ``2``, ``3``, ``?``, and ``Q`` - but you entered ``4``, this would cause the input to get confused and simply *yeet*.

Because my Python skillz are nothing short of terrible, extreme handling wasn't implemented until [v0.9.5](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-5.md), and even then it may not work fully.

</details>

<details><summary><h5>macOS recovery: an internet connection is required</h5></summary>

Make sure your network adapter model is set correctly in your config file. You may want to try with the ``vmxnet3`` virtual network device.

Also make sure that the virtual network is started. You can do this with 

```sh
$ sudo virsh net-start default
```

</details>

<details><summary><h5>qemu-system-x86_64: warning: Number of SMP cpus requested (X) exceeds the recommended cpus supported by KVM (X)</h5></summary>

This is caused by incorrect virtual CPU topology. You may have set an invalid number of virtual CPU cores and/or threads.

Please read [this document](https://github.com/Coopydood/ultimate-macOS-KVM/wiki/AutoPilot) on the wiki to learn what values you should use.

</details>

<details><summary><h5>Repository file integrity damaged</h5></summary>

When using AutoPilot, the restore tools suite, system checkers, or the built-in updater tool, you may encounter an error regarding repo file integrity.

This indicates that critical files needed for the project to operate were not found when searched for by the running script.

Please check that you have not moved or deleted core files, such as those in the ``resources`` folder. 

To repair the repo integrity, you may have to use the online-based restore tool, that can be accessed by typing ``X`` at the restore tools menu.

</details>

<details><summary><h5>XML converstion tool crashes when converting AutoPilot script, or has incorrect values</h5></summary>

Even if the AutoPilot script **is** valid, it may still be incompatible. 

This is because the underlying structure of AP config files was changed in [v0.9.2](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-2.md), and the XML conversion tool looks for this structure.

Therefore, any AutoPilot config files created using **v0.9.1 or earlier** should **NOT** be used with the XML conversion tool. 

Support for updating legacy AP files may come in the future, but for now it is recommended that you simply create a new AP config. **You can keep your data** - just have your existing ``HDD.qcow2`` file in the root ``ultimate-macOS-KVM`` folder, and when AutoPilot reaches the hard disk creation stage, you'll be given the option to use the existing HDD file. You can also skip the macOS image stage if macOS is already installed.

</details>

<details><summary><h5>macOS Ventura (13.X) fails to install or upgrade, with various errors</h5></summary>

This is a [known issue](https://github.com/Coopydood/ultimate-macOS-KVM/issues/10). 

While this is investigated, please do not try to install or upgrade to macOS Ventura, as this may be unrecoverable until resolved. Stick to **macOS Monterey (12)** or earlier for now. 

The most stable tested OS is **macOS Big Sur (11)**.

If you'd like to help the investigation, any and all testing is greatly appreciated, and can be submitted as a comment to the issue linked above.

</details>

<details><summary><h5>Who the hell is Eversiege?</h5></summary>

You may have seen the name ``Eversiege`` pop up throughout the project. Who is it you ask?

[Ask him.](https://github.com/eversiege)

It's not like I know.

</details>