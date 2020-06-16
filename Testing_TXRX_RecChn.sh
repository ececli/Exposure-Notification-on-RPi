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
beginningTime=$(date +%s)
endTime=`expr $beginningTime + 180`
echo $endTime, $beginningTime
while [ $(date +%s)  -lt $endTime ]
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
    sleep $ADV_INTV
    Advertising_stop
done
Scanning

