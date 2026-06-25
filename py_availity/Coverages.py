import requests
import json
from py_availity import Availity

class Coverages(Availity.AvailityABC):
    """Provides access to the Health Transactions Coverages API. 
    Can be used to view plan benefits and current status.
    """

    def __init__(self, key, secret):
        super().__init__(key, secret)

    def get(self, parameters, returnIds=False):
        """Poll for coverage information given a patients information

        Args:
            returnIds (bool): if returning a list of the coverage search 
                Ids (True) or the coverage details (false). Defaults to False. 

            parameters (json | dict | filename): the search parameters 
                (patient member id, dob, state, etc). 
            
        Returns:
            list[str] | json: returns list of ids (strings) or a list of 
                coverages in json format. 

        Raises:
            Exception: KeyError if missing required arg for polling
                config (payer.id and requestTypeCode)
            Exception: If response from coverage API failed
        """
        parameters = self.parseInfo(parameters)
        parameters={x:parameters[x] for x in parameters.keys() if parameters[x] is not None}

        # Parameter cleaning, not implemented right now because of lack of ability to test.

        # try:
        #     self.checkRequiredArgs(parameters, parameters['payer']['id'], 207)
        # except KeyError as err:
        #     raise Exception('Missing key search parameter(payer id or request type code)') from err

        try:
            coveragePoll = requests.post(
                url='https://api.availity.com/availity/v1/coverages',
                headers={
                    'Authorization': self.authentication,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data=parameters
            ).json()
            coverages = coveragePoll['coverages']
        except:
            raise Exception(f"Error polling coverage information\n"
                  f"{coveragePoll['error']: coveragePoll['error_description']}")

        ids = [''] * len(coverages)
        for i in range(len(coverages)):
            ids[i] += coverages[i]['id']

        if returnIds: 
            return ids
        
        return self.getCoveragesSearch(ids)

    def getById(self, ids):
        """Gets coverage details based on search Ids (from self.get())

        Args:
            ids (list[str]): list of search id's as returned from self.get()

        Returns:
            json: format "coverages":[list of coverage details per ids]
        """

        results = {'coverages': []}
        for id in ids:
            searchPoll = requests.get(
                url=f'https://api.availity.com/availity/v1/coverages/{id}',
                headers={'Authorization': self.authentication},
            ).json()
            results['coverages'].append(searchPoll)

        return results