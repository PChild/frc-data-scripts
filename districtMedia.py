import gen

tba = gen.setup()

YEAR = 2018
DISTRICT = 'iri'

distTeams = []
iriTeams = ["frc20", "frc33", "frc67", "frc88", "frc118", "frc133", "frc195", 
            "frc217", "frc225", "frc234", "frc245", "frc302", "frc319", 
            "frc340", "frc359", "frc384", "frc469", "frc494", "frc624", 
            "frc694", "frc708", "frc829", "frc865", "frc868", "frc1024", 
            "frc1102", "frc1218", "frc1533", "frc1619", "frc1640", "frc1706", 
            "frc1710", "frc1720", "frc1731", "frc1741", "frc1746", "frc1747", 
            "frc1806", "frc2013", "frc2056", "frc2168", "frc2337", "frc2363", 
            "frc2451", "frc2468", "frc2481", "frc2590", "frc2614", "frc2655", 
            "frc2771", "frc2791", "frc2826", "frc2834", "frc3357", "frc3452", 
            "frc3478", "frc3538", "frc3641", "frc3707", "frc3847", "frc3940", 
            "frc4028", "frc4265", "frc4499", "frc4587", "frc4944", "frc4967", 
            "frc5254", "frc5406", "frc6800"]

teamList = iriTeams

for index, tm in enumerate(teamList):
    gen.progressBar(index, len(teamList))
    team = tba.team(tm)
    
    distTeams.append({'team': team['team_number'], 'name': team['nickname'], 'website': team['website'], 'facebook': "", 'github': "", 'twitter': "", 'instagram': "", 'youtube': ""})
    
    for site in tba.team_profiles(team['team_number']):
        siteType = site['type'][:-8]
        distTeams[index][siteType] = "www." + siteType + ".com/" + site['foreign_key']

colOrder = []

gen.listOfDictToCSV(DISTRICT + str(YEAR) + "profiles", distTeams)