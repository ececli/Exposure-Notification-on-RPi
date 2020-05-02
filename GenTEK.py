import cryptolib
# Generate Temporary Exposure Key
tek, i = cryptolib.getTEK(16)
print(tek)
with open('TEK.txt', 'wb') as fb:
    fb.write(tek)