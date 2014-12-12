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
import pandas as pd
from sqlalchemy import create_engine
from collections import OrderedDict

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

def compare(df1, df2):
    # compare column names

    c1= set([c for c in df1.columns])
    c2= set([c for c in df2.columns])
    print len(c1)
    print len(c2)
    if c1 == c2:
        print 'All column names match'
    else:
        print 'Columns in 1 that are not in 2: '+str(c1 - c2)
        print 'Columns in 2 that are not in 1: '+str(c2 - c1)
    # compare types
    types1 = [t for t in df1.dtypes]
    types2 = [t for t in df2.dtypes]
    if types1 == types2:
        print 'Data types match'
    else:
        print 'Data types do not exactly match'
        print types1
        print '--------'
        print types2
    # compare length of data
    if len(df1) == len(df2):
        print 'Number of rows match'
    else:
        print "n_rows1, n_rows2"+str((len(df1), len(df2)))
    # compare data values
    df1.sort(axis=0) == df2.sort(axis=0)
    ne = (df1 != df2).any(1)
    ne_stacked = (df1 != df2).stack()
    changed = ne_stacked[ne_stacked]
    if len(changed) == 0:
        print 'Values match'
    else:
        print 'Values do not match'
        changed.index.names = ['id', 'col']
        print changed


@cli.command()
@click.argument("usr", default="postgres")
@click.argument("pwd", default="postgres")
def test(usr, pwd):
    """
    Use pandas to quickly compare data in TEST to delivered csv
    """
    # get data to test
    forTesting = [row for row in dissdata.filelist if row["status"] == "TEST"]
    TEST = r"postgresql+psycopg2://{usr}:{pwd}@localhost:5432/postgis".format(usr=usr,
                                                                               pwd=pwd)
    schema = "idwtest1"
    for row in forTesting:

        #srcFile = os.path.join(STAGING_AREA, row["datafile"])
        srcFile = os.path.join(dissdata.path, "data", row["folder"], row["datafile"])
        print srcFile
        if "_cd_bc.csv" in srcFile:
            pk = "census_division_id"
        else:
            pk = "census_subdivision_id"
        # read source data
        df1 = pd.read_csv(srcFile, index_col=[0,1])
        print df1.columns
        # create a quick test db for trying this out

        #table = os.path.splitext(srcFile)[0]
        #df1.to_sql(table, engine)

        # read test data
        engine = create_engine(TEST)
        destTable = row["bcgw_table"]
        dftmp = pd.read_sql_table(destTable, engine, schema=schema)
        # alter indexes
        #print dftmp

        df2 = dftmp.set_index([u'census_year',pk])
        df2 = pd.DataFrame(df2)
        df2 = df2.drop('ogc_fid', 1)

        #print df2["q"]
        compare(df1, df2)

@cli.command()
@click.argument("infile", type=click.Path(exists=True))
def column_lengths(infile):
    """
    quickly report on max length of values in datafile
    """

    data = read_datafile(infile)
    path, f = os.path.split(infile)
    metafile = os.path.join(path, f.replace(".csv", "_METADATA.csv"))
    meta = read_datafile(metafile)
    typeDict = OrderedDict()

    for c in meta:
        if c["field"]:
            column = c["field"]
            if c["type"] == 'string':
                typeDict[column] = ("Varchar2", str(max(set([len(row[column]) for row in data]))))
            elif c["type"] == 'integer':
                typeDict[column] = ("Number", str(max(set([len(row[column]) for row in data]))))
            elif c["type"] == 'float':
                precision = str(max(set([len(row[column].split(".")[0]) for row in data])))
                l = []
                for row in data:
                    if "." in row[column]:
                        l.append(len(row[column].split(".")[1]))
                    else:
                        l.append(0)
                scale = max(l)
                if scale == 0:
                    typeDict[column] = ("Number", precision)
                else:
                    typeDict[column] = ("Number", precision+","+str(scale))
    data = []
    for metarow in meta:
        data.append({"field": metarow["field"],
                     "type": typeDict[metarow["field"]][0],
                     "length": typeDict[metarow["field"]][1],
                     "description": metarow["description"]})
    write_csv(sys.stdout, ["field", "type","length", "description"], data)
