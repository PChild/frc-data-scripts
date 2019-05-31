import gen
import eventTypes

tba = gen.setup()

eventKey = 'walcott'
teams = [58, 155, 173, 177, 178, 195, 228, 230, 237, 558, 716, 999, 1071, 1099, 2064, 2067, 3461, 3525, 3654, 4055,
         4557, 5943, 7127, 7153, 7462, 7694]

normalEvents = [eventTypes.DISTRICT, eventTypes.CMP_DIVISION, eventTypes.REGIONAL,
                eventTypes.DISTRICT_CMP, eventTypes.DISTRICT_CMP_DIVISION]

outData = []
for team in teams:
    maxOPR = 0
    for event in tba.team_events('frc' + str(team), 2019):
        if event.event_type in normalEvents:
            eventOPR = tba.event_oprs(event.key)['oprs']['frc' + str(team)]
            if eventOPR > maxOPR:
                maxOPR = eventOPR
    outData.append({'team': team, 'opr': maxOPR})

gen.listOfDictToCSV(eventKey + ' max opr', outData, ['team', 'opr'])
