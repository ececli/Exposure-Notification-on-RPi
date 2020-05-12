# Cryptography Library
# by Lu Shi, ANTD/NIST
import secrets
import string
import time
import hashlib
import hmac
from math import ceil

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

EKRollingPeriod = 144


# AES-128 ECB Mode Encryption
def aes_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphered_bytes = cipher.encrypt(data)
    return ciphered_bytes

# AES-128 ECB Mode Decryption
def aes_decrypt(key, ciphered_data):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphered_data)
    return plaintext


# AES-128 CTR Mode Encryption
def aes_ctr_encrypt(key, iv, data):
    nonce = iv[:15]
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphered_bytes = cipher.encrypt(data)
    return ciphered_bytes

# AES-128 CTR Mode Decryption
def aes_ctr_decrypt(key, iv, ciphered_data):
    nonce = iv[:15]
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ciphered_data)
    plaintext = pt.hex()
    return plaintext


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
    alphabet = string.ascii_letters + string.digits
    crn = ''.join(secrets.choice(alphabet) for i in range(outputLength))
    return crn.encode('utf-8')


# Generate ENIntervalNumber
def getENIntervalNum():
    now = time.time()
    return int(now/600)

# Generate Temporary Exposure Key (16 bytes)
def getTEK(outputLength):
    tek = crng(outputLength)
    i = (getENIntervalNum()//EKRollingPeriod) * EKRollingPeriod
    return tek, i


# Generate Rolling Proximity Identifier Key
def getRPIK(tek):
    info_bytes = 'EN-RPIK'.encode('utf-8')
    return hkdf(tek, '', info_bytes, 16)


# Create PaddedData for RPI
def padData():
    info_bytes = 'EN-RPI'.encode('utf-8')
    zero_bytes = bytes.fromhex('000000000000')
    ENIN = getENIntervalNum()
    ENIN_hex = str(hex(ENIN).lstrip("0x"))
    ENIN_hex_le = ENIN_hex[4:] + ENIN_hex[2:4] + ENIN_hex[0:2] + "00"
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

# Associated Encrypted Metadata
def getAEM(aemk, rpi, metadata):
    return aes_ctr_encrypt(aemk, rpi, metadata)
