from bluepy.btle import Scanner
import csv
import os
import time
import sys

fileName = "ContactTracingData_" + time.strftime("%Y%m%d", time.localtime()) + ".csv"
FLAG = '1a'
CT_SERVICE_UUID = '00006ffd'
SCAN_WINDOW = 3.0
NUM_DESC = 3 


def create_csvFile(fileName):
     with open(fileName,'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["Timestamp","MAC","RSSI","RPI"]
        csv_write.writerow(csv_head)

if __name__ == '__main__':
    
    ts = time.time()
    scanner = Scanner()
    try:       
        devices = scanner.scan(SCAN_WINDOW)
        # devices = scanner.scan(SCAN_WINDOW, passive = True)
    except BTLEManagementError as err:
        print(err)
        sys.exit(1)

    if not os.path.exists(fileName):
        create_csvFile(fileName)

    with open(fileName,'a+') as f:
        csv_write = csv.writer(f)
        for device in devices:
            # print("Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi))
            scanData = device.getScanData()
            # scanDataLength = len(scanData)
            if len(scanData) != NUM_DESC:
                continue # if the list is not desired, then skip
            else:
                if scanData[0][0] == 1 and scanData[0][2] == FLAG and scanData[1][0] == 3 and scanData[2][0] == 22 and scanData[1][2][0:8] == CT_SERVICE_UUID:
                    RCI = scanData[2][2]
                    rowData = [ts, device.addr, device.rssi, RCI]             
                    csv_write.writerow(rowData)
                    print(rowData)
                    
      
            





