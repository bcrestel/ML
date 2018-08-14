# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:39:58 2017

@author: mdesantis
"""
import pyodbc
import pandas as pd
import pandas.io.sql as pd_sql
cnn = pyodbc.connect(r'Driver={SQL Server};Server=ASTDC-SQL33P;Database=GlobalStockData;Trusted_Connection=yes;')

#df = pd_sql.read_sql("select Month, EoM_Ret from dbo.USStockData where Month>=201501", cnn)

sql_str = """
select Month, Month - 100*floor(Month/100) as nMonth, floor(Month/100) as nYear, 
Moody_Year, Permco, EoM_Ret as Ret, Exchange, EoM_Tcap, BoM_Tcap, BEME, Profitability,dTA 
from dbo.USStockData
where Share_Code in (10,11)
order by Month
"""


df = pd_sql.read_sql(sql_str, cnn)

df.to_csv('USStockData.csv')

#with open(r"SQLQuery1.sql") as f:
#    sql_str = f.read()
#df = pd_sql.read_sql(sql_str, cnn)


path = 'data/'
df = pd.read_csv(path+'USStockData.csv')


