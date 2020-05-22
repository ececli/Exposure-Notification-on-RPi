#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_scan.sh

Address_Type=$PUBLIC_ADDR
Adv_Ch=$ADV_CHANNEL
Adv_Counter=0
Scan_Counter=0

initBLE

while true
do
    Advertising
    if [ $? == 1 ];
	then
		echo "BLE Advertising - Fail"
	else
		let "Adv_Counter++"
		echo "BLE Advertisement " $Adv_Counter
	fi
    sleep $ADV_INTV
    Scanning
    if [ $? == 1 ];
	then
		echo "BLE Scanning - Fail"
	else
		let "Scan_Counter++"
		echo "BLE Scan " $Scan_Counter
	fi
done

