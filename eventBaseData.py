import gen

tba = gen.setup()

eventList = tba.events(2018)

data = []
for event in eventList:
    if event['event_type'] in range(0, 10):
        data.append({'Name': event['name'], 'State': event['state_prov'], 'Country': event['country'], 'Type': event['event_type_string']})
        
gen.listOfDictToCSV('2018 Event Base Data', data, ['Name', 'State', 'Country', 'Type'])