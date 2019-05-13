import requests
from firstelastic import FRCES

baseES = FRCES(2019)

base = 'http://es01.usfirst.org'
eventTeams = '/teams/_search?size=1000&source={"_source":{"exclude":["awards","events"]},"query":{"query_string":{"query":"events.fk_events:%s%%20AND%%20profile_year:%s"}}}'  # (first_eid, year)

testData = requests.get(base + eventTeams % ())
