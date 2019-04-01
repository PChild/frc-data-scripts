import gen

tba = gen.setup()

year = 2019

nameMap = []
for event in tba.events(year):
    if event['event_type'] == 0:
        nameMap.append({'Name': event['name'], 'Code': str(2019) + event['event_code']})

gen.listOfDictToCSV(str(year) + ' Event Name Map', nameMap, ['Name', 'Code'])