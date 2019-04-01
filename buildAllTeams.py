import gen
from tqdm import tqdm

tba = gen.setup()

#Set this to None for ALL teams
year = 2019

teamList = []
for page in tqdm(range(0,40)):
    currentTeams = tba.teams(page, year, False, True)
    
    if currentTeams == []:
        break
    else:
        teamList += currentTeams
        
if year is not None:
    fileKey = str(year) +'TeamKeys'
else:
    fileKey = 'allTeamKeys'
gen.listToCSV(fileKey, teamList)