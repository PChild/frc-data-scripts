import gen

YEAR = 2018
tba = gen.setup()

regionTeams = {}

usRegions = {'California': ['CA', 'California'],
           'Texas': ['TX', 'Texas', 'NM', 'New Mexico'],
           'Midwest': ['OK', 'Oklahoma', 'ND', 'North Dakota', 'SD', 'South Dakota',
                       'KS', 'Kansas', 'WI', 'Wisconsin', 'IL', 'Illinois',
                       'NE', 'Nebraska', 'MO', 'Missouri', 'IA', 'Iowa'],
           'Desert': ['NV', 'Nevada', 'AZ', 'Arizona'],
           'New York': ['NY', 'New York'],
           'Mountain': ['CO', 'Colorado', 'UT', 'Utah', 'ID', 'Idaho', 'WY', 'Wyoming', 'MT', 'Montana'],
           'South': ['Arkansas', 'LA', 'MS', 'AB'],
           'Florida': ['FL', 'Florida'],
           'Minnesota': ['MN', 'Minnesota'],
           'WOW': ['PA', 'WV', 'OH'],
           'South Carolina': ['SC', 'South Carolina'],
           'Hawaii': ['HI', 'Hawaii'],
           'Quebec': ['Quebec', 'QC'],
           'Alberta': ['Alberta', 'AB'],
           'British Columbia': ['British Columbia', 'BC']}

nonUsRegions = ['Australia', 'Turkey', 'Mexico', 'Brazil', 'China']

districts = [item.key for item in tba.districts(YEAR)]
distTeams = []
for district in districts:
    if district != '2018tx':
        districtTeams = tba.district_teams(district, False, True)
        regionTeams[district[4:]] = districtTeams
        distTeams += districtTeams
        
for region in usRegions:
    regionTeams[region] = []

for region in nonUsRegions:
    regionTeams[region] = []
    
teams = []
for page in range(0,20):
        newTeams = tba.teams(page, YEAR)
        if newTeams == []:
            break;
        else:
            teams += newTeams
            
baseTeams = teams[:]
for team in baseTeams:
    if team.key in distTeams:
        teams.remove(team)
    for region in usRegions:
        if team.state_prov in usRegions[region]:
            regionTeams[region].append(team.key)
            teams.remove(team)
        if team.country in nonUsRegions:
            regionTeams[team.country].append(team.key)
            teams.remove(team)
    