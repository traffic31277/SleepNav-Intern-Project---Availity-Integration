import requests
import json
from AvailityAbstract import AvailityABC

class ServiceReview(AvailityABC):
    """Provides access to the Health Transactions Service Reviews API. 
    Can be used to create/view Authorization and Referral Requests
    """
    def __init__(self, key, secret, patientJSON = None):
        super().__init__(key, secret, patientJSON)
    
    def pollAuth(self, params: json):
        """Sends service review inquiry based on params.

        Args:
            params (json): all query paramters

        Raises:
            Exception: KeyError if missing required arg for polling 
            config (payer.id and requestTypeCode)
        """

        parmas = self.parseInfo(params)
        parameters = {x:params[x] for x in params.keys() if x is not None}
        body = {**self.patient, **parameters}

        # checking with config what params are required
        try:
            self.checkRequiredArgs(params, params['payer']['id'],
                                   'service-review',params['requestTypeCode'])  
        except KeyError as err:
            raise Exception('Missing key search parameter(payer id or request type code)') from err


        srInquiry = requests.get(
            url="https://api.availity.com/availity/v2/service-reviews",
            headers={
                "Authorization": self.authentication,
                "X-Api-Mock_Scenario-ID": "SRI-GetComplete-i"
            },
            params=body
        )

