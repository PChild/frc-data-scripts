import statistics as stat
import tbapy
tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

#These control which year and district data is pulled for
YEAR = 2018
DISTRICT = 'chs'

#Structures to hold commonly used data
eventData = {}
teamsList = []

#Fetch district teams and events
distTeams = tba.district_teams(str(YEAR) + DISTRICT, False)
distEvents = tba.district_events(str(YEAR) + DISTRICT)

def storeEventOPRs(event):
    eventData[event]  = tba.event_oprs(event)

#Store data on common district events first
for event in distEvents:
    storeEventOPRs(event['key'])

for team in distTeams:
    print("Processing team " + str(team['key']))
    oprs = []

    events = tba.team_events(team['key'], YEAR)
    
    for event in events:
                
        #Only run on official events, ignores preseason, offseason, and unlabled
        #Try / Except to handle borked events
        #Tries to load data from eventData first, only hits TBA if needed
        #Stores team OPR data for later use.
        if event['event_type'] in range(0,10):
            try:
                if event['key'] in eventData.keys():
                    oprs.append(eventData[event['key']]['oprs'][team['key']])
                else:
                    print("Storing event " + event['key'])
                    storeEventOPRs(event['key'])
                    oprs.append(eventData[event['key']]['oprs'][team['key']])
            #Print errors, typically this has just been teams winning awards when
            #they didn't compete (ie Dean's list, WFA, etc.)
            except Exception as e:
                print(e)
    #Handle teams that we didn't get data for, zero is an OK value for them.
    if len(oprs) is 0:
        maxOPR = 0
        avgOPR = 0
    else:
        maxOPR = max(oprs)
        avgOPR = stat.mean(oprs)
    
    #Store team data in a dict, append that dict to the list of teams 
    teamData = {'num': team['team_number'], 'maxOPR': maxOPR, 'avgOPR': avgOPR, 'city': team['city'], 'state': team['state_prov'], 'rookie_year': team['rookie_year']}
    teamsList.append(teamData)

#File to save out to, will overwrite if script is rerun.
f = open(DISTRICT + str(YEAR) + "OPRs.csv", 'w')

#write out names of data fields. This is kind of bad and uses data from the last
#loop execution to get field names.
for prop in teamData.keys():
    f.write(prop + ", ")
f.write("\n")

#iterate over the teams we got data for and write out their data.
for team in teamsList:
    for prop in team.keys():
        f.write(str(team[prop]) + ", ")
    f.write("\n")
f.close()