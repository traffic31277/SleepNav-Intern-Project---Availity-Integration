import requests
import json
from AvailityAbstract import AvailityABC


class Coverages(AvailityABC):
    """Provides access to the Health Transactions Coverages API. 
    Can be used to view plan benefits and current status.
    """

    def __init__(self, key, secret):
        super().__init__(key, secret)

    def get(self, parameters: json, returnIds=False):
        """Poll for coverage information given a patients information

        Args:
            returnIds (bool): if returning a list of the coverage search Ids (True)
            or the coverage details (false). Defaults to False. 

            _patient (json | string | dict), optional: json or filename for patient if not using 
            default set for class. 

        Returns:
            list[str] | json: returns list of ids (strings) or a list of coverages in json format. 

        Raises:
            Exception: KeyError if missing required arg for polling 
            config (payer.id and requestTypeCode)
            Exception: If response from coverage API failed
        """
        parameters = self.parseInfo(parameters)
        parameters={x:parameters[x] for x in parameters.keys() if parameters[x] is not None}

        # TODO: uncomment
        # try:
        #     self.checkRequiredArgs(parameters, parameters['payer']['id'], 207)
        # except KeyError as err:
        #     raise Exception('Missing key search parameter(payer id or request type code)') from err

        # TODO: uncomment
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