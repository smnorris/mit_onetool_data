# dissdata
import os
from csvkit import CSVKitDictReader

# load the data_categories_destinations file
path = os.path.split(__file__)[0]
filelistcsv = os.path.join(path,
                        r"data/data_categories_destinations.csv")
with open(filelistcsv, "r") as openfile:
    filelist = [row for row in CSVKitDictReader(openfile)]

bcgwfiles = [os.path.join(path,
                          "data",
                          row["folder"],
                          row["datafile"]) for row in filelist if row["destination"] == 'BCGW']
