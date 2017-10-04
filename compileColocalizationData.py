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


def extractFilename(row, colname):
    """
    Extracts filename from pathname or just filename
    eg file:///Z:/_user%20folder/sam%20vdw/todo/counting/Brain09/AVD%20M09%20S02%7EB_001left.tif
    :param row:
    :param colname: column name containing filename
    :return:
    """
    p = row[colname]
    #print('Filename: ', p)
    if isabs(p):
        fname = basename(p)
        fname = fname.replace('%20', ' ') #replace any spaces
    else:
        fname = p
    return fname


def main(inputdir, outputfile, colname):
    """
    Main process - loops through files in inputdir, creates new column for Filename, appends to outputfile
    :param inputdir:
    :param outputfile:
    :param colname:
    :return:
    """

    if access(inputdir, R_OK):
        ctr = 0
        seriespattern = '*_Image.csv'
        summarydata = pandas.DataFrame()
        try:
            files = glob.glob(join(inputdir, seriespattern))
            print("Files:", len(files))

            cols = ['Brain', 'Filename', 'Count_ColocalizedPARV_DAPI_Objects', 'Count_ColocalizedGAD_DAPI_Objects',
                    'Count_ColocalizedGAD_and_PARVObjects']
            outputdir = dirname(outputfile)
            if inputdir == outputdir:
                #add subdir for output files
                try:
                    mkdir(join(outputdir, 'sorted'))
                    outputdir = join(outputdir, 'sorted')
                except:
                    pass

            for f2 in files:
                print(f2)                # eg Brain09_Image.csv
                data = pandas.read_csv(f2)

                if (not data.empty):
                    if 'Filename' not in data.columns and 'Brain' not in data.columns:
                        # Create filename column as first column
                        origcols = data.columns.tolist()
                        data['Filename'] = data.apply(lambda x: extractFilename(x, colname), axis=1)
                        # Add Brain num column
                        brain = basename(f2).split('_')[0]
                        data['Brain'] = data.apply(lambda x: brain, axis=1)
                        #Add new columns to original data
                        cols1 = ['Brain','Filename'] + origcols
                        data1 = data
                        data1 = data1.reindex_axis(cols1, axis=1)
                        copyf = join(outputdir, basename(f2))
                        data1.to_csv(copyf, index=False)  # save copy with extra columns
                        data = data.reindex_axis(cols, axis=1)


                    # Save to compiledfile
                    if summarydata.empty or len(data.columns) == len(summarydata.columns):
                        summarydata = summarydata.append(data)
                        ctr += 1
                    else:
                        msg = "Error: Unable to append data to summary as different number of headers: %s" % f2
                        print(msg)
                        raise Exception(msg)

            try:
                #Filter data on these columns only
                #cols = ['Brain', 'Filename', 'Count_ColocalizedPARV_DAPI_Objects', 'Count_ColocalizedGAD_DAPI_Objects',
                #        'Count_ColocalizedGAD_and_PARVObjects']
                summarydata = summarydata.reindex_axis(cols, axis=1)

                #Sort via ending to tabs if Excel or separate files if CSV
                endings = ['left','right','leftil','rightil']
                if splitext(outputfile)[1] == '.csv':
                    summarydata.to_csv(outputfile, index=False) #all data
                    for ending in endings:
                        subfile = outputfile.replace('.csv','_' + ending + '.csv')
                        sdata = summarydata[summarydata.Filename.str.endswith(ending + '.tif')]
                        sdata.to_csv(subfile, index=False)
                        print("Data for %s : %s" % (ending, subfile))

                else:
                    writer = pandas.ExcelWriter(outputfile, engine='xlsxwriter')
                    summarydata.to_excel(writer, index=False,sheet_name='All')
                    for ending in endings:
                        sdata = summarydata[summarydata.Filename.str.endswith(ending + '.tif')]
                        sdata.to_excel(writer, index=False,sheet_name=ending)
                    writer.close()
                print("Completed: ", ctr, "files compiled to: ", outputfile)

            except Exception as e:
                print(e)
        except:
            raise IOError

    else:
        raise IOError("Cannot access directory: %s" % inputdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Compile Image CSV Files',
                                     description='''\
            Reads a directory, moves Filename column to beginning and extracts data into an output file.  Output files will be copied to sorted directory.
             ''')
    parser.add_argument('--filedir', action='store', help='Directory containing files', default=".")
    parser.add_argument('--output', action='store', help='Output file name with full path', default="SummaryImageData.xls")
    parser.add_argument('--column', action='store', help='Column name', default="FileName_Dapi")

    args = parser.parse_args()
    print("*" * 80, "\nRunning Compile CSV\n", "*" * 80)
    print("\nInput: \t", args.filedir, "\nOutput: \t", args.output, "\nColumn: \t", args.column, "\n")
    main(args.filedir, args.output, args.column)
