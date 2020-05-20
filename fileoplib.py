#
# fileoplib.py: file Operation Library.
# by Chang Li. ANTD/ITL/NIST
import os
import csv
import cryptolib
import datetime
import loadConfig as cf


# csvFile_prefix = "CTData_"
# TEKLogFile_prefix = 'CT_TEK_'
# logPath = os.getcwd()+'/KeyLog'
# csvPath = os.getcwd()+'/Data'
# keptDays = 14

def isCreatedToday(fileName):
    fileTime = datetime.datetime.fromtimestamp(os.path.getctime(fileName))        
    now = datetime.datetime.utcnow()
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
        return cf.csvFile_prefix + datetime.datetime.utcnow().strftime('%m%d') + "_Enpt.csv"
    else:
        return cf.csvFile_prefix + datetime.datetime.utcnow().strftime('%m%d') + ".csv"

def create_csvFile(isEnpt = False):
    isFolderExist(cf.csvPath)
    fileName = csvFileName(isEnpt)
    if not os.path.exists(cf.csvPath+'/' +fileName):
        with open(cf.csvPath+'/' +fileName,'w') as f:
            csv_write = csv.writer(f)
            if isEnpt:
                csv_head = ["Timestamp","MAC","RSSI","UUID","RPI","AEM"]
            else:
                csv_head = ["Timestamp","MAC","RSSI","UUID","RPI","Version","TX_Power","Reserved"]
            csv_write.writerow(csv_head)
        
    os.chmod(cf.csvPath+'/' +fileName,0o666)
    
    
def writeCSV(rowData, isEnpt = False):
    isFolderExist(cf.csvPath)
    fileName = csvFileName(isEnpt)
    if not(os.path.exists(cf.csvPath+'/' +fileName)):
        print(os.path.exists(cf.csvPath+'/' +fileName))
        print('file does not exist')
        create_csvFile()
        
    with open(cf.csvPath+'/' + fileName,'a') as f:
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
    isFolderExist(cf.logPath)
    TEKFileName = cf.TEKLogFile_prefix + datetime.datetime.utcnow().strftime('%m%d') + ".log"
    iFileName = cf.TEKLogFile_prefix + "i_" + datetime.datetime.utcnow().strftime('%m%d') + ".log"
    if not(os.path.exists(cf.logPath+'/' +TEKFileName) and os.path.exists(cf.logPath+'/' +iFileName)):
        with open(cf.logPath+'/' +TEKFileName, 'wb') as fb:
            fb.write(tek)
        with open(cf.logPath+'/' +iFileName, 'w') as f:
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
    delOldFiles(cf.logPath)
    delOldFiles(cf.csvPath)
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
    isFolderExist(cf.logPath)
    TEKFileName = cf.TEKLogFile_prefix + datetime.datetime.utcnow().strftime('%m%d') + ".log"
    iFileName = cf.TEKLogFile_prefix + "i_" + datetime.datetime.utcnow().strftime('%m%d') + ".log"
    if os.path.exists(cf.logPath+'/' +TEKFileName) and os.path.exists(cf.logPath+'/' +iFileName):
        with open(cf.logPath+'/' +TEKFileName, 'rb') as fb:
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
                now = datetime.datetime.utcnow()
                if (now - fileTime).days > cf.keptDays:
                    os.remove(os.path.join(Path,x))
    return 0


def writeConfig(MAC,rpi_hex,aem_hex):
    with open(cf.RPI_AEM_fileName,'w+') as fb:
        fb.write("export MAC=\""+MAC+"\"\n")
        fb.write("export RPI=\""+' '.join(a+b for a,b in zip(rpi_hex[::2], rpi_hex[1::2]))+"\"\n")
        fb.write("export AEM=\""+' '.join(a+b for a,b in zip(aem_hex[::2], aem_hex[1::2]))+"\"")
    return True
