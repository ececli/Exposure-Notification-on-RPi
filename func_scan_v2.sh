#!/bin/bash
. ./ContactTracing_BLE.conf
. ./func_bluetoothOps.sh
. ./func_readResult.sh

read_message(){
	rawMsg=""
	while read line;
	do
		if [[ $line =~ ^\> ]]; 
		then
			# first, decode the message if it is not empty
			if [[ $rawMsg ]]; 
			then
				decode_message "$rawMsg"
				rawMsg=""
			fi
			# then write the line to the message
			rawMsg=$line		
		else
			# if the message is not finished, then add the line to the current message
			rawMsg="$rawMsg $line"
		fi
	done
}

# Note that for the testing purpose, we add Scan_Counter into csv file
decode_message(){
	Input=$1
	msg=${Input//[ >]/} # remove space and > 
	if [[ $msg =~ ^043E2B0201.{16}1F02011A03036FFD17166FFD ]];
	then
		# decode the message 
		TS=$(date +%s%3N)
		msg_MacAddr_type="${msg:12:2}"
		msg_MacAddr="${msg:24:2}:${msg:22:2}:${msg:20:2}:${msg:18:2}:${msg:16:2}:${msg:14:2}"
		msg_RPI=${msg:50:32}
		msg_metadata=${msg:82:8}
		msg_RSSI="0x${msg:90:2}"
		msg_RSSI_dB=$[$((0x${msg:90:2})) - 256] 	
		echo "$TS,$msg_MacAddr_type,$msg_MacAddr,$msg_RPI,$msg_metadata,$msg_RSSI_dB,$msg_RSSI,$Scan_Counter" >> $csvFILENAME
		echo "$TS,$msg_MacAddr_type,$msg_MacAddr,$msg_RPI,$msg_metadata,$msg_RSSI_dB,$msg_RSSI,$Scan_Counter"
	fi
}

checkCSVFile(){
	if [[ ! -d $CSV_FILENAME_FOLDER ]];
	then
		mkdir $CSV_FILENAME_FOLDER
	fi

	if [[ ! -f $csvFILENAME ]];
	then
		touch $csvFILENAME
		echo $DATA_CSVHEADER >> $csvFILENAME
	fi
}


Scanning_stop(){
	Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x000c 00 $FILTER_DUPLICATES)
    if checkResult "$Var1";
    then
		echo "BLE Scanning - Stopped"
	fi
}

Scanning_start(){
	Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x000c 01 $FILTER_DUPLICATES)
	if checkResult "$Var1";
    then
		echo "BLE Scanning - Started"
		return 0
	else
		return 1
	fi
}

Scanning_setting(){
	Var1=$(sudo hcitool -i $BLE_DEVICE cmd 0x08 0x000b 00 $BLESCAN_INTV $BLESCAN_WIN 00 00)
    if checkResult "$Var1";
    then
		echo "BLE Scanning - Set Successfully"
	fi
}

Scanning(){
	csvFILENAME=$CSV_FILENAME_FOLDER$CSV_FILENAME_PREFIX$(date -u +"%m%d")$CSV_FILENAME_FILETYPE
	checkCSVFile
	Scanning_setting
	int=1
    while(( $int<$TIMEOUT ))
    do
		echo "Trial number" $int
		Scanning_start
		if [ $? == 1 ];
		then
			Scanning_stop
			let "int++"
            if [ $int == $TIMEOUT ];
            then
				echo "BLE Scanning - Unsuccessful (Timeout)"
                bluetooth_reset
                return 1
            fi
		else
			break
		fi
	done
	sudo timeout -s INT $SCAN_INTV hcidump -i $BLE_DEVICE -R --raw | read_message
	Scanning_stop
	echo "BLE Scanning - Complete"
	return 0
	
}
