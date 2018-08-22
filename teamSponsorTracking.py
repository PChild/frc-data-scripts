import gen
import pandas as pd

def getYearTeamData(year):
    commits = {'2014': '4fc2a1e7098b6b76a77be4257d134d5016bdbe98',
               '2015': '719399b75c31fc2ba8987b9092c98982e5635513',
               '2016': 'b6918c2adc2d17d09f03c3fa4f6cb81a04067ae3',
               '2017': 'df54d730ff792ee683928d7b31ebe1100043da80',
               '2018': '0737784b208ace11371dc13113fd760bfeae6ab7'}
    
    names = ['Key', 'Name', 'Sponsors', 'Location', 'Website', 'Rookie Year']
    if year > 2016:
        names = ['Key', 'Name', 'Sponsors', 'City', 'State', 'Country', 'Website', 'Rookie Year', 'Facebook', 'Twitter', 'Youtube', 'Github', 'Instagram', 'Periscope']
    
    searchUrl = 'https://raw.githubusercontent.com/the-blue-alliance/the-blue-alliance-data/' + commits[str(year)] + '/teams/teams.csv'
    return pd.read_csv(searchUrl, names=names, index_col=False)

def getAllYearsData(lastYear):
    allYears = []
    
    for year in range(2014, lastYear + 1):
        allYears.append(getYearTeamData(year))
        
    return allYears

def getTeamList(allYears):
    teamList = []
    
    for yearTeams in allYears:
        for idx, team in yearTeams.iterrows():
            if team['Key'][3:] not in teamList:
                teamList.append(team['Key'][3:])
                
    return teamList
                
def prepDict(teamList):
    allData = {}
    for team in teamList:
        allData[team] = {}
        for year in range(2014, 2019):
            allData[team][str(year)] = {'Count': 0, 'Lost': 0, 'Added': 0, 'Sponsors': [], 'Lost Sponsors': [], 'Added Sponsors': []}
    return allData
            
def processData(maxYear=2018):
    allYears = getAllYearsData(maxYear)
    teamList = getTeamList(allYears)
    allData = prepDict(teamList)

    for idx, year in enumerate(range(2014, maxYear + 1)):
        print('On year', year)
        
        yearTeams = allYears[idx]
        
        for idx, team in yearTeams.iterrows():
            if not pd.isnull(team['Sponsors']):
                key = team['Key'][3:]
                currentYear = allData[key][str(year)]
                
                sponsorList = team['Sponsors'].replace('&', '/').replace(',', '').split('/')
                sponsorList = [item.strip() for item in sponsorList]
                
                tmpList = sponsorList[:]
                for s in tmpList:
                    if not bool(s and s.strip()):
                        sponsorList.remove(s)
                        
                sponsorCount = len(sponsorList)
                sponsorNames = sponsorList
                
                currentYear['Count'] = sponsorCount
                currentYear['Sponsors'] = sponsorNames
                
                if year != 2014:
                    prevYear = allData[key][str(year - 1)]
                    prevSponsorList = prevYear['Sponsors']
                    
                    lostSponsors = []
                    lostCount = 0
                    for sponsor in prevSponsorList:
                        if sponsor not in sponsorList:
                            lostCount += 1
                            lostSponsors.append(sponsor)
                    
                    gainedSponsors = []
                    gainedCount = 0
                    for sponsor in sponsorList:
                        if sponsor not in prevSponsorList:
                            gainedCount += 1
                            gainedSponsors.append(sponsor)
                    
                    currentYear['Lost Sponsors'] = lostSponsors
                    currentYear['Added Sponsors'] = gainedSponsors
                    currentYear['Lost'] = lostCount
                    currentYear['Added'] = gainedCount
    return allData

def formatData(data):
    formattedData = []
    
    for team in data:
        if int(team) > 0 and int(team) < 10000:
            teamData = data[team]
            dataObj = {'Team': team}
            
            for year in teamData:
                yearData = teamData[year]
                
                for field in yearData:
                    if type(yearData[field]) is list:
                        dataObj[year + ' ' + field] = ' / '.join(yearData[field])
                    else:
                        dataObj[year + ' ' + field] = yearData[field]
            formattedData.append(dataObj)
    return formattedData

def main():
    MAXYEAR = 2018
    
    sponsorData = processData(MAXYEAR)
    cleanedData = formatData(sponsorData)
    
    cleanedData = sorted(cleanedData, key= lambda k: int(k['Team']))
    
    colOrder = ['Team']
    keys = ['Count', 'Lost', 'Added', 'Sponsors', 'Lost Sponsors', 'Added Sponsors']
    for year in range(2014, MAXYEAR + 1):
        for key in keys:
            colOrder.append(str(year) + ' ' + key)
    
    gen.listOfDictToCSV('FRC Sponsor Data', cleanedData, colOrder)
    
if __name__ == '__main__':
    main()