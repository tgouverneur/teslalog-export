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
    parser.add_argument('-f', '--file', dest='fname', required=False, help='Filename to be used to display data')
    parser.add_argument('-t', '--trips', dest='trips', action='store_true', help='Shows trips')
    parser.add_argument('-c', '--charges', dest='charges', action='store_true', help='Shows charging sessions')
    args = parser.parse_args()

    if args.fname and not os.path.exists(args.fname):
        error('Specified file does not exists.')

    if not args.fname:
        error('No source file specified')

    tl = None

    print('[-] Loading TeslaLog saved data...')
    tl = Teslalog.loads(args.fname)

    print('[-] Listing cars & other data...')
    for car in tl.cars:
        print('\tc> ' + str(car) + ' [' + str(len(car.trips)) + ' trips][' + str(len(car.charges)) + ' charging sessions]')
        if args.trips:
            for trip in car.trips:
                print('\t\ttrip> ' + str(trip))
        if args.charges:
            for charge in car.charges:
                print('\t\tcharge> ' + str(charge))


if __name__ == "__main__":
    main()
