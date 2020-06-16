#!/usr/bin/python3

import sys
import argparse
from teslalog import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', required=True, help='Teslalog username')
    parser.add_argument('-p', '--password', dest='password', required=True, help='Teslalog Password')
    parser.add_argument('-f', '--file', dest='fname', required=False, help='Filename to be used for the CSV output')
    args = parser.parse_args()

    print('[-] Login to TeslaLog in progress..');
    tl = Teslalog(args.username, args.password)
    print('[-] Logged in..');
    print('[-] Listing available cars..');
    tl.car_list()
    print('[-] Car list fetched: ' + str(len(tl.cars)) + ' cars found')
    for car in tl.cars:
        print('\t+ ' + str(car))
        tl.fetch_logs(car, True)

    if args.fname is not None:
        tl.dumps(args.fname)


if __name__ == "__main__":
    main()
