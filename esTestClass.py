import requests

class FirstES(object):
    """
    Helper class for fetching data from FIRST's ElasticSearch instance
    """


    
    def __init__(self, year):
        self.URL_BASE = 'http://es01.usfirst.org'
        self.EVENT_LIST_URL = '/events/_search?size=1000&source={"query":{"query_string":{"query":"(event_type:FRC)%%20AND%%20(event_season:%s)"}}}'  # (year)
        self.EVENT_TEAMS_URL = '/teams/_search?size=1000&source={"_source":{"exclude":["awards","events"]},"query":{"query_string":{"query":"events.fk_events:%s%%20AND%%20profile_year:%s"}}}'  # (first_eid, year)
        self.reqSession = requests.session()
        self.eventKeyMap = self.getEventKeyToIdMap(year)
    
    def _get(self, endpoint):
        """
        Helper method: GET data from given URL
        
        :param endpoint: String for endpoint to get data from.
        :return: Requested data in JSON format.
        """
        return self.session.get(self.URL_BASE + endpoint).json()
    
    def _getEventKeyToIdMap(self, year):
        """
        Builds a dictionary mapping of FRC event keys to corresponding FIRST Event IDs for use in ES.
        
        :param year: Int year to fetch events for
        :return: Dictionary containing the event key to ID map.
        """
        eventList = [hit['_source'] for hit in self._get(self.EVENT_LIST_URL % (year))['hits']['hits']]
        eventKeyMap = {}
        for event in eventList:
            
            """Opted to not return local kickoff events, can re-add if wanted""" 
            if not event['event_subtype'] == 'Local Kickoff':
                eventKey = str(year) + event['event_code'].lower()
                eventKeyMap[eventKey] = event['id']
        
        return eventKeyMap
    
    def event_teams(self, event, simple=False, keys=False):
        """
        Get list of teams at an event.
        
        :param event: Event key to get data on.
        :param simple: Get only vital data.
        :param keys: Return list of team keys only rather than full data on every team.
        :return: List of string keys or Team objects.
        """
        
        #baseList = [hit['_source'] for hit in self.get(self.EVENT_TEAMS_URL, % ())] 
        return 'memes' 
