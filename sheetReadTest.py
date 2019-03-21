import pandas
import requests
from io import StringIO 
import gen

tba = gen.setup()

#General settings for running waiver stuff
year = 2019
teamKey = 'CHS'
maxDraftRounds = 12

#Document and sheet specific url stuff, change for next year
bookID = '1-2Flli3g1d_r2sEkr0DjLnyXGgyn3LwC3uSh5uVThTc'
sheetID = '963745347'

#General g sheets url stuff.
baseURL = 'https://docs.google.com/spreadsheets/d/'
exportPart = '/export?format=csv&gid='

#Get sheet from internet and read it in
req = requests.get(baseURL + bookID + exportPart + sheetID)
decodedData = StringIO(req.content.decode('utf-8'))
dataDf = pandas.read_csv(decodedData,index_col=0)


#Cleans up the sheet some so its less bad to work with.
#Standardizes column names, resets tier being the index, drops crap columns,
#removes null rows
renameDict = {'index': 'Tier', 'event code': 'Code'}
for val in range(0, maxDraftRounds + 1):
    if val > 3:
        renameDict['[Round ' + str(val) + ']'] = 'Rnd ' + str(val)
    else:
        renameDict['Round ' + str(val)] = 'Rnd ' + str(val)
        
dataDf = dataDf.reset_index().rename(columns=renameDict).iloc[1:]
trashCols = ['Livescorer data generator DO NOT EDIT', 'Unnamed: 3', 'Unnamed: 4',]
dataDf = dataDf.drop(trashCols, axis=1)
dataDf = dataDf[pandas.notnull(dataDf['Tier'])]

#Build list of drafts we did
draftsList = dataDf['Code'].unique().tolist()
#draftsList = ['2019ksla']

#Iterate over all the events we drafted
for draftCode in draftsList: 
    
    #Handle regional events
    if str(year) in draftCode:
        eventTeams = [team[3:] for team in tba.event_teams(draftCode, False, True)]
        
        #Only care about teams taken in our tier.
        slffTeamRows = dataDf[dataDf['Code'] == draftCode]
        ourTier = slffTeamRows[slffTeamRows['Player'] == teamKey]['Tier'].iloc[0]
        tierTeamRows = slffTeamRows[slffTeamRows['Tier'] == ourTier]
        
        for idx, draftResult in tierTeamRows.iterrows():
            for draftRound in range(0, maxDraftRounds):
                roundStr = 'Rnd ' + str(draftRound + 1)
                teamVal = draftResult[roundStr]
                
                if not pandas.isnull(teamVal):
                    try:
                        eventTeams.remove(teamVal)
                    except:
                        print(draftResult['Player'], 'has MIA:', teamVal, '@', draftResult['Event'], '(' + draftCode + ')')
        
        #Now that we've removed all the drafted teams, lets collect data our teams picks and available picks
        for team in eventTeams:
                
        
            