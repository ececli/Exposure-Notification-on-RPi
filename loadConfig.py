import configparser
import os

confFile = "CT_pyConfig.conf"

cp = configparser.ConfigParser()
cp.read(confFile)

RPI_AEM_fileName = cp.get("FILE_OP","RPI_AEM_fileName")
META_fileName = cp.get("FILE_OP","META_fileName")
TEKLogFile_prefix = cp.get("FILE_OP", "TEKLogFile_prefix")
csvFile_prefix = cp.get("FILE_OP", "csvFile_prefix")
keptDays = cp.getint("FILE_OP","keptDays")
logPath = os.getcwd() + cp.get("FILE_OP", "logPath")
csvPath = os.getcwd() + cp.get("FILE_OP", "csvPath")


FLAG = cp.get("SCAN", "FLAG")
CT_SERVICE_UUID = cp.get("SCAN", "CT_SERVICE_UUID")
NUM_DESC = cp.getint("SCAN", "NUM_DESC") # Number of descriptions in the message
# Scan window is uniformly random 
SCAN_WINDOW_MIN = cp.getfloat("SCAN_WINDOW", "SCAN_WINDOW_MIN")
SCAN_WINDOW_MAX = cp.getfloat("SCAN_WINDOW", "SCAN_WINDOW_MAX")

