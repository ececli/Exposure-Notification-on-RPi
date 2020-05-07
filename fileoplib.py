#
# fileoplib.py: file Operation Library. 
import cryptolib
import os
import datetime
import csv

csvFile_prefix = "CTData_"
TEKLogFile_prefix = 'CT_TEK_'
logPath = os.getcwd()+'/KeyLog'
csvPath = os.getcwd()+'/Data'
# csvPath = os.getcwd()
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
        print('Path is not existed.')
        os.makedirs(path, exist_ok=True)
        print('Path created: ' + path)
        os.chmod(path,0o777)

def csvFileName(isEnpt = False):
    if isEnpt:
        return csvFile_prefix + datetime.datetime.now().strftime('%m%d') + "_Enpt.csv"
    else:
        return csvFile_prefix + datetime.datetime.now().strftime('%m%d') + ".csv"

def create_csvFile(isEnpt = False):
    isFolderExist(csvPath)
    fileName = csvFileName(isEnpt)
    if not os.path.exists(csvPath+'/' +fileName):
        with open(csvPath+'/' +fileName,'w') as f:
            csv_write = csv.writer(f)
            if isEnpt:
                csv_head = ["Timestamp","MAC","RSSI","UUID","RPI","AEM"]
            else:
                csv_head = ["Timestamp","MAC","RSSI","UUID","RPI","Version","TX_Power","Reserved"]
            csv_write.writerow(csv_head)
        
    os.chmod(csvPath+'/' +fileName,0o666)
    
    
def writeCSV(rowData, isEnpt = False):
    isFolderExist(csvPath)
    fileName = csvFileName(isEnpt)
    if not(os.path.exists(csvPath+'/' +fileName)):
        print(os.path.exists(csvPath+'/' +fileName))
        print('file does not exist')
        create_csvFile()
        
    with open(csvPath+'/' + fileName,'a') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(rowData)

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
    
    