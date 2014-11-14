# dissdata

Data collection for MIT's DISS application

## Installation
```
$ pip install -e git+http://github.com/smnorris/dissdata.git#egg=dissdata
```

dissdata is tested only on Python 2.7.  

Python requirements are:
- [click](http://click.pocoo.org/3/)
- [csvkit](http://csvkit.readthedocs.org/en/latest/index.html)  

When installing with pip, pip should fetch these for you.



## Usage
Data is stored as .csv files in the `/dissdata/data` folder.
Browse the README files in each subfolder for information about the data files included, such as:
- title
- description
- caveats
- detailed preparation notes  

See the `_METADATA.csv` files that correspond to each data file for detailed descriptions of each column in the data file.

To re-generate the complete summary data dictionary `diss_datadict.csv` that compiles all the included `_METADATA.csv` files, use the command line tool and send the results to file:  
```
$ dissdata summarize > diss_datadict.csv
```

## TODO
If required, build output files tailored to MIT requirements:
```
$ dissdata build
```


