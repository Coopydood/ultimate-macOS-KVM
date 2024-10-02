## XML Conversion Tool
### Convert and import AutoPilot boot scripts

#### Introduction
The **XML Conversion Tool** is an included utility script within the project.

It can be found and run from the **Extras** menu.

This tool allows you to convert existing **AutoPilot-generated boot script files** into **XML domain files**, that can then be imported into the **Virtual Machine Manager (virt-manager)** GUI, for more user-friendly access.

***

> [!WARNING]
> As of **[v0.9.2](https://github.com/Coopydood/ultimate-macOS-KVM/blob/main/docs/changelogs/v0-9-2.md)**, the base structure of AutoPilot boot scripts has been changed.
>
> Therefore, users with AutoPilot boot scripts generated using a version of **v0.9.1** or earlier should __**NOT**__ use the XML Conversion Tool with these scripts **UNLESS ALL** the following applies:
>- You're using v0.9.7 or later
>- The script is in the root `ultimate-macOS-KVM` directory
>- The matching AutoPilot blob files for the script are intact
>- The XML Conversion Tool is able to autodetect your script
>
>This is because as of v0.9.7, the XML Conversion Tool can now work using blobs - created when running AutoPilot. However, this only works when the blobs are still intact from the AP run that created your config file. They may be in the `stale` folder. If this is the case, move them to the parent `blobs` folder first.
>
>No support will be provided, and no testing has been conducted into the effects of using incompatible scripts.
>
>For the newest upstream boot script patches, you can *create a new AutoPilot config*, while preserving your existing hard disk file.
***



When first running the tool, you'll be given two options: 

**1. Convert AutoPilot config to XML**

**2. Import XML file**

This document will explain what each option does.

***
#### Convert AutoPilot config to XML

For most people, this will be the only function needed in this tool.

> [!IMPORTANT]
> If your AutoPilot boot script was created using a project version of v0.9.1 or earlier, you **MUST** read the compatibility warning above, as you probably can't use this unless several stars align.

However, if your AutoPilot script was created using v0.9.2 or later, you can continue.

Select `1. Convert AutoPilot config to XML`.

The XML Conversion Tool does a quick scan of the root `ultimate-macOS-KVM` folder. If it finds a valid AutoPilot boot script, it will ask if you'd like to use the file it automatically detected. For most, this is likely the file you want. However, if you've moved your AutoPilot script file elsewhere, or have since renamed it, etc. - then you'll be asked to provide the path to a valid AutoPilot file.

For example:
```
/users/ULTMOS/Documents/Scripts/myBootScript.sh
```
> [!WARNING]
> File paths with whitespace are not supported at this time.

Hit the ENTER key. The tool will then scan the file selected and verify that it's a valid AutoPilot script.

Then, when verified, make sure the correct file is listed, and select `1. Convert file to XML and import` from the option menu.

The conversion process will now begin. This may take a few moments. The output XML file will be saved to the same directory and with the same name as the source script. So, for example:

If you converted a script
```
/users/ULTMOS/Documents/Scripts/myBootScript.sh
```
the converted XML file would output to
```
/users/ULTMOS/Documents/Scripts/myBootScript.xml
```

Your original script with the `.sh` extension is kept, and will not be removed after conversion.

When conversion is complete, you'll be prompted to import your new XML file using `virsh`. See more in the section below.
***
#### Import XML file

Whether this was skipped during conversion, or you simply have an existing XML you'd like to import - this option helps you define a domain XML file with virsh.

You'll be asked to select a valid `.xml` file. This must be in the correct **virsh domain** format, usually looking similar to this:

```xml
<domain xmlns:qemu="http://libvirt.org/schemas/domain/qemu/1.0" type="kvm">
  <name>ultmos-130</name>
  <title>macOS 13.0 (ultimate-macOS-KVM)</title>
  <description>  macOS 13.0
  ...
  <qemu:commandline>
  <qemu:arg value="-cpu"/>
  <qemu:arg value="Skylake-Client,kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on,+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"/>
  <qemu:arg value="-global"/>
  <qemu:arg value="nec-usb-xhci.msi=off"/>
  </qemu:commandline>
</domain>
```

> [!NOTE]
> It does **NOT** have to have been created by ultimate-macOS-KVM. This function is designed to work with **ANY** domain XML file originating from anywhere.

> [!NOTE]
> You will not be asked to select an XML file if you have just used the conversion function. The newly-converted file will be used automatically.

***

<img src="https://github.com/Coopydood/ultimate-macOS-KVM/assets/39441479/ef278407-a14f-4ae7-bc23-3f635687db65" width="25%"> 

<sub>Written and maintained by **Coopydood**. </sub>
<br><sub>You can [contribute](https://github.com/Coopydood/ultimate-macOS-KVM/new/dev/docs) to documentation, too!</sub>