#
# fileoplib.py: file Operation Library.
# by Chang Li. ANTD/ITL/NIST
import cryptolib
import os
import datetime
import csv

csvFile_prefix = "CTData_"
TEKLogFile_prefix = 'CT_TEK_'
logPath = os.getcwd()+'/KeyLog'
csvPath = os.getcwd()+'/Data'
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

# # Write Temporary Exposure Key and i
# def writeTEK(tek, i, fileName):
#     # if the file is existed and just generated today, then do no replace it
#     if os.path.exists(fileName) and isCreatedToday(fileName):
#         return False
#     with open(fileName, 'wb') as fb:
#         fb.write(tek)
#     return True

# Write Temporary Exposure Key and i
def logTEK(tek,i):
    isFolderExist(logPath)
    TEKFileName = TEKLogFile_prefix + datetime.datetime.now().strftime('%m%d') + ".log"
    iFileName = TEKLogFile_prefix + "i_" + datetime.datetime.now().strftime('%m%d') + ".log"
    if not(os.path.exists(logPath+'/' +TEKFileName) and os.path.exists(logPath+'/' +iFileName)):
        with open(logPath+'/' +TEKFileName, 'wb') as fb:
            fb.write(tek)
        with open(logPath+'/' +iFileName, 'w') as f:
            f.write(str(i))
        return True
    return False

def genTEKFile():
    tek, i = cryptolib.getTEK(16)
    print(tek)
    print(i)
    success = logTEK(tek,i)
    # After generating tek, log the tek and delete the old files
    # logTEK(fileName)
    delOldFiles(logPath)
    delOldFiles(csvPath)
    return tek, success



# # Read Temporary Exposure Key
# def readTEK(fileName):
#     if os.path.exists(fileName) and isCreatedToday(fileName):
#         with open(fileName, 'rb') as fb:
#             tek = fb.read()
#         return tek
#     tek, success = genTEKFile(fileName)
#     return tek

# Read Temporary Exposure Key
def readTEK():
    isFolderExist(logPath)
    TEKFileName = TEKLogFile_prefix + datetime.datetime.now().strftime('%m%d') + ".log"
    iFileName = TEKLogFile_prefix + "i_" + datetime.datetime.now().strftime('%m%d') + ".log"
    if os.path.exists(logPath+'/' +TEKFileName) and os.path.exists(logPath+'/' +iFileName):
        with open(logPath+'/' +TEKFileName, 'rb') as fb:
            tek = fb.read()
        return tek
    tek, success = genTEKFile()
    return tek



def delOldFiles(Path):
    ds = list(os.walk(Path))
    for d in ds:
        if d[2] != []:
            for x in d[2]:
                fileTime = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(Path,x)))
                now = datetime.datetime.now()
                if (now - fileTime).days > keptDays:
                    os.remove(os.path.join(Path,x))
    return 0


def writeConfig(MAC,rpi_hex,aem_hex,fileName):
    with open(fileName,'w+') as fb:
        fb.write("export MAC=\""+MAC+"\"\n")
        fb.write("export RPI=\""+' '.join(a+b for a,b in zip(rpi_hex[::2], rpi_hex[1::2]))+"\"\n")
        fb.write("export AEM=\""+' '.join(a+b for a,b in zip(aem_hex[::2], aem_hex[1::2]))+"\"")
    return True
