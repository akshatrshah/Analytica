import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

files=[file for file in os.listdir("./Sales_Data")]
all_months_data=pd.DataFrame()

for file in files:
    df=pd.read_csv("./Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])

all_months_data.to_csv("all_data.csv",index=False)
all_data=pd.read_csv("all_data.csv")

nan_df = all_data[all_data.isna().any(axis=1)]
print(nan_df.head())

all_data = all_data.dropna(how='all')
print(all_data.head())

all_data=all_data.dropna(how='all')
all_data=all_data[all_data['Order Date'].str[0:2]!='Or']
all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])
all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']

result=all_data.groupby('Month').sum()
months=range(1,13)
plt.bar(months,result['Sales'])
plt.xticks(months)
plt.ylabel('Sales in million USD ($)')
plt.xlabel('Month number')
plt.show()



def get_state(address):
    return address.split(",")[2].split(' ')[1]
all_data['City']=all_data['Purchase Address'].apply(lambda x:x.split(",")[1]+', '+get_state(x))
city=all_data.groupby('City').sum()
cities=[city for city, df in all_data.groupby('City')]
plt.bar(cities,city['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('City')
plt.xticks(rotation='vertical', size=8)
plt.show()




all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']=all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute
#print(all_data.head())
hours=[hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours,all_data.groupby(['Hour']).count())
plt.ylabel('Sales in USD ($)')
plt.xlabel('Hour')
plt.show()




df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()

count =Counter()

for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))
print(count.most_common(10))



product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

keys = [pair for pair, df in product_group]
plt.bar(keys, quantity_ordered)
plt.xticks(keys, rotation='vertical', size=8)
plt.show()






































# def get_city(address):
#     return address.split(",")[1].strip(" ")
#
# def get_state(address):
#     return address.split(",")[2].split(" ")[1]
#
# all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
# all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')
# months = range(1,13)
# print(months)
#
# plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
# plt.xticks(months)
# plt.ylabel('Sales in USD ($)')
# plt.xlabel('Month number')
# plt.show()
# all_data.groupby(['City']).sum()
# keys = [city for city, df in all_data.groupby(['City'])]
#
# plt.bar(keys,all_data.groupby(['City']).sum()['Sales'])
# plt.ylabel('Sales in USD ($)')
# plt.xlabel('Month number')
# plt.xticks(keys, rotation='vertical', size=8)
# plt.show()
# all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
# all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
# all_data['Count'] = 1
# keys = [pair for pair, df in all_data.groupby(['Hour'])]
#
# plt.plot(keys, all_data.groupby(['Hour']).count()['Count'])
# plt.xticks(keys)
# plt.grid()
# plt.show()


