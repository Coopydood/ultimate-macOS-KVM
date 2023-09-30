#!/usr/bin/bash

# Simple handoff conversion script utilising dmg2img
# Created by Coopydood for ultimate-macOS-KVM

./resources/dmg2img ./BaseSystem.dmg
rm ./BaseSystem.dmg

echo 
echo SUCCESS: The BaseSystem file you downloaded was converted and placed into the ultimate-macOS-KVM folder for you.
echo