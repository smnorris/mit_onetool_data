#!/usr/bin/env python

"""
dissdata command line interface for:
  - summarizing included data
  - building output data structures
"""

import click
import dissdata
import fnmatch
import os
import sys
from csvkit import CSVKitDictReader, CSVKitDictWriter
import shutil

STAGING_AREA = r"\\data.bcgov\data_staging_bcgw\socio_economic"

# For some reason piping result bails
# the internet tells me to fix it like this:
# http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
# note that this is also referred to in csvkit itself
# https://github.com/onyxfish/csvkit/blob/master/csvkit/cli.py
# but don't use on windows!
if not os.environ.get("OS", '').lower().startswith('windows'):
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE,SIG_DFL)

def find_files(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def read_metafiles(files):
    for f in files:
        path, metafile = os.path.split(f)
        datadict = {}
        datadict["folder"] = os.path.split(path)[1]
        datadict["datafile"] = metafile.split("_METADATA")[0]+".csv"
        with open(f, "r") as openfile:
            for row in CSVKitDictReader(openfile):
                rowlower = {k.lower():row[k] for k in row}
                yield dict(datadict.items() + rowlower.items())

def read_datafile(f):
    data = []
    with open(f, "r") as openfile:
        for row in CSVKitDictReader(openfile):
            data.append({k.lower():row[k] for k in row})
    return data

def write_csvdata(writer, data):
    writer.writeheader()
    for row in data:
        writer.writerow(row)

def write_csv(output, outFields, data):
    if output == sys.stdout:
        writer = CSVKitDictWriter(output, outFields)
        write_csvdata(writer, data)
    else:
        with open(output, "w") as openfile:
            writer = CSVKitDictWriter(openfile, outFields)
            write_csvdata(writer, data)

def get_header(f):
    with open(f, "r") as openfile:
        reader = CSVKitDictReader(openfile)
        header = [r.lower() for r in reader.fieldnames]
    return header

def write_insert(writer, data, newrow, line=None):
    writer.writeheader()
    for i, row in enumerate(data):
        if line and i == line:
            writer.writerow(newrow)
        writer.writerow(row)
    # if line number wasn't specified, just tag new row on at the end
    if not line:
        writer.writerow(newrow)

def insert_row(incsv, row, line, output=None):
    """
    insert provided row at specified line number
    (where line number of header=0)
    """
    # if no output specified, overwrite file
    if not output:
        output = incsv
    data = read_datafile(incsv)
    header = get_header(incsv)
    if output == sys.stdout:
        writer = CSVKitDictWriter(output, header)
        write_insert(writer, data, row, line)
    else:
        with open(output, "w") as openfile:
            writer = CSVKitDictWriter(openfile, header)
            write_insert(writer, data, row, line)


@click.group()
def cli():
    pass

@cli.command()
def summarize():
    """
    Quickly summarize all datasets in the repository's /data folder
     - scans all folders, reading _METADATA.csv files
     - dumps results to stdout, in a format suitable for writing to csv
    """
    outFields = ["folder", "datafile", "metadata_csv", "field", "type", "description"]
    csvfiles = find_files("*_METADATA.csv", dissdata.path)
    csvdata = read_metafiles(csvfiles)
    write_csv(sys.stdout, outFields, csvdata)


@cli.command()
def add_census_year():
    """
    Add CENSUS_YEAR field to all BCGW bound data.
    Set census_year to 2011.
    """
    # process each file
    for datafile in dissdata.bcgwfiles:
        print 'Adding census year to '+datafile
        # get existing header
        columns = get_header(datafile)
        if "census_year" not in columns:
            # pre-pend census year to existing header
            columns = ["census_year"]+columns
            # read the file
            data = read_datafile(datafile)
            for row in data:
                row[u"census_year"] = 2011
            # overwrite file
            write_csv(datafile, columns, data)
        # add to metadata
        fileName, fileExtension = os.path.splitext(datafile)
        metafile = fileName+"_METADATA"+fileExtension
        newline = {"field": "census_year",
                   "type": "number",
                   "description": "CENSUS YEAR is the census year that the data is collected. e.g., 2006, 2011."}
        insert_row(metafile, newline, 1)

@cli.command()
def deliver_bcgw():
    """
    Copy all BCGW bound datafiles to STAGING_AREA
    """
    print 'Delivering data to BCGW staging folder'
    for row in dissdata.filelist:
        srcFile = os.path.join(dissdata.path, "data", row["folder"], row["datafile"])
        if row["destination"] == 'BCGW' and row["status"] == "DLVR":
            print os.path.join(srcFile)
            shutil.copy(srcFile, os.path.join(STAGING_AREA, row["datafile"]))

@cli.command()
def remap_languages():
    """
    move language data around to match other census data
    ie, attributes in simple columns, single row for each geography
    """

