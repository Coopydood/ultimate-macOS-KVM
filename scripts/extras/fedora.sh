#!/bin/sh

# Fixes for Fedora's SELinux integration within this repository.*
# Needs to be run with sudo.
# * = Testing, script is not ready until conformation.

sudo ausearch -c 'rpc-virtqemud' --raw | audit2allow -M my-rpcvirtqemud
sudo semodule -i my-rpcvirtqemud.pp
sudo semodule -i my-rpcvirtqemud.pp
sudo semodule -X 300 my-qemusystemx86.pp
