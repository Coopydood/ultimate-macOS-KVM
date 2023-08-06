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
NAME="macOS"
FILE="bootExample.sh"

IGNORE_FILE=0
REQUIRES_SUDO=0
VFIO_PTA=0
GEN_EPOCH=1691275656

SCREEN_RES="1280x720"

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

NETWORK_DEVICE="vmxnet3"
MAC_ADDRESS="00:16:cb:00:21:09"

#   You should not have to touch anything below this line, especially if you
#   don't really know what you're doing. It'll probably break something.

args=(
-global ICH9-LPC.acpi-pci-hotplug-with-bridge-support=off
-enable-kvm -m "$ALLOCATED_RAM" -cpu "$CPU_MODEL",kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on,"$CPU_FEATURE_ARGS"
-machine q35
-usb -device usb-kbd -device usb-tablet #USB_DEV
-smp "$CPU_THREADS",cores="$CPU_CORES",sockets="$CPU_SOCKETS"
-device usb-ehci,id=ehci
-device qemu-xhci,id=xhci
-device pcie-root-port,bus=pcie.0,slot=1,x-speed=16,x-width=32
#VFIO_DEV_BEGIN
#VFIO_DEV_END
-device isa-applesmc,osk="ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
-drive if=pflash,format=raw,readonly=on,file="$REPO_PATH/$OVMF_DIR/OVMF_CODE.fd"
-drive if=pflash,format=raw,file="$REPO_PATH/$OVMF_DIR/OVMF_VARS.fd"
-smbios type=2
-device ich9-intel-hda -device hda-duplex
-device ich9-ahci,id=sata
-drive id=OpenCore,if=none,snapshot=on,format=qcow2,file="$REPO_PATH/boot/OpenCore.qcow2"
-drive id=HDD,if=none,file="$REPO_PATH/HDD.qcow2",format=qcow2
-device ide-hd,bus=sata.2,drive=OpenCore
-device ide-hd,bus=sata.3,drive=HDD

############## REMOVE THESE LINES AFTER MACOS INSTALLATION ###############
-drive id=BaseSystem,if=none,file="$REPO_PATH/BaseSystem.img",format=raw
-device ide-hd,bus=sata.4,drive=BaseSystem
##########################################################################

-netdev user,id=net0 -device "$NETWORK_DEVICE",netdev=net0,id=net0,mac="$MAC_ADDRESS"
-device qxl-vga,vgamem_mb=128,vram_size_mb=128
-monitor stdio
#-display none
#-vga qxl

################ UNCOMMENT IF YOU WANT TO USE VNC MONITOR ################
#-vnc 0.0.0.0:1,password=on -k en-us
##########################################################################

)

qemu-system-x86_64 "${args[@]}"