#!/bin/bash
shopt -s nullglob
for g in `find /sys/kernel/iommu_groups/* -maxdepth 0 -type d | sort -V`; do
    echo "IOMMU Group ${g##*/}:"
    for d in $g/devices/*; do
        echo -e "\t$(lspci -nns ${d##*/})"
        
    done;
done;
    echo ""
    echo "WARNING: The devices you want to pass through, i.e. GPUs, *MUST* be in their own IOMMU group."
    echo ""
