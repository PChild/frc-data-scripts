import eventTypes
import datetime
import gen

current_date = datetime.datetime.now().strftime('%Y-%m-%d')
tba = gen.setup()

offList = []
for event in tba.events(2019):
    if event.event_type == eventTypes.OFFSEASON:
        if event.start_date > current_date:
            offList.append({'name': event.name, 'code': event.key, 'start': event.start_date, 'end': event.end_date})

offList = sorted(offList, key=lambda k: k['start'])

gen.listOfDictToCSV('2019 OFF Events', offList, ['name', 'code', 'start', 'end'])
