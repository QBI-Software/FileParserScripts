# -*- coding: utf-8 -*-
"""
Utility script: parseExcel
Reads a directory and extracts sheet into an output file
run from console/terminal with (example):
>python parseExcel.py --filedir "data" --output "output.csv" --sheet "Sheetname_to_extract"

Created on Thu Mar 2 2017

@author: Liz Cooper-Williams, QBI
"""

import argparse
import glob
import re
import shutil
from os import listdir, R_OK, path, mkdir, access
from os.path import isdir, join, basename, splitext

import pandas

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Parse Excel Files',
                                     description='''\
            Reads a directory and extracts sheet into an output file

             ''')
    parser.add_argument('--filedir', action='store', help='Directory containing files', default=".")
    parser.add_argument('--output', action='store', help='Output file name with full path', default="..\\output.xlsx")
    parser.add_argument('--sheet', action='store', help='Sheet name to extract (default is "Each Tree-Dendrite")',
                        default="Each Tree-Dendrite")
    args = parser.parse_args()

    inputdir = args.filedir
    outputfile = args.output
    sheet = args.sheet
    print("Input:", inputdir)
    if access(inputdir, R_OK):
        seriespattern = '*.xls*'
        writer = pandas.ExcelWriter(outputfile, engine='xlsxwriter')
        try:
            files = glob.glob(join(inputdir, seriespattern))
            print("Files:", len(files))
            for f2 in files:
                print(f2)
                (fsheet, _) = splitext(basename(f2))
                data = pandas.read_excel(f2, sheet)
                if (not data.empty):
                    data.to_excel(writer, sheet_name=fsheet)

        except ValueError as e:
            print("Sheet not found: ", e)

        except:
            raise OSError
        print("Files extracted to: ", outputfile)
        writer.save()
        writer.close()
    else:
        print("Cannot access directory: ", inputdir)
