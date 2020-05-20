#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf
. ./func_readResult.sh
. ./func_initBLE.sh
. ./func_adv.sh
. ./func_scan.sh

Address_Type=$RANDOM_ADDR
Adv_Ch=$ADV_CHANNEL

initBLE
echo $MetaData > $METADATA_FILENAME

while true
do
    . ./MAC_RPI_AEM.config
    MetaData=$AEM
    Advertising
    sleep $ADV_INTV
    Scanning
done









