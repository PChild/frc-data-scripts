import gen
from tqdm import tqdm

tba = gen.setup()

year = 2019

basePath = '..\\tba\\events\\' + str(year) + '\\'

def saveAwardsData(event):
    eventAwards = tba.event_awards(event)
    
    awardsData = []
    if eventAwards: 
        for award in eventAwards:
            for idx, recip in enumerate(award['recipient_list']):
                awardsData.append({'awardString': event + '_' + str(award['award_type']),
                                   'awardName': award['name'],
                                   'awardTeam': award['recipient_list'][idx]['team_key'],
                                   'awardPerson': award['recipient_list'][idx]['awardee']})
        
        colOrder = ['awardString', 'awardName', 'awardTeam', 'awardPerson']
        gen.listOfDictToCSV(basePath + event + '\\' + event + '_awards', awardsData, colOrder, False)

for event in tqdm(tba.events(year, False, True)):   
        saveAwardsData(event)