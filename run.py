#!/usr/bin/python3

import sys
import argparse
import os.path
from teslalog import *

def error(msg):
    print('[!] ' + msg)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', required=True, help='Teslalog username')
    parser.add_argument('-p', '--password', dest='password', required=True, help='Teslalog Password')
    parser.add_argument('-f', '--file', dest='fname', required=False, help='Filename to be used for the CSV output')
    parser.add_argument('-i', '--input', dest='ifile', required=False, help='Filename to be used for the CSV input')
    parser.add_argument('-r', '--resume', dest='resume', action='store_true', help='Resume fetching data')
    parser.add_argument('-b', '--before', dest='before', required=False, help='Date before which we need to browse YYYY-MM-DD')
    parser.add_argument('-s', '--skip', dest='skip', required=False, help='Skip error encountered and try to fetch as much as possible anyway')
    args = parser.parse_args()

    if args.resume and not args.ifile:
        error('Resuming the download of data needs input filename specified')

    if not args.resume and args.ifile:
        error('Input file can be specified only with resume mode..')

    if args.fname and os.path.exists(args.fname):
        error('Specified output file already exists.')

    tl = None

    if args.resume:
        if not os.path.exists(args.ifile):
            error('Specified input file does not exists.')

        print('[-] Loading TeslaLog saved data...')
        tl = Teslalog.loads(args.ifile)
        tl.username = args.username
        tl.password = args.password
        print('[-] Logging into Teslalog...')
        tl.login()

    else:
        print('[-] Login to TeslaLog in progress..')
        tl = Teslalog(args.username, args.password)

    print('[-] Logged in..')
    print('[-] Listing available cars..')
    tl.car_list(args.resume)
    print('[-] Car list fetched: ' + str(len(tl.cars)) + ' cars found')
    for car in tl.cars:
        print('\t+ ' + str(car))
        try:
            tl.fetch_logs(car, debug=True, resume=args.resume, before=args.before, skip=args.skip)
        except Exception as e:
            print('\t!! {}'.format(e))

    if args.fname is not None:
        tl.dumps(args.fname)


if __name__ == "__main__":
    main()
