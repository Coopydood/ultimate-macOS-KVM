# debug-rs
# Internal debug command used to reset stale AP-gen'd files.

rm ./boot.sh
rm ./resources/config.sh
rm ./blobs/*.apb
rm ./HDD.qcow2
rm ./boot-noPT.sh
rm ./vfio-args.txt
rm -rf ./boot/*
rm ./ovmf/OVMF_CODE.fd
rm ./ovmf/OVMF_VARS.fd
echo  
echo AutoPilot working files reset.
echo  
