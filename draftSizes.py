import gen

tba = gen.setup()

teamCount = 14
draftSize = teamCount * 3

singleTier = 0
multiTier = 0
regionalCount = 0
for event in tba.events(2018):
    if event['event_type'] == 0:
        regionalCount += 1
        
        teamCount = len(tba.event_teams(event['key'], False, True))
        
        if teamCount < draftSize:
            multiTier += 1
        else:
            singleTier += 1
        
print("Of", regionalCount, "regionals,", multiTier, "would need multiple tiers.", )