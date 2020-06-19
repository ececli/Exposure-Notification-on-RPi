#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv_v2.sh
. ./func_scan_v2.sh
. ./func_fullLog.sh
. ./func_bluetoothOps.sh

Address_Type=$PUBLIC_ADDR
Adv_Ch=$ADV_CHANNEL
Adv_Counter=1
Scan_Counter=1

Adv_Channels=('01' '02' '04')
chnIndex=0

initBLE

log_header

while true
do
    let "chnIndex++"
    if [ $chnIndex == 3 ];
    then
        chnIndex=0
    fi
    Adv_Ch=${Adv_Channels[$chnIndex]}
    MetaData=${MetaData:0:9}$Adv_Ch
    echo " BLE Advertising Channel: " `expr $chnIndex + 37`
    # begin advertising
    log_startAdv $Adv_Counter
    Advertising_start
    if [ $? == 1 ];
    then
	log_advFailed $Adv_Counter
	echo "BLE Advertising - Fail"
	let "Adv_Counter++"
    else
	log_advSuccessful $Adv_Counter
	echo "BLE Advertisement " $Adv_Counter
	let "Adv_Counter++"
    fi
    # sleep $ADV_INTV
    randAdvTime=$( awk -v min=$ADV_INTV -v max=$ADV_INTV_RANDMAX 'BEGIN{ "date +%N" | getline seed; srand(seed); print min+rand()*(max-min)}' )
    sleep $randAdvTime
    Advertising_stop
    # begin scanning
    log_startScan $Scan_Counter
    Scanning
    if [ $? == 1 ];
    then
	log_scanFailed $Scan_Counter
	echo "BLE Scanning - Fail"
	let "Scan_Counter++"
    else
	log_scanSuccessful $Scan_Counter
	echo "BLE Scan " $Scan_Counter
	let "Scan_Counter++"
    fi
done

