## OpenCore
### Important information about the included OpenCore image

#### Introduction
This project contains several customised OpenCore bootloader disk images, modified from kholia's OSX-KVM repo. The images have been set up in a way that should work out-of-the-box without any user modification.

However, due to this one-size-fits-all configuration shared among all users of the project, you might *want* to manually edit some things.

The default OpenCore image included with **ultimate-macOS-KVM** presents the following system properties:

- **Model**: Mac mini (2018)
- **Identifier**: Macmini8,1
- **Processor**: Dual-Core Intel Core i7 @ 2.9GHz
- **Serial Number**: C07W10D9JYVX

#### Do NOT sign in to your Apple ID yet!
But don't worry, you can after some light tinkering.

The problem lies with the *serial number*. The default Mac serial number that comes with the OpenCore image included in this project is **C07W10D9JYVX**. While this *is* in the correct format for a Mac Mini 2018, it's likely going to be shared by several users.

This becomes a problem when Apple IDs get involved. When you sign in to a Mac with your Apple ID, it becomes associated with it, via the serial number. When many people sign in to their unique Apple IDs on the same shared serial number- ...well, some folks at Apple likely begin to stroke their neckbeards.

Basically, the serial number gets **busted**. Or, less dramatically - blacklisted. This means that any Apple ID that tries to sign into it will be flagged as compromised, prompting the user to perform a mandatory password change. Trust me, this is not a headache you want.

So, in order to sign in to your own Apple ID safely, you need your *own* serial number. Ya dig? Read on.

#### Getting your own serial number
Now that you understand the *"why"*, it's time to learn the *"how"*.

Unless you're booting macOS for the first time *with an already-modified OpenCore image containing a unique serial number*, you **should NOT sign in with your Apple ID during Setup Assistant under ANY CIRCUMSTANCES.**

Create a "local" user account by skipping the Apple ID stage of the Setup Assistant. After you complete the Setup Assistant with a regular local account, you can continue.

Now, check your serial number. Go to **Apple Menu > About this Mac** and look at the **Serial Number** entry. If your serial number is **C07W10D9JYVX**, you still have the shared default, and should change it.

To do this, the easiest method is to use **OpenCore Configurator** from within the macOS VM. This can be obtained here: https://mackie100projects.altervista.org/download-opencore-configurator/

Open it, and in the menu bar, go to **Tools > Mount EFI**. A new window will pop up. There will be a couple of entries called "EFI". The one we want is the entry **without** "Preboot,Recovery,VM" etc.

Click **Mount**, authenticate, and close the popup window. Then, on the menu bar, go to **File > Open**. From here, use the Finder popup window to navigate to **EFI > OC** and select **config.plist**. The main window should reopen with entries already populated. 

Now, down the side of the main window, click **PlatformInfo**, then along the tab bar at the top to **SMBIOS**. At the bottom of the page, there is a combo box (select list) to the right of "Check Coverage". Click it, and browse the list of Mac models until you find one that you want (or just choose the 2018 Mac mini again). 

The many fields on the page should now be populated with values, including the *serial number* at the top. Under the box, there should be a **Generate** button. Click that and make sure the new serial number is unique. When you've done this, go ahead and go to **File > Save**, and reboot the VM.

Upon reboot, check the serial number again from the **About this Mac** window. If it has been changed - **congratulations**! You now have a unique serial number. This means you can safely log into your Apple ID, with the assurance no one else will use that serial number. 