#!/usr/bin/env bash
# shellcheck disable=SC2054

# APC-RUN_2022-12-28_12-21-20

############################################################
#	YOU CAN USE THIS FILE TO MANUALLY CREATE A BOOT SCRIPT #
#	INSTEAD OF USING AUTOPILOT.                            #
############################################################

#
#	Created by Coopydood as part of the ultimate-macOS-KVM project.
#
#	Profile: https://github.com/Coopydood
#	Repo: https://github.com/Coopydood/ultimate-macOS-KVM
#
#	Adapted from OSX-KVM among others.
#	Greetz to TheNickDude, Dortania, khoalia, foxlet, and other contributors :]
#


ID="macOS"
NAME="macOS 10.15"
FILE="boot.sh"

ALLOCATED_RAM="4G"
CPU_SOCKETS="1"
CPU_CORES="2"
CPU_THREADS="4"
CPU_MODEL="Penryn"
CPU_FEATURE_ARGS="+ssse3,+sse4.2,+popcnt,+avx,+aes,+xsave,+xsaveopt,check"

REPO_PATH="."
OVMF_DIR="./ovmf"
VFIO_ID_0="$USR_VFIO_ID_0"
VFIO_ID_1="$USR_VFIO_ID_1"
VFIO_ROM="$USR_VFIO_ROM"

USB_DEVICES="$USR_USB_DEVICES"
NETWORK_DEVICE="e1000-82545em"


args=(
-global ICH9-LPC.acpi-pci-hotplug-with-bridge-support=off
-enable-kvm -m "$ALLOCATED_RAM" -cpu "$CPU_MODEL",kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on,"$CPU_FEATURE_ARGS"
-machine q35
-usb -device usb-kbd -device usb-tablet #USB_DEVS_0 "$USB_DEVICES"
-smp "$CPU_THREADS",cores="$CPU_CORES",sockets="$CPU_SOCKETS"
-device usb-ehci,id=ehci
-device pcie-root-port,bus=pcie.0,id=rp1,slot=1,x-speed=16,x-width=32
#VFIO_0 -device vfio-pci,host="$VFIO_ID_0",multifunction=on,romfile="$VFIO_ROM",bus=rp1,addr=0x0.0
#VFIO_1 -device vfio-pci,host="$VFIO_ID_1",bus=rp1,addr=0x0.1
-device isa-applesmc,osk="ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
-drive if=pflash,format=raw,readonly=on,file="$REPO_PATH/$OVMF_DIR/OVMF_CODE.fd"
-drive if=pflash,format=raw,file="$REPO_PATH/$OVMF_DIR/OVMF_VARS-1024x768.fd"
-smbios type=2
-device ich9-intel-hda -device hda-duplex
-device ich9-ahci,id=sata
-drive id=OpenCore,if=none,snapshot=on,format=qcow2,file="$REPO_PATH/OpenCore/OpenCore.qcow2"
-drive id=BaseSystem,if=none,file="$REPO_PATH/BaseSystem.img",format=raw
-drive id=HDD,if=none,file="$REPO_PATH/HDD.qcow2",format=qcow2
-device ide-hd,bus=sata.2,drive=OpenCore
-device ide-hd,bus=sata.3,drive=HDD
-device ide-hd,bus=sata.4,drive=BaseSystem
-netdev user,id=net0 -device "$NETWORK_DEVICE",netdev=net0,id=net0,mac=00:16:cb:00:21:09
-vga qxl
-monitor stdio

)

qemu-system-x86_64 "${args[@]}"
