import requests
import json
from AvailityAbstract import AvailityABC


class Coverages(AvailityABC):
    def __init__(self, key, secret, patientJSON = None, providerJSON = None, subscriberJSON = None):
        super().__init__(key, secret, patientJSON, providerJSON, subscriberJSON)

    def CoveragePolling(self) -> list[str]:
        coveragePoll = requests.post(
            url='https://api.availity.com/availity/v1/coverages',
            headers={
                'Authorization': self.authentication,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=self.patient
        )
        coverages = coveragePoll.json()['coverages']
        ids = [''] * len(coverages)
        for i in range(len(coverages)):
            ids[i] += coverages[i]['id']

        return ids
    
    def getCoveragesSearch(self, ids):
        results = []
        for id in ids:
            searchPoll = requests.get(
                url=f'https://api.availity.com/availity/v1/coverages/{id}',
                headers={'Authorization': self.authentication},
            ).json()
            results.append(searchPoll)

        return results