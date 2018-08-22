import gen
import pandas as pd

def getYearTeamData(year):
    commits = {'2014': '4fc2a1e7098b6b76a77be4257d134d5016bdbe98',
               '2015': '719399b75c31fc2ba8987b9092c98982e5635513',
               '2016': 'b6918c2adc2d17d09f03c3fa4f6cb81a04067ae3',
               '2017': 'df54d730ff792ee683928d7b31ebe1100043da80',
               '2018': '0737784b208ace11371dc13113fd760bfeae6ab7'}
    
    searchUrl = 'https://raw.githubusercontent.com/the-blue-alliance/the-blue-alliance-data/' + commits[str(year)] + '/teams/teams.csv'
    return pd.read_csv(searchUrl, names=['Key', 'Name', 'Sponsors', 'Location', 'Website', 'Rookie Year'])

def processData(maxYear=2018):
    allTeams = {}
    
    for year in range(2014, maxYear + 1):
        print('On year', year)
        yearData = getYearTeamData(year)
        
        for idx, team in yearData.iterrows():
            if not pd.isnull(team['Sponsors']):
                if team['Key'] not in allTeams:
                    allTeams[team['Key']] = {}
                    for year in range(2014, maxYear + 1):
                        allTeams[team['Key']][str(year)] = {'Count': '', 'Lost': 0, 'Added': 0, 'Sponsors': [], 'Lost Sponsors': [], 'Added Sponsors': []}
                        
                currentYear = allTeams[team['Key']][str(year)]
                
                sponsorList = team['Sponsors'].split('/')
                sponsorCount = len(sponsorList)
                sponsorNames = sponsorList
                
                currentYear['Count'] = sponsorCount
                currentYear['Sponsors'] = sponsorNames
                
                if year is not 2014:
                    prevYear = allTeams[team['Key']][str(year - 1)]
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
    return allTeams

def formatData(data):
    formattedData = []
    
    for team in data:
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
    sponsorData = processData()
    cleanedData = formatData(sponsorData)
    
    colOrder = ['Team']
    keys = ['Count', 'Lost', 'Added', 'Sponsors', 'Lost Sponsors', 'Added Sponsors']
    for year in range(2014, 2019):
        for key in keys:
            colOrder.append(str(year) + ' ' + key)
    
    gen.listOfDictToCSV('FRC Sponsor Data', cleanedData, colOrder)
    
if __name__ == '__main__':
    main()