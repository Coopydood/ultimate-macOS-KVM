## Introduction
So, what is AutoPilot? Are we talking about an Airbus A320? Nope, just some random GitHub project on the internet. Regardless, here's the rundown. 

AutoPilot is a script developed by me - Coopydood - to automate the creation of an executable QEMU script file. However, it doesn't just automate it, it also **personalises it based on your preferences.**

The way it works is by asking you - the user - a series of questions about your preferences for the virtual machine. This includes things like the virtual CPU cores, allocated RAM, target OS, etc. Then, AutoPilot uses this information to generate a fully-customised script file, derived from a pre-made base script - with all your preferences. 

The generated script file is **immediately valid** and can be run instantly after AutoPilot completes - which in most cases is under 3 minutes - depending on what you choose to customise. This makes it super easy to get a basic macOS VM up and running with zero user tinkering, all while catering to personal preferences.

With the intro out of the way, I'll now go into more detail about each AutoPilot stage, including acceptable values and how to enter them.
***
NOTE: Any "Accepted" values with a **bold** suffix indicate that you must include it when inputting your custom value into AutoPilot, such as file extensions.

***
## 1. Name your config file
This really is as simple as it sounds. You can choose what you want the file name of the config script to be. This can be an **alphanumeric string** with no special characters except `_` and `-`.

| **Default** |     Accepted    |                  _Examples_                  |
|:-----------:|:---------------:|:--------------------------------------------:|
|   boot.sh   | [string]**.sh** | macOS.sh<br>macOS-1015.sh<br>ultimate_kvm.sh |

***
## 2. Set target OS
This setting only really has one definitive use right now - virtual network adapter model auto selection. Other than that, it is purely cosmetic at this time. It's still recommended to set this value properly in case future functionality and features depend on it.

If defining a custom value, only a **4-digit value for macOS 10.XX releases**, or a **2-digit value for macOS 11 or later** is accepted. 
Do NOT include any subversions (i.e. 10.13.6, 10.15.7, etc.).

In project versions v0.8.6 and later, this value is also now used to add a boot entry to the main menu for easy access. Again, this is purely cosmetic but something to consider.

| **Default** |      Accepted     |  _Examples_  |
|:-----------:|:-----------------:|:------------:|
|     1015    | 10XX<br>_(10.XX)_ | 1013<br>1014 |
|             |   XX<br>_(>=11)_  |   11<br>12   |

***
## 3. Set number of CPU cores
Like any other virtual machine, the guest needs virtual cores to work with. As a general rule, use no more than **80%** of your _host's_ total cores. For example, if your host has _10 cores_, you shouldn't use any more than __8 virtual cores__. That's all I can recommend here - use your own judgment and scale to your hardware appropriately.

| **Default** | Accepted |  _Examples_ |
|:-----------:|:--------:|:-----------:|
|      2      | [number] | 4<br>6<br>8 |

***
## 4. Set number of CPU threads
Similar to the previous step, your guest needs **virtual threads** to work with.

**THIS VALUE IS A MULTIPLIER.** This is calculated as **_virtual cores_ ✕ _virtual threads_**. 

For example, if you wanted a total of 4 virtual cores and 8 virtual threads, you would input 2 here. (4 ✕ [_**2**_] = 8)

If this confuses you - and I don't blame you, I've confused myself - then leave this value as it is.

| **Default** | Accepted | _Examples_ |
|:-----------:|:--------:|:----------:|
|      2      | [number] |   1<br>2   |

***
## 5. Set CPU model
This sets the model of the virtual CPU, and subsequently what the guest OS recognizes it as.

> [!WARNING]
> **THIS SHOULD NOT BE CHANGED UNLESS YOU KNOW WHAT IT MEANS!** Refer to the [official QEMU documentation on CPU models](https://qemu-project.gitlab.io/qemu/system/qemu-cpu-models.html) for a comprehensive list of acceptable values.

If you _**know**_ your **host** CPU model is supported natively by macOS (i.e. Intel Core i3, i5, i7, i9) or at least a **similar variant of a supported model** (such as the i9-10900K being similar to Apple's i9-10910), you can expose the real model to the guest using the `host` value. It might do something. Use at your own risk.

| **Default** |   Accepted  |      _Examples_      |
|:-----------:|:-----------:|:--------------------:|
|    Penryn   | [cpu_model] | Broadwell<br>IvyLake |
|             |     host    |                      |

***
## 6. Set CPU feature arguments
This lets you change the feature set of the virtual CPU. If you're a nerdy nerd nerd who nerds then you might find benefit in tinkering with this, but otherwise:

> [!WARNING]
> **Don't change this unless you know what you're doing.**

|                       **Default**                       |       Accepted      |    _Examples_    |
|:-------------------------------------------------------:|:-------------------:|:----------------:|
| +ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check |        +[arg]       |       +kvm       |
|                                                         | +[arg1],+[arg2] ... | +avx,+kvm,+ssse3 |

***
## 7. Set amount of allocated RAM
This one is very similar to the virtual CPU cores option in that it should be scaled relative to your host's hardware. macOS is surprisingly lenient when it comes to lesser RAM amounts, so you don't need to overdo it. 

> [!NOTE]
> My only recommendation would be: [_total host RAM_] − [_host idle RAM usage_] − 1GB >= **total virtual RAM**

Example: If your host has 16GB total RAM, your host uses 4GB of RAM when idle, don't use any more than 11GB of RAM for the virtual machine. ([_16GB_] − [_4GB_] − 1GB = 11GB)

| **Default** |    Accepted   |    _Examples_   |
|:-----------:|:-------------:|:---------------:|
|      4G     | [number]**G** | 2G<br>8G<br>16G |

***
## 8. Set hard disk capacity
You should think carefully about this one as it might be hard to change later. This is the capacity of your primary virtual hard drive that will be used for your macOS installation. Keep in mind **macOS uses upwards of 40GB for the system**, so you should base your total on how much you think you'll need. 

If you're just testing the project, you can leave it as is. If you plan on using the virtual machine long-term, perhaps make it a bit bigger to give yourself room.

> [!NOTE]
> **This is a dynamically-growing disk. The virtual hard disk file will grow as you use it. The full capacity is NOT used on the host's storage upon creation. If you've ever used VMware's virtual disks, it's the same as that.** Please also note that the _actual_ virtual capacity of the hard disk may be slightly larger than the value you specify.

| **Default** |    Accepted   |      _Examples_     |
|:-----------:|:-------------:|:-------------------:|
|     80G     | [number]**G** | 60G<br>120G<br>256G |

***
## 9. Set network adapter model
This one is a bit more picky. macOS has a limited number of network drivers due to the limited hardware configurations that natively run macOS, therefore you need to pick a model with driver support. 

**Based on your target OS you chose earlier, the default option will auto-select the best model for your macOS version.** 

You can still override this if you'd like, but for most people, whatever is auto-selected will be fine.

|  **Default**  |     Accepted    |     _Examples_    |
|:-------------:|:---------------:|:-----------------:|
| e1000-82545em | [adapter_model] | e1000m<br>vmxnet3 |
|    vmxnet3    |                 |                   |

***
## 10. Network MAC address
The virtual network adapter needs a virtual MAC address to identify it. 

**The default is fine unless you intend on using features such as iMessage and FaceTime, as these services require specific MAC address values.**

In this case, you should use your own custom one, or you can even have the script generate a random compatible one for you. I'd recommend the latter to make it more unique, at the risk of being perhaps a bit less reliable.

|    **Default**    |                Accepted               |                          _Examples_                         |
|:-----------------:|:-------------------------------------:|:-----------------------------------------------------------:|
| 00:16:cb:00:21:09 | XX:XX:XX:XX:XX:XX | 00:16:cb:00:48:02<br>00:16:ca:00:27:09<br>00:16:cr:00:87:33 |

***
## 11. macOS Recovery image file
To install macOS, you'll need an image of the macOS Recovery. 

The script can automatically download a recovery image of a macOS version of your choosing, or you can use one you already have. If you are using a custom image, it should be in the ***.img** format. You can drag a file onto the terminal window, or place a file called `BaseSystem.img` in the root of the project directory to have it be detected automatically. If it is in the ***.dmg** format - this is okay - the script will automatically detect this and convert it for you during the configuration process.

You can also choose to skip this step, but this is not recommended.

|   **Default**  |     Accepted    |              _Examples_             |
|:--------------:|:---------------:|:-----------------------------------:|
| BaseSystem.img | [file_name].img | BaseSystem.img<br>macOSRecovery.img |
|                | [file_name].dmg |   BaseSystem.dmg<br>InstallESD.dmg  |

***
## 12. Screen resolution
As of [v0.9.2](https://github.com/Coopydood/ultimate-macOS-KVM/releases/tag/v0.9.2), you can now pre-select what screen resolution you'd like to use for the virtual screen.

This is done by utilising a pre-made OVMF variable file, with the desired screen resolution built in. Based on what you choose, the corresponding OVMF variable file will be used by AutoPilot to complete setup. 

The default resolution is **1280x720** and is recommended for most users - at least until macOS is installed. However, for a more "native" look, you can choose your monitor's screen resolution if it's supported. This means that in full screen mode, the VM will be running native to your whole screen.

Custom values are not supported. When inputting a value at this stage, you will be given a list of supported resolutions to select from. You must then type the number next to the corresponding resolution to select it, *do not type the resolution itself*.

> [!NOTE]
> **This becomes irrelevant if you use GPU passthrough. Virtual screens are replaced by your physical monitors and their EDID data, which defines available resolutions. This stage is only useful for those not interested in using passthrough.**

| **Default** |                                             Accepted                                            |       _Examples_      |
|:-----------:|:-----------------------------------------------------------------------------------------------:|:---------------------:|
|   1280x720  | 800x600<br>1024x768<br>1280x720<br>1280x1024<br>1440x900<br>1920x1080<br>2560x1440<br>3840x2160 | 1024x768<br>1920x1080 |

***
## 13. Generate XML file
As of [v0.9.3](https://github.com/Coopydood/ultimate-macOS-KVM/releases/tag/v0.9.3), XML files can be generated through conversion of a valid AutoPilot config file using the **XML Conversion tool**. This can be accessed through the **Extras** menu. 

However, with the [v0.9.5](https://github.com/Coopydood/ultimate-macOS-KVM/releases/tag/v0.9.5) update, this functionality is also built right in as an AutoPilot stage.

If you choose, you can have AutoPilot automatically create an XML file alongside your regular boot config script as part of the AutoPilot flow. You'll then be prompted to import it upon completion, for use within Virtual Machine Manager (virt-manager), for easy GUI access.

This stage is completely optional and can be skipped. You can always use the standalone XML conversion tool to convert an AutoPilot script at any time, from the Extras menu.

***
## Review your preferences
You'll now get a chance to see your choices displayed in the form of a summary screen. An example of this screen can be found below:

![AutoPilot summary screen](https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/996fb2b5-28ef-4949-bbc3-4107193b1187)

From here, you can confirm and continue, go back and change your settings, start over, or exit entirely.

***
## Process checklist
The process checklist is displayed upon confirming your preferences, in the form of a traffic light system.

|     **Red**     |  **Yellow** | **Green** |
|:---------------:|:-----------:|:---------:|
| Not yet started | In progress |  Complete |

![AutoPilot progress screen, showing traffic light system](https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/b6390adc-62ff-4a91-bf00-a9b911a5cb29)

If a sub-operation is required, this will be indicated by a dropdown arrow underneath the current parent operation.

***
## Summary
After everything has been completed without issue, you will be presented with a small summary view of what your boot config script is called, the command you can use to run it, and the time it took to complete AutoPilot (speedrunning anyone?).

![AutoPilot post-success screen.](https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/a95f7741-b029-4596-be99-c9fa8b51bb9f)

You'll also receive the option to boot the file straight away, open it in your default text handler (v0.9.2 or later), or exit the program.

