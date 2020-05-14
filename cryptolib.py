
import secrets
import string
import time
import hashlib
import hmac
from math import ceil
import pyaes


TEKRollingPeriod = 144


# AES-128 ECB Mode Encryption
def aes_encrypt(key, data):
    aes = pyaes.AESModeOfOperationECB(key)
    return aes.encrypt(data)


# AES-128 ECB Mode Decryption
def aes_decrypt(key, ciphered_data):
    aes = pyaes.AESModeOfOperationECB(key)
    return aes.decrypt(ciphered_data)


# AES-128 CTR Mode Encryption
def aes_ctr_encrypt(key, iv, data):
    iv_int = int(iv.hex(), 16)
    aes_ctr = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv_int))
    return aes_ctr.encrypt(data)


# AES-128 CTR Mode Decryption
def aes_ctr_decrypt(key, iv, ciphered_data):
    iv_int = int(iv.hex(), 16)
    aes_ctr = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv_int))
    return aes_ctr.decrypt(ciphered_data)


# HKDF
hash_len = 32

def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def hkdf(key, salt, info, outputLength):
    if len(salt) == 0:
        salt = bytes([0]*hash_len)
    prk = hmac_sha256(salt, key)
    t = b""
    okm = b""
    for i in range(ceil(outputLength / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([1+i]))
        okm += t
    return okm[:outputLength]


# CRNG
def crng(outputLength):
    size = outputLength*2
    alphabet = '0123456789abcdef'
    crn = ''.join(secrets.choice(alphabet) for i in range(size))
    return bytes.fromhex(crn)


# Generate ENIntervalNumber
def getENIntervalNum():
    now = time.time()
    return int(now/600)


# Generate Temporary Exposure Key (16 bytes)
def getTEK(outputLength):
    tek = crng(outputLength)
    i = (getENIntervalNum()//TEKRollingPeriod) * TEKRollingPeriod
    return tek, i


# Generate Rolling Proximity Identifier Key
def getRPIK(tek):
    info_bytes = 'EN-RPIK'.encode('utf-8')
    return hkdf(tek, '', info_bytes, 16)


# Create PaddedData for associated RPI
def padData():
    info_bytes = 'EN-RPI'.encode('utf-8')
    zero_bytes = bytes.fromhex('000000000000')
    ENIN = getENIntervalNum()
    ENIN_hex = str(hex(ENIN).lstrip("0x"))
    ENIN_hex_le = ENIN_hex[4:] + ENIN_hex[2:4] + ENIN_hex[0:2] +  "00"
    ENIN_bytes = bytes.fromhex(ENIN_hex_le)
    return info_bytes + zero_bytes + ENIN_bytes


# Create PaddedData for associated RPI (test version)
def padData_test(ENIN):
    info_bytes = 'EN-RPI'.encode('utf-8')
    zero_bytes = bytes.fromhex('000000000000')
    ENIN_hex = str(hex(ENIN).lstrip("0x"))
    ENIN_hex_le = ENIN_hex[4:] + ENIN_hex[2:4] + ENIN_hex[0:2] +  "00"
    ENIN_bytes = bytes.fromhex(ENIN_hex_le)
    return info_bytes + zero_bytes + ENIN_bytes


# Generate Rolling Proximity Identifier 
def getRPI(rpik):
    paddedData = padData()
    return aes_encrypt(rpik, paddedData)


# Generate Associated Encrypted Metadata Key
def getAEMK(tek):
    info_bytes = 'EN-AEMK'.encode('utf-8')
    return hkdf(tek, '', info_bytes, 16)


# Generate Associated Encrypted Metadata
def getAEM(aemk, rpi, metadata):
    return aes_ctr_encrypt(aemk, rpi, metadata)


# Decrypt Metadata
def getMetadata(aemk, rpi, ciphered_metadata):
    return aes_ctr_decrypt(aemk, rpi, ciphered_metadata)
