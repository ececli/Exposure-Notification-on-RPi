#!/bin/bash
. ./ContactTracing_BLE.conf
. ./STATIC_RPI.conf

checkResult(){
    Input=$1
    echo $Input
    Var=${Input##'<'*'>'}
    [ "${Var:12:4}" = '0x0e' ] && [ "${Var:${#Var}-3:2}" = '00' ]
}

getTXPower(){
    Input=$1
    Var=${Input##'<'*'>'}
    if [ "${Var:12:4}" = '0x0e' ] && [ "${Var:${#Var}-6:2}" = '00' ];
    then 
        echo ${Var:${#Var}-3:2}
    else
        echo 'NaN'
    fi
}

Advertising(){

    index=$1
    echo " BLE Advertising - Start On Channel: " `expr $index + 37`
    int=1
    while(( $int<$TIMEOUT ))
    do
        echo "Trial number" $int
        sudo hciconfig $BLE_DEVICE noscan
        Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x00a 00)
        # Var2=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x005 $MAC)
        Var3=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x006 $MIN_INTV $MAX_INTV $ADV_NONCONN_IND $PUBLIC_ADDR 00 00 00 00 00 00 00 ${Adv_Channels[$index]} 00)
        Var4=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x008 1f 02 01 1a 03 03 $SERVICE_UUID_LSB $SERVICE_UUID_MSB 17 16 $SERVICE_UUID_LSB $SERVICE_UUID_MSB $RPI $VERSION $TXPower ${Adv_Channels[$index]} 00)
        Var5=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x00a 01)

        if checkResult "$Var3" -a checkResult "$Var4" -a checkResult "$Var5";
        # if checkResult "$Var2" -a checkResult "$Var3" -a checkResult "$Var4" -a checkResult "$Var5";
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

sudo hciconfig $BLE_DEVICE up
echo "Bluetooth - Power Up"
Var0=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x007)
TXPower=$(getTXPower "$Var0")
echo "Transmit Power Level" $TXPower

Adv_Channels=('01' '02' '04')
chnIndex=0

while true
do

    Advertising $chnIndex
    let "chnIndex++"
    if [ $chnIndex == 3 ];
    then
        chnIndex=0
    fi
    sleep $SCAN_INTV
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
    else
        echo "BLE Scanning - Complete"
    fi

done

