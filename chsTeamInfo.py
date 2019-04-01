import gen

tba = gen.setup()

event = '2019vagle'

baseURLs = {'facebook-profile': 'www.facebook.com/',
            'twitter-profile': 'www.twitter.com/',
            'youtube-profile': 'www.youtube.com/',
            'github-profile': 'www.github.com/',
            'instagram-profile': 'www.instagram.com/',
            'periscope-profile': 'www.periscope.com/'}

profileTypes = ['facebook-profile',
                'twitter-profile',
                'youtube-profile',
                'github-profile',
                'instagram-profile',
                'periscope-profile']

teamData = []

for team in tba.event_teams(event, False, True):
    teamMedia = tba.team_profiles(team)
    outString = team + ', '
    
    for profile in profileTypes:
        foundMatch = False
        for prof in teamMedia:
            if prof['type'] == profile:
                outString += baseURLs[profile] + prof['foreign_key']
        outString += ', '
    teamData.append(outString)
    
gen.listToCSV(event + 'socialData', teamData)