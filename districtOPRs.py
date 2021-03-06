import statistics as stat
import gen
tba = gen.setup()

#These control which year and district data is pulled for
YEAR = 2018
DISTRICT = 'chs'

#Structures to hold commonly used data
eventData = {}
teamsList = []

#Fetch district teams and events
distTeams = tba.district_teams(str(YEAR) + DISTRICT, False)
distEvents = tba.district_events(str(YEAR) + DISTRICT)

#Store data on common district events first
for event in distEvents:
    eventData[event['key']]  = tba.event_oprs(event['key'])

teamCount = 0
for team in distTeams:
    teamCount += 1
    gen.progressBar(teamCount, len(distTeams))
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
                    eventData[event['key']]  = tba.event_oprs(event['key'])
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

gen.listOfDictToCSV(DISTRICT + str(YEAR) + "OPRs", teamsList)