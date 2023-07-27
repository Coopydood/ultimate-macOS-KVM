## Gotchas
### Things that will grab you by the balls unexpectedly

#### Introduction

You know those computery things that make you facepalm and want to give up because you have no idea why it's happening to you, and all at 3AM running on no sleep? Yeah, I know I do, and I'll be referring to these god-forsaken moments as "gotchas". Because they gotcha. Then sprinkled on some sleep deprivation for good measure. 

This document is for when you learn the definition above to be true, as a comforting guide through the stages of grief. Take a look and prepare yourself, or don't and hope that you don't need to come back here. But you will. Pinkie promise. :P

Please note this document will be updated frequently.

***
<details><summary><h5>main.py: Permission denied</h5></summary>

Awww, you little donkey. You forgot to make it executable.

```
chmod +x ./main.py
```

*sigh*. I did say it was for noobs. Dammit.

</details>

<details><summary><h5>Virtual machine detected, functionality may be limited</h5></summary>

Exactly what it says on the tin. However, it **is** just a warning. 

You can still access all aspects of the project, but they probably won't work unless you have nested virtualisation enabled, and even then, good luck with performance.

If this message appears in error, and it is your host machine, please [submit an issue on GitHub](https://github.com/Coopydood/ultimate-macOS-KVM/issues/new), providing your system specifications in the issue.

</details>


<details><summary><h5>AutoPilot can't create a virtual hard disk file</h5></summary>

You probably don't have ``qemu-tools`` installed.

</details>

<details><summary><h5>macOS recovery: an internet connection is required</h5></summary>

Make sure your network adapter model is set correctly in your config file. You may want to try with the ``vmxnet3`` virtual network device.

Also make sure that the virtual network is started. You can do this with 

```
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

<details><summary><h5>Who the hell is Eversiege?</h5></summary>

You may have seen the name ``Eversiege`` pop up throughout the project. Who is it you ask?

[Ask him.](https://github.com/eversiege)

It's not like I know.

</details>