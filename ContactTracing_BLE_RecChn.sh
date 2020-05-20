#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_scan.sh

Address_Type=$PUBLIC_ADDR
Adv_Ch=$ADV_CHANNEL

Adv_Channels=('01' '02' '04')
chnIndex=0

initBLE

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
    Advertising
    sleep $ADV_INTV
    Scanning
done

