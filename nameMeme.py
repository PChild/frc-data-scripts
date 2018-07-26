from multiprocessing import Pool
import gen

tba = gen.setup()

def getTeamData(tm):
    team = tba.team(tm)
    return({'Team': team['team_number'], 'Name': team['nickname'].replace(",", ""), 'Sponsors': team['name'].count('/') + 1, 'Full Name': team['name'].replace(",", "")})

def main():
    teams = []
    teamList = gen.readTeamListCsv(2018)['Teams']
    pool = Pool()
    teams += pool.map(getTeamData, teamList)
        
    teams = sorted(teams, key= lambda k: k['Sponsors'], reverse=True)
    colOrder = ['Team', 'Name', 'Sponsors', 'Full Name']
    gen.listOfDictToCSV("Team Sponsors", teams, colOrder)

if __name__ == '__main__':
    main()