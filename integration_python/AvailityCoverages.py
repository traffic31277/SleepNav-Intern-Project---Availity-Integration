import requests
import json
from AvailityAbstract import AvailityABC


class Coverages(AvailityABC):
    """Provides access to the Health Transactions Coverages API. 
    Can be used to view plan benefits and current status.
    """

    def __init__(self, key, secret, patientJSON = None):
        super().__init__(key, secret, patientJSON)

    def coveragePolling(self, returnIds=False, _patient=None):
        """Poll for coverage information given a patients information

        Args:
            returnIds (bool): if returning a list of the coverage search Ids (True)
            or the coverage details (false). Defaults to False. 

            _patient (json | string | dict), optional: json or filename for patient if not using 
            default set for class. 

        Returns:
            list[str] | json: returns list of ids (strings) or a list of coverages in json format. 
        """

        if _patient is None:
            _patient = self.patient
        else:
            _patient = self.parseInfo(_patient)

        try:
            coveragePoll = requests.post(
                url='https://api.availity.com/availity/v1/coverages',
                headers={
                    'Authorization': self.authentication,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data=_patient
            ).json()
            coverages = coveragePoll['coverages']
            
        except:
            print(f"Error polling coverage information\n"
                  f"{coveragePoll['error']: coveragePoll['error_description']}")

        ids = [''] * len(coverages)
        for i in range(len(coverages)):
            ids[i] += coverages[i]['id']

        if returnIds: 
            return ids
        
        return self.getCoveragesSearch(ids)

    def getCoveragesSearch(self, ids):
        """Gets coverage details based on search Ids (from coveragePolling())

        Args:
            ids (list[str])

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