#!/bin/bash
. ./ContactTracing_BLE.conf
. ./func_bluetoothOps.sh
. ./func_readResult.sh

initBLE(){
	bluetooth_on
	Var0=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x007)
	TXPower=$(getTXPower "$Var0")
	echo "Transmit Power Level" $TXPower
	MetaData="$VERSION $TXPower 00 00"

}
