#!/bin/bash
. ./ContactTracing_BLE.conf

Advertising(){
    echo "BLE Advertising - Start"
    int=1
    while(( $int<$TIMEOUT ))
    do
        echo "Trial number" $int
        sudo hciconfig $BLE_DEVICE noscan
        Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x00a 00)
		Var2=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x005 $MAC)
		Var3=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x006 $MIN_INTV $MAX_INTV $ADV_NONCONN_IND $Address_Type 00 00 00 00 00 00 00 $Adv_Ch 00)
		Var4=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x008 1f 02 01 1a 03 03 $SERVICE_UUID_LSB $SERVICE_UUID_MSB 17 16 $SERVICE_UUID_LSB $SERVICE_UUID_MSB $RPI $MetaData)
        Var5=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x00a 01)

		if checkResult "$Var2" -a checkResult "$Var3" -a checkResult "$Var4" -a checkResult "$Var5";
        then
            echo "BLE Advertising - Successful"
            return 0
        else
            let "int++"
            if [ $int == $TIMEOUT ];
            then
                echo "BLE Advertising - Unsuccessful (Timeout)"
                sudo hciconfig $BLE_DEVICE down
                return 1
            fi
        fi
    done

}
