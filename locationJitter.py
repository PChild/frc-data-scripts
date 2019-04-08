import random
import pandas as pd

xlsx = pd.ExcelFile('Jitter Data.xlsx')
teamData  = pd.read_excel(xlsx, 'Base Team Data')
jitterData = teamData.copy()

jitter = 0.03

locationData = []

for index, row in jitterData.iterrows():
    teamLocation = {'Lat': row['Lat'], 'Lng': row['Lng']}
    jittered = ""
    if teamLocation in locationData:
        teamLocation['Lat'] += random.uniform(-1,1) * jitter 
        teamLocation['Lng'] += random.uniform(-1,1) * jitter
        jittered = "YES"
    locationData.append(teamLocation)
    jitterData.set_value(index, 'Jitter Lat', teamLocation['Lat'])
    jitterData.set_value(index, 'Jitter Lng', teamLocation['Lng'])
    jitterData.set_value(index, 'Jittered', jittered)

writer = pd.ExcelWriter('Jitter Data.xlsx', engine='xlsxwriter')
teamData.to_excel(writer, index=False, sheet_name='Base Team Data')
jitterData.to_excel(writer, index=False, sheet_name='Jitter Data')
writer.save()