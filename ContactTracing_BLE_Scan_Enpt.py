# Encrypted version
from bluepy.btle import Scanner, BTLEManagementError
import fileoplib
import os
import time
import sys

FLAG = '1a'
CT_SERVICE_UUID = '0000fd6f'
SCAN_WINDOW = 3.0
NUM_DESC = 3 

if __name__ == '__main__':
    
    ts = time.time()
    scanner = Scanner()
    try:       
        devices = scanner.scan(SCAN_WINDOW)
        # devices = scanner.scan(SCAN_WINDOW, passive = True)
    except BTLEManagementError as err:
        print(err)
        sys.exit(1)

    fileoplib.create_csvFile(True)

    for device in devices:
        # print("Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi))
        scanData = device.getScanData()
        # scanDataLength = len(scanData)
        if len(scanData) != NUM_DESC:
            continue # if the list is not desired, then skip
        else:
            if scanData[0][0] == 1 and scanData[0][2] == FLAG and scanData[1][0] == 3 and scanData[2][0] == 22 and scanData[1][2][0:8] == CT_SERVICE_UUID:
                ServiceData = scanData[2][2]
                UUID = ServiceData[2:4] + ServiceData[0:2]
                RCI = ServiceData[4:36]
                AEM = ServiceData[36:44]
                rowData = [ts, device.addr, device.rssi, UUID, RCI, AEM]             
                fileoplib.writeCSV(rowData,True)
                print(rowData)
                    
      
            






