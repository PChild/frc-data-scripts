import os
import base64
import requests

year = 2018
user = 'CHILDREPT0401'
authKey = os.getenv('firstAPI')
plainToken = user + ':' + authKey
serverBase = 'https://frc-api.firstinspires.org/v2.0/' + str(year) + '/'
authToken = base64.b64encode(plainToken.encode()).decode()
headers = {'Authorization': 'Basic ' + authToken,
           'Cache-Control': 'no-cache, max-age=10',
           'Pragma': 'no-cache'}

def getEventTeams(event):    
    rawTeams = requests.get(serverBase + 'teams?eventCode=' + event, headers=headers).json()['teams']
    return [team['teamNumber'] for team in rawTeams]

