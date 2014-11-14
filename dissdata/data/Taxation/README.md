# MunicipalPropertyTaxRates.csv

## Description
Property tax rates for BC Municipalities, 2014.

Municipal tax rate bylaws are required to be adopted before May 15th of each year. Tax rate files and tax burden files are available in July of that same year.

## Source
Ministry of Community, Sport and Cultural Development
http://www.cscd.gov.bc.ca/lgd/infra/statistics_index.htm  
http://www.cscd.gov.bc.ca/lgd/infra/library/Schedule702_2014.xls  

## Caveats etc
The quality of information contained in the schedules depends on the inputs of local governments.  

Note on School Tax Rates:  
The Province currently has two tax credit programs: the Provincial Industrial Property Tax Credit which gives a 60% school tax reduction to Class  4 (Major Industry), and the Provincial Farm Land Tax Credit which gives a 50% school tax reduction to Class 9 (Farm) properties.  The Ministry of Community, Sport and Cultural Development does not take these credits into account when reporting property tax rates.

## Preparation notes
- download spreadsheet from source
- add CENSUS_SUBDIVISION_ID field from 2011 Census data, link via CSD Name
- remove source Municipality and Type fields
- rename source tax rate fields, standardizing and prefixing with 'RATE'


# SalesAndIncomeTax.csv

## Description
Sales and Income tax descriptions and rates, these are the same throughout BC.

## Source
Sources are noted within the file.  
Data are generally taken from BC Ministry of Finance and Revenue Canada web sites.

## Caveats etc
For detailed tax information contact 
Canada Revenue Agency - http://www.cra-arc.gc.ca/menu-e.html  
Ministry of Finance - http://www2.gov.bc.ca/gov/theme.page?id=4DA4C0F9EA4A8A26605350E5097DEADD


# SalesTax_ItemsSubjectTo.csv

## Description
A list of IEDC noted items and the tax rates they are subject to. These are the same throughout BC.

## Source
Data were entered manually and taken from Canada Revenue Agency, BC Ministry of Finance web sites.   
Additional PST and ICE tax info based on an enquiry to CTBTaxQuestions@gov.bc.ca

## Caveats etc
For detailed tax information contact 
Canada Revenue Agency - http://www.cra-arc.gc.ca/menu-e.html  
Ministry of Finance - http://www2.gov.bc.ca/gov/theme.page?id=4DA4C0F9EA4A8A26605350E5097DEADD  