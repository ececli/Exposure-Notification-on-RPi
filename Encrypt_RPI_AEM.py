# This file is executed automatically every 15 min
import cryptolib
import random
from os import path
import fileoplib

# TEK_fileName = 'TEK.txt'
META_fileName = 'MetaData.txt'
# RPI_AEM_fileName = "MAC_RPI_AEM.config"
# RPI_AEM_logFileName = "GenRPI.log"
# Read Temporary Exposure Key
tek = fileoplib.readTEK()
print('TEK: ', tek)
# Read Metadata
if path.exists(META_fileName):
    with open(META_fileName, 'r') as fb:
        metadata = fb.read()
else:
    metadata = bytes.fromhex('400C0000')
# Get Rolling Proximity Identifier Key
# rpik = cryptolib.getRPIK(tek)
# Get Rolling Proximity Identifier
rpi = cryptolib.getRPI(cryptolib.getRPIK(tek))
rpi_hex = rpi.hex()
print('RPI: ', rpi_hex)
# Get Associated Encrypted Metadata Key
# aemk = cryptolib.getAEMK(tek)
# Get Associated Encrypted Metadata
aem = cryptolib.getAEM(cryptolib.getAEMK(tek), rpi, metadata)
aem_hex = aem.hex()
print('AEM: ', aem_hex)
# Generate random private MAC address
while True:
    MAC = "%02x %02x %02x %02x %02x %02x" % (random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 63)) # Note that MSB is in the end
    if not(MAC == '00 00 00 00 00 00' or MAC == 'ff ff ff ff ff 3f'):
        break 
print('MAC: ', MAC)    
fileoplib.writeConfig(MAC,rpi_hex,aem_hex)

# with open(RPI_AEM_logFileName,'a+') as fb:
    # fb.write()
