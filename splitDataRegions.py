# -*- coding: utf-8 -*-
"""
Utility script: compileColocalizationData
 - for Sam
Requirements: Python v3.4+ (or 2.7 is OK)
             pandas library
Description: 
    Reads a directory appends all csv files together (assumes same headers)
    run from console/terminal with (example):
    >python compileColocalizationData.py --filedir "data" --output "output.csv" --column "

Created on Sep 27 2017

@author: Liz Cooper-Williams, QBI
"""

import argparse
import glob
from os import R_OK, access, mkdir
from os.path import join, basename, isabs, splitext, dirname

import pandas

def main(inputfile, outputfile, sheet, dropcols=False):
    """
    Main process - loops through files in inputdir, creates new column for Filename, appends to outputfile
    :param inputdir:
    :param outputfile:
    :param colname:
    :return:
    """

    if access(inputfile, R_OK):
        #summarydata = pandas.DataFrame()
        try:
            if splitext(inputfile)[1] =='.csv':
                data = pandas.read_csv(inputfile)
            elif splitext(inputfile)[1] in ['.xlsx','.xls']:
                data = pandas.read_excel(inputfile, sheetname=sheet)
            if (not data.empty):
                summarydata = data.dropna(axis=0, how='all')
                if dropcols:
                    cols = [s for s in summarydata.columns.tolist() if not s.startswith('Unnamed')]
                    summarydata = summarydata.reindex_axis(cols, axis=1)
                #Sort via ending to tabs if Excel or separate files if CSV
                endings = ['left','right','leftil','rightil']
                if splitext(outputfile)[1] == '.csv':
                    #summarydata.to_csv(outputfile, index=False) #all data
                    for ending in endings:
                        subfile = outputfile.replace('.csv','_' + ending + '.csv')
                        sdata = summarydata[summarydata.Filename.str.endswith(ending + '.tif')]
                        sdata.to_csv(subfile, index=False)
                        print("Data for %s : %s" % (ending, subfile))

                else:
                    writer = pandas.ExcelWriter(outputfile, engine='xlsxwriter')
                    #summarydata.to_excel(writer, index=False,sheet_name='All')
                    for ending in endings:
                        sdata = summarydata[summarydata.Filename.str.endswith(ending + '.tif')]
                        sdata.to_excel(writer, index=False,sheet_name=ending)
                    writer.close()
                print("Completed: ", outputfile)

        except Exception as e:
                print(e)

    else:
        raise IOError("Cannot access file: %s" % inputfile)


if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='''\
            Reads a csv or excel file and extracts data into an output file.  Output files will be copied to sorted directory.
             ''')
    parser.add_argument('--input', action='store', help='Input file name with full path', default=r"My data.xlsx")
    parser.add_argument('--output', action='store', help='Output file name with full path', default="SummaryData2.xls")
    parser.add_argument('--sheet', action='store', help='Sheet name of data file', default="compiled")
    parser.add_argument('--dropblank', action='store_true', help='Sheet name of data file', default=True)

    args = parser.parse_args()
    print("*" * 80, "\nSplit Data by Regions\n", "*" * 80)
    print("\nInput: \t", args.input, "\nOutput: \t", args.output, "\nSheet: \t", args.sheet, "\n")
    main(args.input, args.output, args.sheet, args.dropblank)
