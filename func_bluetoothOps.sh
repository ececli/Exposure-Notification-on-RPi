#!/bin/bash
. ./ContactTracing_BLE.conf

bluetooth_off(){
	sudo hciconfig $BLE_DEVICE down
	echo "WARNING: BLUETOOTH - POWER DOWN"
}

bluetooth_on(){
	sudo hciconfig $BLE_DEVICE up
	echo "BLUETOOTH - POWER UP"
}

bluetooth_reset(){
	sudo hciconfig $BLE_DEVICE reset
	echo "WARNING: BLUETOOTH - RESET"
}
