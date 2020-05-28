#!/bin/bash
. ./ContactTracing_BLE.conf

log_header(){
	echo "Timestamp,isScanning,Counter,isSuccessful,isFinished" > $FULLLOG_FILENAME
}

log_startAdv(){
	Input=$1
	echo "$(date +%s%3N),0,$Input,1,0" >> $FULLLOG_FILENAME
}

log_advFailed(){
	Input=$1
	echo "$(date +%s%3N),0,$Input,0,1" >> $FULLLOG_FILENAME
}

log_advSuccessful(){
	Input=$1
	echo "$(date +%s%3N),0,$Input,1,1" >> $FULLLOG_FILENAME
}

log_startScan(){
	Input=$1
	echo "$(date +%s%3N),1,$Input,1,0" >> $FULLLOG_FILENAME
}

log_scanFailed(){
	Input=$1
	echo "$(date +%s%3N),1,$Input,0,1" >> $FULLLOG_FILENAME
}

log_scanSuccessful(){
	Input=$1
	echo "$(date +%s%3N),1,$Input,1,1" >> $FULLLOG_FILENAME
}
