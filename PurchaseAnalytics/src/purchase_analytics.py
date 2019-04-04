# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 05:06:44 2019

@author: 60yu
"""

import numpy as np
import pandas as pd

#import dataset
priorDf = pd.read_csv('C:/Users/666/Desktop/order_products__prior.csv',sep=',', encoding='latin-1', error_bad_lines=False)
trainDf = pd.read_csv('C:/Users/666/Desktop/order_products__train.csv',sep=',', encoding='latin-1', error_bad_lines=False)
product = pd.read_csv('C:/Users/666/Desktop/products.csv',sep=',', encoding='latin-1', error_bad_lines=False)
department = pd.read_csv('C:/Users/666/Desktop/departments.csv',sep=',', encoding='latin-1', error_bad_lines=False)

# concatenate priorDf and Train Df in the same order_products dataframe.
order_products_all = pd.concat([trainDf, priorDf], axis=0)
merged = product.merge(order_products_all,on='product_id',how='inner')
#merged = department.merge(merged,on='department_id',how='inner')

#checking missing data
total = order_products_all.isnull().sum().sort_values(ascending=False)
percent = (order_products_all.isnull().sum()/order_products_all.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total Missing', 'Percent'])
missing_data


#number_of_orders. How many times was a product requested from this department? 
#(If the same product was ordered multiple times, we count it as multiple requests)
##per dept products ordered
group1 = merged.groupby(['department_id','product_id'],as_index=False)['reordered'].count()
overall=group1
group2=merged[merged['reordered'] == 0]
##number of products ordered for the first time
group3 = group2.groupby(['department_id','product_id'],as_index=False)['reordered'].count()
first_time=group3

overall.columns=['deptartment_id','product_id','number_of_orders']
first_time.columns=['deptartment_id','product_id','number_of_first_orders']
final_df = overall.merge(first_time,on='product_id',how='inner')
del final_df['deptartment_id_y']
del final_df['product_id']
df = final_df.groupby(['deptartment_id_x'],as_index=False).sum()
df.columns=['department_id','number_of_orders','number_of_first_orders']
df['percentage']=df['number_of_first_orders']/df['number_of_orders']
df['percentage']=df['percentage'].round(2)


df.to_csv('report.csv',sep='\t',encoding='utf-8')

