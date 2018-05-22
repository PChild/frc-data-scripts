import pandas as pd
import tbapy
import geocoder

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

YEAR = 2018

f = open("iriLocations" + str(YEAR) + ".csv", 'w', encoding='utf-8')

props = ['team_number', 'nickname', 'city', 'state_prov', 'country', 'postal_code', 'lat', 'lng']

for prop in props:
    f.write(prop + ", ")
f.write("\n")

for team in pd.read_csv('iriAccepted.csv')['teams']:    
    print("Fetching data for " + str(team))
    teamData = tba.team(int(team), False)

    print("Geolocating...")
    teamData['lat'], teamData['lng'] = geocoder.osm(teamData['city'] + ", " + teamData['state_prov']).latlng
    
    for prop in props:
        f.write(str(teamData[prop]) + ", ")
    f.write("\n")
f.close()