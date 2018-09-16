import gen
from tqdm import tqdm

tba = gen.setup()
events = tba.events(2018)

offseasons = []
for event in tqdm(events):
    if event.event_type == 99 and event.start_date > '2018-05-11':
        locationString = event.city + ' ' + event.state_prov + ' ' + event.country
        
        offseasons.append({'Code': event.event_code,
                           'Name': event.name,
                           'Date': event.start_date,
                           'Location': locationString})
    
gen.listOfDictToCSV('Offseasons Info', offseasons, ['Code', 'Name', 'Date', 'Location'])