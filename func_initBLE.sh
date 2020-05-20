#!/bin/bash
. ./ContactTracing_BLE.conf

initBLE(){
	sudo hciconfig $BLE_DEVICE up
	echo "Bluetooth - Power Up"
	Var0=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x007)
	TXPower=$(getTXPower "$Var0")
	echo "Transmit Power Level" $TXPower
	MetaData="$VERSION $TXPower 00 00"

}
