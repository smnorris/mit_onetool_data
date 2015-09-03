"""
Functions for cleaning and grouping StatsCan data.

Ensure input files are loaded to db before processing (see PrepareCensusNHS.md)
Required input tables:
   - census_src (census data at csd level)
   - nhs_cd_src (nhs data at cd level)
   - nhs_csd_src (nhs data at csd level)
   - cen_census_subdivisions (spatial table, from GeoBC Census_2011.gdb)
   - cen_census_divisions (spatial, from GeoBC Census_2011.gdb)

Note that this script was created in March 2014, before the exact usage
of required data was defined. It functions as is but could definitely be
cleaned/improved.

"""

import os
import csv
from DBTools import pgdb


def get_datadef(inFile):
    # load definitions of each desired output column
    # Statscan (census, nhs) only!
    outList = []
    for row in csv.DictReader(open(inFile, 'rbU')):
        if row["SOURCE_TABLE"] in ["census", "nhs"]:
            outList.append(row)
    return outList


def get_unique(db, column, table):
    sql = "SELECT DISTINCT {column} FROM {table}".format(column=column,
                                                         table=table)
    return db.query(sql).fetchall()


def tweak_nhs_income(db, table):
    """
    NHS topics aren't distinct, there is no way to build a query that specifies
    total income vs after-tax income, the distinction is in a row/subheading

    Fix the topic values by looping through the data row by row.
    """
    # fetch all income records, ordered by line number
    sql = """SELECT line_number, characteristics
             FROM {table}
             WHERE topic = 'Income of households in 2010'
             ORDER BY line_number""".format(table=table)
    totalFlag = False
    for row in db.query(sql).fetchall():
        if row[1] == 'Household total income in 2010 of private households' or\
           row[1] == 'Household income in 2010 of private households':
            totalFlag = True
        if row[1] == 'After-tax income of households in 2010 of private households' or\
           row[1] == 'One-person private households':
            totalFlag = False
        if totalFlag is True:
            sql = """UPDATE {table}
                     SET topic = 'Income of households in 2010 (total)'
                     WHERE line_number = ?""".format(table=table)
            db.execute(sql, row[0])


def tweak_nhs_education(db, table):
    """
    NHS topics aren't distinct, there is no way to build a query that specifies
    15+ education vs 25-64 education

    Fix the topic values by looping through the data row by row.
    """
    # fetch all income records, ordered by line number
    sql = """SELECT line_number, characteristics
             FROM {table}
             WHERE topic = 'Education'
             ORDER BY line_number""".format(table=table)
    flag = False
    for row in db.query(sql).fetchall():
        if row[1] == 'Total population aged 25 to 64 years by highest certificate, diploma or degree':
            flag = True
        if row[1] == 'Total population aged 15 years and over by major field of study - Classification of Instructional Programs (CIP) 2011':
            flag = False
        if flag:
            sql = """UPDATE {table}
                     SET topic = 'Education (25-64)'
                     WHERE line_number = ?""".format(table=table)
            db.execute(sql, row[0])


def create_census_source(db):
    """
    slim down the source data, cleaning column names
    """
    print 'massaging source data'
    db.drop_table("mit.census_csd")
    sql = """CREATE TABLE mit.census_csd AS
            SELECT
              "Geo_Code" AS csduid,
              "Topic" AS topic,
              "Characteristics" AS characteristics,
              "Note" AS note,
              "Total" AS total,
              "Flag_Total" AS flag_total,
              "Male" AS male,
              "Flag_Male" AS flag_male,
              "Female" AS female,
              "Flag_Female" AS flag_female
            FROM
              mit.census_src
            WHERE
              "Topic" IN ('Age characteristics',
                          'Population and dwelling counts',
                          'Household and dwelling characteristics')
            ORDER BY csduid, "Topic","Characteristics"
            """
    db.execute(sql)
    db.execute("""ALTER TABLE mit.census_csd
                  ADD COLUMN census_id SERIAL PRIMARY KEY""")
    for column in ["csduid", "topic", "characteristics"]:
        sql = """CREATE INDEX
                 ON mit.census_csd ({column})
                 """.format(column=column)


def create_nhs_source(db):
    """
    due to poor data quality, process nhs at several different levels
    """
    for level in ["cd", "csd"]:
        db.drop_table("mit.nhs_"+level)
        sql = """CREATE TABLE mit.nhs_{level} AS
                SELECT
                  line_number,
                  "Geo_Code" AS {level}uid,
                  "GNR" as gnr,
                  "Topic" AS topic,
                  "Characteristic" AS characteristics,
                  "Note" AS note,
                  "Total" AS total,
                  "Flag_Total" AS flag_total,
                  "Male" AS male,
                  "Flag_Male" AS flag_male,
                  "Female" AS female,
                  "Flag_Female" AS flag_female
                FROM
                  mit.nhs_{level}_src
                WHERE
                  "Topic" IN ('Income of households in 2010',
                              'Education',
                              'Industry',
                              'Occupation',
                              'Median commuting duration',
                              'Labour force status')
                ORDER BY line_number
                """.format(level=level)
        db.execute(sql)
        db.execute("""ALTER TABLE mit.nhs_{level}
                      ADD COLUMN nhs_id SERIAL PRIMARY KEY
                      """.format(level=level))
        # index for speed
        for column in ["geoid", "topic", "characteristics"]:
            sql = """CREATE INDEX
                     ON mit.nhs_{level} ({column})
                  """.format(level=level,
                             column=column)
        # fix the NHS 'Topic' columns
        tweak_nhs_income(db, "mit.nhs_"+level)
        tweak_nhs_education(db, "mit.nhs_"+level)


def create_output_table(db, meta, level):
    print 'Creating output table '+level["output"]
    # create output table from spatial and nhs (to get gnr%)
    db.drop_table(level["output"])
    sql = """CREATE TABLE {outTable} AS
             (SELECT
                s.{key}::int as {level}uid,
                --s.geom,
                nhs.gnr
              FROM  {spatialSrc} s
              LEFT OUTER JOIN
                  (SELECT DISTINCT
                    {level}uid, gnr
                   FROM mit.nhs_{level}) nhs
              ON s.{key}::int = nhs.{level}uid)
          """.format(outTable=level["output"],
                     key=level["uid"],
                     level=level["code"],
                     spatialSrc=level["spatial"])
    db.execute(sql)
    # index
    db.execute("""CREATE UNIQUE INDEX
                  ON {outTable} ({level}uid)""".format(outTable=level["output"],
                                                       level=level["code"]))
    db.execute("""ALTER TABLE {outTable}
                  ADD PRIMARY KEY ({level}uid)""".format(outTable=level["output"],
                                                         level=level["code"]))
    # add new columns
    if level["code"] == "csd":
        sql = """ALTER TABLE {outTable}
                 ADD COLUMN census_flag text""".format(outTable=level["output"])
        db.execute(sql)
    sql = """ALTER TABLE {outTable}
             ADD COLUMN nhs_flag text""".format(outTable=level["output"])
    db.execute(sql)
    for column in meta:
        # but only add if we've defined the data type
        if column["DRAFT_COLUMN_TYPE"]:
            sql = """ALTER TABLE {outTable}
                     ADD COLUMN {colName} {colType}
                  """.format(outTable=level["output"],
                             colName=column["DRAFT_COLUMN_NAME"],
                             colType=column["DRAFT_COLUMN_TYPE"])
            db.execute(sql)


def populate_output_table(db, meta, level):
    """
    Insert the required data into the output table

    meta is a list of dicts directly from datalist.csv,
    one for each row.
    """
    # filter out census columns if processing at cd level
    #if level["code"] == 'cd':
    #    meta = [column for column in meta if column["SOURCE_TABLE"] == "nhs"]
    for column in meta:
        srcTable = "mit."+column["SOURCE_TABLE"]+"_"+level["code"]
        if column["DRAFT_COLUMN_TYPE"]:
            print "Loading to output table: "+column["DRAFT_COLUMN_NAME"]
            for uid in get_unique(db, level["code"]+"uid", srcTable):
                uid = uid[0]
                srcChar = column["SOURCE_CHARACTERISTICS"].split(";")
                srcChar = [s.strip() for s in srcChar]
                chrFilter = ["characteristics = ?" for c in srcChar]
                # generate the update statement from the list of
                # characteristics given in meta (datalist.csv)
                update = """UPDATE {outTable}
                     SET {col} =
                     (SELECT sum({srcColumn})
                     FROM {srcTable}
                     WHERE {level}uid = ?
                     AND topic = ?
                     AND  ({filter})
                     )
                     WHERE {level}uid = ?
                  """.format(outTable=level["output"],
                             col=column["DRAFT_COLUMN_NAME"],
                             level=level["code"],
                             srcColumn=column["SOURCE_COLUMN"],
                             srcTable=srcTable,
                             filter=" OR ".join(chrFilter))
                param = srcChar
                param.insert(0, uid)
                param.insert(1, column["SOURCE_TOPIC"])
                # before executing the update, note whether there is a flag
                # associated with the characteristic for this csd
                sql = """SELECT DISTINCT flag_total
                         FROM {srcTable}
                         WHERE {level}uid = ?
                         AND topic = ?
                         AND flag_total is not null
                         AND ({filter})
                      """.format(srcTable=srcTable,
                                 level=level["code"],
                                 filter=" OR ".join(chrFilter))
                flagResult = db.query(sql, param).fetchall()
                param.append(uid)
                # execute the update
                db.execute(update, param)
                # if there is a flag, note in output
                if flagResult:
                    if column["SOURCE_TABLE"] == "nhs":
                        sql = """UPDATE {outTable}
                             SET nhs_flag = 'Y'
                             WHERE {level}uid = ?
                          """.format(outTable=level["output"],
                                     level=level["code"])
                    if column["SOURCE_TABLE"] == "census":
                        sql = """UPDATE {outTable}
                             SET census_flag = 'Y'
                             WHERE {level}uid = ?
                          """.format(outTable=level["output"],
                                     level=level["code"])
                    db.execute(sql, (uid))


# initialize database
db = pgdb.Database()

# load metadata file listing all columns to process
metaFile = "DataDictionary.csv"
meta = get_datadef(metaFile)

# define inputs and outputs at each level of geography
csd = {"output": "mit.demographics_labour_csd",
       "spatial": "mit.cen_census_subdivisions",
       "uid": "census_subdivision_id",
       "code": "csd"}
cd = {"output": "mit.demographics_labour_cd",
      "spatial": "mit.cen_census_divisions",
      "uid": "census_division_id",
      "code": "cd"}
levels = [cd]

# create clean source tables from the data loaded to db from source csv
#create_census_source(db)
#create_nhs_source(db)

# create outputs
for level in levels:
    create_output_table(db, meta, level)
    populate_output_table(db, meta, level)

# populate null flag values as per data bc requirements
#db.execute("""UPDATE mit.demographics_labour_csd SET census_flag = 'N' WHERE census_flag IS NULL""")
#db.execute("""UPDATE mit.demographics_labour_csd SET nhs_flag = 'N' WHERE nhs_flag IS NULL""")
db.execute("""UPDATE mit.demographics_labour_cd SET nhs_flag = 'N' WHERE nhs_flag IS NULL""")
