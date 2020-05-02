import cryptolib
import random
from os import path

TEK_fileName = 'TEK.txt'
META_fileName = 'MetaData.txt'
RPI_AEM_fileName = "MAC_RPI_AEM.config"
RPI_AEM_logFileName = "GenRPI.log"
# Read Temporary Exposure Key
if path.exists(TEK_fileName):
    with open(TEK_fileName, 'rb') as fb:
        tek = fb.read()
else:
    tek, i = cryptolib.getTEK(16)
    with open('TEK.txt', 'wb') as fb:
        fb.write(tek)
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
with open(RPI_AEM_fileName,'w+') as fb:
    fb.write("export MAC=\""+MAC+"\"\n")
    fb.write("export RPI=\""+' '.join(a+b for a,b in zip(rpi_hex[::2], rpi_hex[1::2]))+"\"\n")
    fb.write("export AEM=\""+' '.join(a+b for a,b in zip(aem_hex[::2], aem_hex[1::2]))+"\"")
    
    

# with open(RPI_AEM_logFileName,'a+') as fb:
    # fb.write()