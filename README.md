# Teslalog-export

This code is a WIP and is currently ugly-af, but it works :-)
NOTE: Right now, this tool can be used to fetch data from teslalog.com and can display it on screen from the JSON backup. Future work will include a CSV generator in TeslaFi format so it can be imported to Teslamate... stay tuned!

## Display saved data

The display.py tool can be used to read back any saved data from Teslalog.com:

```
usage: display.py [-h] [-f FNAME] [-t] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -f FNAME, --file FNAME
                        Filename to be used to display data
  -t, --trips           Shows trips
  -c, --charges         Shows charging sessions
```

Example:

```
[-] Loading TeslaLog saved data...
[-] Listing cars & other data...
	c> [XXX][VIN: XXXXXXXXXXXX][Name: XXXXXX]
		trip> [2020-04-23][XXXXXXX][Location name][44 data points]
		trip> [2020-04-21][XXXXXXX][Location 2 Name][60 data points]
		trip> [2020-04-21][XXXXXXX][Location name][3 data points]
		trip> [2020-04-21][XXXXXXX][Location 3 Name][55 data points]
		trip> [2020-04-20][XXXXXXX][Location 4 name][45 data points]
		trip> [2020-04-20][XXXXXXX][Location name][13 data points]
		trip> [2020-04-17][XXXXXXX][Location 4 name][59 data points]
```

## Fetch data from teslalog.com

To fetch data, you need to provide your teslalog.com username and password, the download will start and save data to the mentionned file if you specify one. If there's an issue with teslalog.com while fetching data (which, trust me, can happen ;-)), the JSON file will get saved with the progress. You can resume the download using the resume flag.

```
usage: run.py [-h] -u USERNAME -p PASSWORD [-f FNAME] [-i IFILE] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Teslalog username
  -p PASSWORD, --password PASSWORD
                        Teslalog Password
  -f FNAME, --file FNAME
                        Filename to be used for the CSV output
  -i IFILE, --input IFILE
                        Filename to be used for the CSV input
  -r, --resume          Resume fetching data
```


