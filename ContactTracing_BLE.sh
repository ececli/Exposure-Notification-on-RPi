#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_scan.sh

Address_Type=$PUBLIC_ADDR
Adv_Ch=$ADV_CHANNEL

initBLE

while true
do
    Advertising
    sleep $ADV_INTV
    Scanning
done

