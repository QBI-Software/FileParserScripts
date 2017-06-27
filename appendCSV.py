# -*- coding: utf-8 -*-
"""
Utility script: appendCSV
Requirements: Python v3.4+ (or 2.7 is OK)
             pandas library
Description: 
    Reads a directory appends all csv files together (assumes same headers)
    run from console/terminal with (example):
    >python appendCSV.py --filedir "data" --output "output.csv"

Created on Tue Jun 27 2017

@author: Liz Cooper-Williams, QBI
"""

import argparse
import glob
from os import listdir, R_OK, path, mkdir, access
from os.path import isdir, join, basename, splitext

import pandas
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Append CSV Files',
                                     description='''\
            Reads a directory and extracts sheet into an output file

             ''')
    parser.add_argument('--filedir', action='store', help='Directory containing files', default=".")
    parser.add_argument('--output', action='store', help='Output file name with full path', default="Summaryoutput.csv")

    args = parser.parse_args()

    inputdir = args.filedir
    outputfile = args.output
    ctr = 0
    print("Input:", inputdir)
    if access(inputdir, R_OK):
        seriespattern = '*.csv'
        summarydata = pandas.DataFrame()
        try:
            files = glob.glob(join(inputdir, seriespattern))
            print("Files:", len(files))
            for f2 in files:
                print(f2)
                data = pandas.read_csv(f2)
                if (not data.empty):
                    summarydata = summarydata.append(data)
                    ctr += 1
            summarydata.to_csv(outputfile)
            print("Completed: ",ctr, "files extracted to: ", outputfile)
        except:
            raise OSError
        
    else:
        print("Cannot access directory: ", inputdir)
