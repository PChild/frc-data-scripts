import pandas as pd
import chardet

with open('2018VexData.csv', 'rb') as f:
    result = chardet.detect(f.read())

baseOld = pd.read_excel('2017VendorData.xlsx', 'VEX').drop_duplicates(subset='Part Number')
baseNew = pd.read_csv('2018VexData.csv', encoding=result['encoding']).drop_duplicates(subset='Part Number')

new = baseNew[baseNew['Part Number'].isin(baseOld['Part Number'])]
old = baseOld[baseOld['Part Number'].isin(baseNew['Part Number'])]



old = old.set_index('Part Number')
new = new.set_index('Part Number')

old['PriceVal'] = old['Price'].replace('[\$,]', '', regex=True).astype(float)
new['PriceVal'] = new['Price'].replace('[\$,]', '', regex=True).astype(float)

new['Old Price'] = old['Price']
new['Price Change'] = new['PriceVal'] - old['PriceVal']
new['% Change'] = round((new['Price Change'] / new['Old Price']) * 100)

changedPrices = new[new['Price Change'] != 0]
changedPrices = changedPrices[['Name', 'Old Price', 'Price', 'Price Change', '% Change']]
changedPrices.rename(columns={'Price': 'New Price'}, inplace=True)

changedPrices = changedPrices.sort_values('% Change', ascending=False)

changedPrices['Old Price'] = ['${:,.2f}'.format(x) for x in changedPrices['Old Price']]
changedPrices['Price Change'] = ['${:,.2f}'.format(x) for x in changedPrices['Price Change']]
changedPrices.index.name = 'Part Number'

changedPrices.to_csv('Vex Changed Prices.csv')