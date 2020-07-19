import datetime
import os
import shutil
import subprocess
import sys
from ftplib import FTP
from subprocess import call

import dateutil.parser


def convertTime(input):
    return dateutil.parser.isoparse(input)


def getFilePath(baseStationID, hourBlock, t):
    return f'/cors/rinex/{t.year}/{t.timetuple().tm_yday:03}/{baseStationID}/{baseStationID}{t.timetuple().tm_yday:03}{hourBlock}.{abs(t.year) % 100}o.gz'


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Please specify the base station id, start time and end time.")
        sys.exit(0)

    teqcCmd = os.getenv("TEQC_CMD") 
    if not teqcCmd:
        teqcCmd = "teqc"
    
    gunzipCmd = os.getenv("GUNZIP_CMD") 
    if not gunzipCmd:
        gunzipCmd = "gunzip"
  
    baseStationID = sys.argv[1]
    startTimetStr = sys.argv[2]
    endTimeStr = sys.argv[3]

    print(f'Input:{baseStationID} {startTimetStr} {endTimeStr}')

    start = convertTime(startTimetStr)
    end = convertTime(endTimeStr)

    tmpPath = "./tmp/"

    try:
        os.mkdir(tmpPath, 0o755)
    except OSError:
        print("Creation of the directory %s failed" % tmpPath)
    else:
        print("Successfully created the directory %s" % tmpPath)

    count = 0
    elements = []
    while start < end:
        filePath = getFilePath(baseStationID, "0", start)
        print(f"start fetching file: {filePath}")

        fileName = f'./tmp/file{count}.gz'

        # retrive file from ftp server
        ftp = FTP('ftp.ngs.noaa.gov')
        ftp.login(user='anonymous', passwd='anonymous')
        
        fileRetrieved = open(fileName, 'wb')
        ftp.retrbinary('RETR ' + filePath, fileRetrieved.write, 1024)

        ftp.quit()
        fileRetrieved.close()

        # unzip file
        call([gunzipCmd, fileName])

        elements.append(os.path.splitext(fileName)[0])

        count += 1
        start = start + datetime.timedelta(days=1)

    el = ' '.join([str(v) for v in elements])

    os.system(f'{teqcCmd} {el} > nypb.obs')

    shutil.rmtree(tmpPath, ignore_errors=True, onerror=None)
