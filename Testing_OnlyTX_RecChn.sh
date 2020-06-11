#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_fullLog.sh

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

done

