#!/bin/sh

# Fixes for Fedora's SELinux integration within this repository.*
# Needs to be run with sudo.
# * = Testing, script is not ready until conformation.

sudo semanage fcontext -a -t virt_image_t 'OVMF_CODE.fd'
sudo restorecon -v 'OVMF_CODE.fd'
sudo ausearch -c 'rpc-virtqemud' --raw | audit2allow -M my-rpcvirtqemud
sudo semodule -i my-rpcvirtqemud.pp
sudo semanage fcontext -a -t virt_image_t 'OVMF_CODE.fd'
sudo restorecon -v 'OVMF_CODE.fd'
sudo ausearch -c 'qemu-system-x86' --raw | audit2allow -M my-qemusystemx86
sudo semodule -X 300 -i my-qemusystemx86.pp
# This next line may need to be tweaked to be a universal file path to the OVMF file included in the repository
sudo semanage fcontext -a -t virt_image_t '/home/auorafirewood/ultimate-macOS-KVM/ovmf/OVMF_CODE.fd'
sudo ausearch -c 'qemu-system-x86' --raw | audit2allow -M my-qemusystemx86
