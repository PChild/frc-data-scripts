import gen
import pandas
import eventTypes
import awardTypes
from hallOfFame import hallOfFame
from rookieValues import rookieValues

tba = gen.setup()

#Base mCA values for awards
awardValues = {awardTypes.CHAIRMANS_FINALIST: 1500,
               awardTypes.CHAIRMANS: 1000,       
               awardTypes.ENGINEERING_INSPIRATION: 600,
               awardTypes.ENTREPRENEURSHIP: 400,
               awardTypes.IMAGERY: 300,
               awardTypes.GRACIOUS_PROFESSIONALISM: 250,
               awardTypes.CREATIVITY: 100,
               awardTypes.JUDGES: 200,
               awardTypes.DEANS_LIST: 200,
               awardTypes.SPIRIT: 200,
               awardTypes.WOODIE_FLOWERS: 200,
               awardTypes.ENGINEERING_EXCELLENCE: 100,
               awardTypes.INNOVATION_IN_CONTROL: 100,
               awardTypes.WINNER: 100,
               awardTypes.INDUSTRIAL_DEESIGN: 100,
               awardTypes.SAFETY: 100}

baseTeamCount = 50 #teams base size (smaller events worth less)
reversionFactor = 0.19 #reversion towards zero mCA

eloBaseLine = 1450 #Baseline for getting extra mCA
rookieEloBase = 1450 #Base Elo assigned to rookies or revived teams
eloScale = 0.5 #mCa per elo rating difference

yearToPredict = 2019 #Year that we're going to calc mCA data for
yearRange = 4 #How many years back to get data from

endYear = yearToPredict - 1 #Last played FRC year
startYear = endYear - yearRange
yearRange = range(startYear, yearToPredict)

#Get previous years Elo ratings, if not found just apply 1450 (this covers rookies, revived, etc)
def mapElo(teamKey, year):
    teamNum = int(teamKey[3:])
    if teamNum in teamElos.index:
        return teamElos[str(year)].loc[teamNum]
    else:
        return rookieEloBase

#Check if team is in HOF.
def teamInHOF(team):
    return any([team in hallOfFame[year] for year in hallOfFame])

def calcEventMCA(team, event):
    eventMCA = 0
    teamAwards = gen.readTeamCsv('frc'+ str(team), 'awards', int(event[:4]))
    
    #Don't bother doing calc if the team didn't win awards that year
    #This check is duplicated in calcYearMCA, but included here as well in case
    #function is run independently.
    if teamAwards is not None:
        eventFilter = teamAwards['Event'] == event
        currentAwards = teamAwards[eventFilter]
        
        #If the team didn't win any awards at this event don't calc.
        if not currentAwards.empty:
                eventValuation = len(gen.readEventCsv(event, 'teams')) / baseTeamCount
                
                for idx, award in currentAwards.iterrows():
                    if award['Type'] in awardValues:
                        #For CA Finalist or Honorable Mention treat it as 100 team event
                        if award['Type'] == awardTypes.CHAIRMANS_FINALIST or award['Type'] == awardTypes.CHAIRMANS_HONORABLE_MENTION:
                            eventValuation = 2
                        eventMCA += eventValuation * awardValues[award['Type']]
    return eventMCA

#Calculates a team's mCA for a given year.
def calcYearMCA(team, year):
    teamEvents = gen.readTeamCsv("frc" + str(team), 'events', year)
    yearMCA = 0
    
    #Check if team actually had events in the current year, if not then zero mCA
    if teamEvents is not None:
        isOfficial = teamEvents['Type'].between(eventTypes.REGIONAL, eventTypes.FOC, inclusive=True)
        officialEvents = teamEvents[isOfficial]
        
        #Make sure the team actually had official events before trying any calc
        if not officialEvents.empty:
            teamYearAwards = gen.readTeamCsv('frc'+ str(team), 'awards', year)
            
            #If the team didn't win any awards then don't bother calculating per event mCA
            if teamYearAwards is not None and not teamYearAwards.empty:
                for event in officialEvents['Event']:
                    yearMCA += calcEventMCA(team, event)
                    
    #Previous year Elo values above the baseline increase mCA rating
    if year == endYear:
        teamPrevElo = df.loc[team, str(year) + ' Elo']
        if teamPrevElo > eloBaseLine:
            yearMCA += eloScale * (teamPrevElo - eloBaseLine)
    return yearMCA

#Calculates a team's current mCA value
def calcTeamMCA(team):
    #0 mCA to start.
    #HoF teams excluded, 
    #Rookies get no points their first year.
    #Apply a reversion scaling based on how old points are- 0.89 ^ (# years ago)
    teamMCA = 0
    if not teamInHOF(team):
        for year in yearRange:            
            if team < rookieValues[year]:
                reversionBase = 1 - reversionFactor
                reversionPower = endYear - year
                reversion = reversionBase ** reversionPower
                
                teamMCA += calcYearMCA(team, year) * reversion
            
    return teamMCA
    
#This code iterates through to pull in team elo values or apply the default elo value
teamElos = pandas.read_csv('eloData.csv', index_col='Team')
df = pandas.read_csv(str(yearToPredict)+'TeamKeys.csv', names=['Team Key'])
df['Team'] = df['Team Key'].apply(lambda key: int(key[3:]))
df['#'] = df['Team']
df = df.set_index('#')
for year in yearRange:
    df[str(year) + ' Elo'] = df['Team Key'].apply(mapElo, args=(year,))


def calcAllMCA():
    #Calculate mCA values for each team for the current year.
    df['mCA'] = df['Team'].apply(calcTeamMCA)
    
    #Set the mCA values to int, clean up a bit, sort, then save it
    outputSeries = df['mCA'].astype(int)
    outputSeries.index.rename('Team', inplace=True)
    outputSeries.name = 'milliCA Rating'
    outputSeries.sort_values(ascending=False, inplace=True)
    outputSeries.to_csv(str(endYear)+'mCA.csv', header=True)