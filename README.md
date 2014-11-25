# dissdata

Data collection for MIT's DISS application

## Installation
```
$ pip install -e git+http://github.com/smnorris/dissdata.git#egg=dissdata
```

This installs only to local folder, rather than the system python's site-packages.

This is problematic on GTS though - git isn't installed and dealing with packages installed by other users is problematic due to permissions.

install to a virtualenv instead:

```
pip install virtualenv
mkdir dissdata_env
virtualenv dissdata_env
dissdata_env/Scripts/activate
- manually download zipfile from github 
- unzip, rename dissdata-master to dissdata, move into dissdata_env
cd dissdata_env
cd dissdata
pip install -e .
```


## Requirements
dissdata is tested only on Python 2.7.  

Python requirements are:
- [click](http://click.pocoo.org/3/)
- [csvkit](http://csvkit.readthedocs.org/en/latest/index.html) 
- [pandas](http://pandas.pydata.org/)

When installing with pip, pip should fetch these for you.



## Usage
Browse the the `/dissdata/data` folder to see included data.  

README files in each subfolder for information about the data files included, such as:
- title
- description
- source
- caveats
- preparation notes  

Data files noted in the READMEs are all held as .csv.

A data dictionary for each data file is included in the corresponding `_METADATA.csv`, with type and description for each column included in the data file.  

`diss_datadict.csv` in the root folder is a complete data dictionary - it is simply a merge of all the `_METADATA.csv` files included in the package. If changes are made to individual metadata files, update the complete list with this command:  
```
$ dissdata summarize > diss_datadict.csv
```

## TODO
If required, build output files tailored to MIT requirements:
```
$ dissdata build
```


