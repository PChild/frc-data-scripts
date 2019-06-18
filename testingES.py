from firstelastic import FRCES

baseES = FRCES(2019)

test = baseES.get_event_teams('2019vabla', False, True)
getMap = baseES._get_tba_es_field_map()