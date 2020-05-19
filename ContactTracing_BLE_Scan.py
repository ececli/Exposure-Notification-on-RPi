# Unencrypted version
from bluepy.btle import Scanner, BTLEManagementError
import os
import sys
import time
import fileoplib
import random

FLAG = '1a'
CT_SERVICE_UUID = '0000fd6f'
NUM_DESC = 3
# Scan window is uniformly random 
SCAN_WINDOW_MIN = 3.0
SCAN_WINDOW_MAX = 4.0

if __name__ == '__main__':
    
    ts = time.time()
    scanner = Scanner()
    scan_Window = random.uniform(SCAN_WINDOW_MIN,SCAN_WINDOW_MAX)
    try:       
        devices = scanner.scan(scan_Window)
        # devices = scanner.scan(SCAN_WINDOW, passive = True)
    except BTLEManagementError as err:
        print(err)
        sys.exit(1)

    fileoplib.create_csvFile(False)

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
                Version = ServiceData[36:38]
                TXPower = ServiceData[38:40]
                Reserved = ServiceData[40:44]
                rowData = [ts, device.addr, device.rssi, UUID, RCI, Version, TXPower, Reserved]             
                fileoplib.writeCSV(rowData,False)
                print(rowData)
