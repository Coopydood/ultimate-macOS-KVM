# debug-rs
# Internal debug command used to reset stale AP-gen'd files.

rm ./boot.sh > /dev/null 2>&1
rm ./resources/config.sh > /dev/null 2>&1
rm ./blobs/*.apb > /dev/null 2>&1
rm ./blobs/user/*.apb > /dev/null 2>&1
rm ./HDD.qcow2 > /dev/null 2>&1
rm ./boot-noPT.sh > /dev/null 2>&1
rm ./vfio-args.txt > /dev/null 2>&1
rm -rf ./boot/* > /dev/null 2>&1
rm ./ovmf/OVMF_CODE.fd > /dev/null 2>&1
rm ./ovmf/OVMF_VARS.fd > /dev/null 2>&1
rm ./boot.xml > /dev/null 2>&1
echo  
echo AutoPilot working files reset.
echo  
