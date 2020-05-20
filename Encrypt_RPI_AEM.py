# This file is executed automatically every 15 min
import cryptolib
import random
from os import path
import fileoplib

# Read Temporary Exposure Key
tek = fileoplib.readTEK()
print('TEK: ', tek)
# Read Metadata
metadata = fileoplib.readMeta()
print('META: ', metadata.hex())
# Get Rolling Proximity Identifier
rpi = cryptolib.getRPI(cryptolib.getRPIK(tek))
rpi_hex = rpi.hex()
print('RPI: ', rpi_hex)
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
