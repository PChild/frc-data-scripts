import gen

YEAR = 2018
tba = gen.setup()

regionTeams = {}

usRegions = {'California': ['CA', 'California'],
           'Texas': ['TX', 'Texas', 'NM', 'New Mexico'],
           'Midwest': ['OK', 'ND', 'SD', 'KS', 'WI', 'IL', 'NE', 'MO', 'IA'],
           'Desert': ['NV', 'Nevada', 'AZ', 'Arizona'],
           'New York': ['NY', 'New York'],
           'Mountain': ['CO', 'UT', 'ID', 'WY', 'MT'],
           'South': ['Arkansas', 'LA', 'MS', 'AB'],
           'Florida': ['FL', 'Florida'],
           'Minnesota': ['MN', 'Minnesota'],
           'WOW': ['PA', 'WV', 'OH'],
           'South Carolina': ['SC', 'South Carolina']}

nonUsRegions = {}

districts = [item.key for item in tba.districts(YEAR)]
for district in districts:
    if district != '2018tx':
        regionTeams[district[4:]] = tba.district_teams(district, False, True)
    
teams = []
for page in range(0,20):
        newTeams = tba.teams(page, YEAR)
        if newTeams == []:
            break;
        else:
            teams += newTeams