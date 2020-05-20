#!/bin/bash
. ./ContactTracing_BLE.conf

Scanning(){
	sudo hciconfig $BLE_DEVICE up
	# sudo hciconfig $BLE_DEVICE noleadv
	# sudo hciconfig $BLE_DEVICE piscan
	echo "BLE Scanning - Start"
	sudo python3 $PYTHON_FILENAME
	if [ $? == 1 ];
	then
		echo "BLE Scanning - Failed"
		sudo hciconfig $BLE_DEVICE reset
		sleep 2
		echo "BLE Reset"
		return 1
	else
		echo "BLE Scanning - Complete"
		return 0
	fi
}
