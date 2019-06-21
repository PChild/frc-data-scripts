import gen
import eventTypes

tba = gen.setup()

regCnt = 0

for event in tba.events(2019):
    if event['event_type'] == eventTypes.REGIONAL:
        regCnt += 1
        
print(regCnt)