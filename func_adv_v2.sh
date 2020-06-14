#!/bin/bash
. ./ContactTracing_BLE.conf
. ./func_bluetoothOps.sh

Advertising_stop(){
    Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x000a 00)
    if checkResult "$Var1";
    then
		echo "BLE Advertising - Stopped"
	fi
}

Advertising_start(){
    echo "BLE Advertising - Start"
    int=1
    while(( $int<$TIMEOUT ))
    do
        echo "Trial number" $int
		Var2=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x0005 $MAC)
		Var3=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x0006 $MIN_INTV $MAX_INTV $ADV_NONCONN_IND $Address_Type 00 00 00 00 00 00 00 $Adv_Ch 00)
		Var4=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x0008 1f 02 01 1a 03 03 $SERVICE_UUID_LSB $SERVICE_UUID_MSB 17 16 $SERVICE_UUID_LSB $SERVICE_UUID_MSB $RPI $MetaData)
        Var5=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x000a 01)

		if checkResult "$Var2" -a checkResult "$Var3" -a checkResult "$Var4" -a checkResult "$Var5";
        then
            echo "BLE Advertising - Successful"
            return 0
        else
            let "int++"
            if [ $int == $TIMEOUT ];
            then
                echo "BLE Advertising - Unsuccessful (Timeout)"
                bluetooth_reset
                return 1
            fi
        fi
    done

}

Advertising(){
    Advertising_start
    sleep $ADV_INTV
    Advertising_stop
    
}
