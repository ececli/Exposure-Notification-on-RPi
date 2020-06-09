#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_scan.sh
. ./func_fullLog.sh

Address_Type=$PUBLIC_ADDR
Adv_Ch=$ADV_CHANNEL
Adv_Counter=1
Scan_Counter=1

initBLE

log_header

while true
do
	log_startAdv $Adv_Counter
	Advertising
	if [ $? == 1 ];
	then
		log_advFailed $Adv_Counter
		echo "BLE Advertising - Fail"
	else
		log_advSuccessful $Adv_Counter
		echo "BLE Advertisement " $Adv_Counter
		let "Adv_Counter++"
	fi
	sleep $ADV_INTV
	log_startScan $Scan_Counter
	Scanning_v2 $Scan_Counter
	if [ $? == 1 ];
	then
		log_scanFailed $Scan_Counter
		echo "BLE Scanning - Fail"
	else
		log_scanSuccessful $Scan_Counter
		echo "BLE Scan " $Scan_Counter
		let "Scan_Counter++"
	fi
done
