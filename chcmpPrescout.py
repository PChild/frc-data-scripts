import tbapy
import string
printable = set(string.printable)

tba = tbapy.TBA('DJRE7IGB1IBTCtvpZfFnn7aZfBWoY9bTIZfQFY7CVBZ8tWeNRX6x0XdISQ63skHv')

def profileHandler(team):
    baseData = tba.team_profiles(team)
    teamLinks = []
    
    for profile in baseData:
        prof = profile['type']
        link = "http://www."
        
        if prof == "facebook-profile":
            link += "facebook.com"
        elif prof == "github-profile":
            link += "github.com"
        elif prof == "instagram-profile":
            link += "instagram.com"
        elif prof == "twitter-profile":
            link += "twitter.com"
        elif prof == "youtube-channel":
            link += "youtube.com"
        elif prof == "periscope-profile":
            link += "periscope.tv"
            
        link += "/"+ profile['foreign_key']
        teamLinks.append(link)
        
    return teamLinks

eventCode = input("Enter event code: ").lower()
eventKey = "2018" + eventCode
print("Fetching data for " + eventKey + "...")
event = tba.event(eventKey)
eventTeams = tba.event_teams(eventKey)
f = open("prescout" + eventKey + ".csv", 'w')


f.write("Team #, Name, Previous, Current Record, Social Media \n")
for team in eventTeams:
    teamLinks = [team['website']]
    teamLinks += profileHandler(team['key'])
    
    teamEvents = tba.team_events(team['key'], '2018', True)
    
    earlyEvents = []
    for ev in teamEvents:
        if ev['start_date'] < event['start_date']:
            earlyEvents.append(ev['event_code'])
            
    f.write(str(team['team_number']) + ", " + ''.join(filter(lambda x: x in printable, team['nickname']))+ ", ")
    if len(earlyEvents) is 0:
        pass
    else:
        for idx in range(len(earlyEvents)):
            f.write(earlyEvents[idx])
            if idx is not len(earlyEvents) - 1:
                f.write(" / ")
    f.write(" , ")
    for link in teamLinks:
        if link is None:
            pass
        else:
            f.write(link + ", ")
    f.write('\n')
f.close()
print("Data collection complete.")