#
# fileoplib.py: file Operation Library. 
import cryptolib
import os
import datetime

TEKLogFile_prefix = 'CT_TEK_'
logPath = os.getcwd()+'/KeyLog'
keptDays = 14

def isCreatedToday(fileName):
    fileTime = datetime.datetime.fromtimestamp(os.path.getctime(fileName))        
    now = datetime.datetime.now()
    if (now - fileTime).days == 0:
        return True
    else:
        return False

def isFolderExist(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


# Write Temporary Exposure Key
def writeTEK(tek, fileName):
    # if the file is existed and just generated today, then do no replace it
    if os.path.exists(fileName) and isCreatedToday(fileName):
        return False
    with open(fileName, 'wb') as fb:
        fb.write(tek)
    return True

def genTEKFile(fileName):
    tek, i = cryptolib.getTEK(16)
    success = writeTEK(tek, fileName)
    # After generating tek, log the tek and delete the old files
    logTEK(fileName)
    delOldFiles()
    return tek, success


def writeConfig(MAC,rpi_hex,aem_hex,fileName):
    with open(fileName,'w+') as fb:
        fb.write("export MAC=\""+MAC+"\"\n")
        fb.write("export RPI=\""+' '.join(a+b for a,b in zip(rpi_hex[::2], rpi_hex[1::2]))+"\"\n")
        fb.write("export AEM=\""+' '.join(a+b for a,b in zip(aem_hex[::2], aem_hex[1::2]))+"\"")
    return True

# Read Temporary Exposure Key
def readTEK(fileName):
    if os.path.exists(fileName) and isCreatedToday(fileName):
        with open(fileName, 'rb') as fb:
            tek = fb.read()
        return tek
    tek, success = genTEKFile(fileName)
    return tek

def logTEK(TEKFile):
    isFolderExist(logPath)
    fileName = TEKLogFile_prefix + datetime.datetime.now().strftime('%m%d') + ".log"
    if not(os.path.exists(logPath+'/' +fileName)):
        with open(logPath+'/' +fileName, 'wb') as fb:
            fb.write(readTEK(TEKFile))
        return True
    return False

def delOldFiles():
    ds = list(os.walk(logPath))
    for d in ds:
        if d[2] != []:
            for x in d[2]:
                fileTime = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(logPath,x)))
                now = datetime.datetime.now()
                if (now - fileTime).days > keptDays:
                    os.remove(os.path.join(logPath,x))
    return 0


    
# def writeRPILog():
    
    