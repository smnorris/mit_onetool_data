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

# For some reason piping result bails
# the internet tells me to fix it like this:
# http://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
# note that this is also referred to in csvkit itself
# https://github.com/onyxfish/csvkit/blob/master/csvkit/cli.py
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
    outFields = ["folder", "data_csv", "metadata_csv", "field", "type", "description"]
    csvfiles = find_files("*_METADATA.csv", "dissdata/data")
    csvdata = read_metafiles(csvfiles)
    writer = CSVKitDictWriter(sys.stdout, outFields)
    writer.writeheader()
    for row in csvdata:
        writer.writerow(row)

@cli.command()
def build():
    """
    Build output data structure for publication
    """
    print "todo"
    # process data...
