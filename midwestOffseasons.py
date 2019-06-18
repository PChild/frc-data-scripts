import gen
import eventTypes

tba = gen.setup()

'''
Midwest definition taken from Bureau of Labor Statisics:
    https://www.bls.gov/regions/midwest/midwest.htm
'''
midwest = ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'MI', 'IN', 'OH']

year = 2019

midwestEvents = []
for event in tba.events(year):
    if event['state_prov'] in midwest and event['event_type'] is eventTypes.OFFSEASON:
        midwestEvents.append({'Start Date': event['start_date'], 'End Date': event['end_date'], 'Event Name': event['name'], 'Location': event['city'] + ' ' + event['state_prov']})

midwestEvents = sorted(midwestEvents, key= lambda k: k['Start Date'])
gen.listOfDictToCSV(str(year) + ' Midwest Offseasons', midwestEvents, ['Event Name', 'Start Date', 'End Date', 'Location'])