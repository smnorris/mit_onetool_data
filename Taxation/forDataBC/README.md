# Local Government Taxes

## Taxes_DevelopmentCostCharges_CD.csv

### Description
Representative and sample Development Cost Charges for BC Municipalities.

### Source
Ministry of Community, Sport and Cultural Development
http://www.cscd.gov.bc.ca/lgd/finance/development_cost_charges.htm
http://www.cscd.gov.bc.ca/lgd/library/2012_Local_Government_DCC_Rates.xls

### Caveats etc
The information in this file has not been audited or otherwise reviewed.  We cannot guarantee the accuracy or completeness of the information.  For more detailed information, or to confirm information, please contact the specific local government. 

### Preparation notes
- download spreadsheet from source
- add CENSUS_DIVISION_ID field from 2011 Census data, link via CD Name
- remove source 'Name' field 
- rename source fields, standardizing and prefixing with 'DCC'
- remove non-regional districts
- where a range of values were provided, calculated the average
- split categories into RATE vs COST columns as data are provided as both % rates and as dollar amounts


## Taxes_DevelopmentCostCharges_CSD.csv

### Description
Representative Development Cost Charges for BC Municipalities.

### Source
Ministry of Community, Sport and Cultural Development
http://www.cscd.gov.bc.ca/lgd/finance/development_cost_charges.htm
http://www.cscd.gov.bc.ca/lgd/library/2012_Local_Government_DCC_Rates.xls

### Caveats etc
The information in this file has not been audited or otherwise reviewed.  We cannot guarantee the accuracy or completeness of the information.  For more detailed information, or to confirm information, please contact the specific local government. 

### Preparation notes
- download spreadsheet from source
- add CENSUS_SUBDIVISION_ID field from 2011 Census data, link via CSD Name
- remove source 'Name' field 
- rename source fields, standardizing and prefixing with 'DCC'
- remove regional districts


## Taxes_Property_Municipal.csv

### Description
Property tax rates for BC Municipalities, 2014.

### Source
Ministry of Community, Sport and Cultural Development
http://www.cscd.gov.bc.ca/lgd/infra/statistics_index.htm
http://www.cscd.gov.bc.ca/lgd/infra/library/Schedule702_2014.xls

### Caveats etc
The quality of information contained in the schedules depends on the inputs of local governments.  

Note on School Tax Rates:  
The Province currently has two tax credit programs: the Provincial Industrial Property Tax Credit which gives a 60% school tax reduction to Class  4 (Major Industry), and the Provincial Farm Land Tax Credit which gives a 50% school tax reduction to Class 9 (Farm) properties.  The Ministry of Community, Sport and Cultural Development does not take these credits into account when reporting property tax rates.

### Preparation notes
- download spreadsheet from source
- add CENSUS_SUBDIVISION_ID field from 2011 Census data, link via CSD Name
- remove source Municipality and Type fields
- rename source tax rate fields, standardizing and prefixing with 'RATE'