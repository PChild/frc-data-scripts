import gen
import eventTypes

tba = gen.setup()

year = 2019

regionals = []
for event in tba.events(2019):
    if event['event_type'] == eventTypes.REGIONAL:
        if event['country'] != 'China':
            regionals.append({'Code': event['key'],
                              'Week': event['week'],
                              'Start Date': event['start_date']})
    
regionals = sorted(regionals, key= lambda k: k['Start Date'])
gen.listOfDictToCSV(str(year)+' Regionals', regionals, ['Code', 'Week', 'Start Date'])