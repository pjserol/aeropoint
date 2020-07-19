# Aeropoint

Command line tool that given a base station ID, start time and end time downloads the day blocks from a given time and merges them into a single RINEX observation file.

One of these networks in the NOAA CORS network in the United States. RINEX observation data from each of their base stations is published in 1 hour blocks on their FTP server at 'ftp://www.ngs.noaa.gov/cors/rinex'. You can read more about the network here: 'http://geodesy.noaa.gov/CORS/'

## Requirements (installed)

- gunzip
- teqc 'https://www.unavco.org/software/data-processing/teqc/teqc.html'

## Python dependencies

- datetime
- os
- shutil
- subprocess
- sys

## Environment Variables

- GUNZIP_CMD
- TEQC_CMD  

export env GUNZIP_CMD="gunzip"  
export env TEQC_CMD="teqc"

## Test locally

- python -m unittest discover -s . -p '*_test.py'

## Run the app

- /usr/bin/python3 ./main.py nypb 2020-07-09T23:11:22Z 2020-07-14T01:33:44Z

## Improvements

- Download the file by 1 hour blocks when available instead of downloading only the files of the full day
- Handle error when file doesn't exist from the server, validation of the input format of the date
- Add files processed in a report file (success or not)
- Add better test coverage
