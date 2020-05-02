import cryptolib

metadata = bytes.fromhex('400C0000')

# Get Temporary Exposure Key
tek, i = cryptolib.getTEK(16)
print('\nTemporary Exposure Key:', tek)
print('TEK length:', len(tek), '\n')

# Get Rolling Proximity Identifier Key
rpik = cryptolib.getRPIK(tek)
print('Rolling Proximity Identifier Key:', rpik)
print('RPIK length:', len(rpik), '\n')

# Get Rolling Proximity Identifier Key
rpik2 = cryptolib.getRPIK(tek)
print('Rolling Proximity Identifier Key:', rpik2)
print('RPIK length:', len(rpik2), '\n')

# Get Rolling Proximity Identifier
rpi = cryptolib.getRPI(rpik)
print('Rolling Proximity Identifier: ', rpi.hex())
print('RPI length:', len(rpi), '\n')

# Get Associated Encrypted Metadata Key
aemk = cryptolib.getAEMK(tek)
print('Associated Encrypted Metadata Key: ', aemk)
print('AEMK len:', len(aemk), '\n')

# Get Associated Encrypted Metadata
aem = cryptolib.getAEM(aemk, rpi, metadata)
print('Associated Encrypted Metadata: ', aem.hex())
print('AEM len:', len(aem), '\n')