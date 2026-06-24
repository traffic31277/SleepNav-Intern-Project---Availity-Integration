import requests
import json
from availity_python import Availity

class ServiceReview(Availity.AvailityABC):
    """Provides access to the Health Transactions Service Reviews API. 
    Can be used to create/view Authorization and Referral Requests
    """
    def __init__(self, key, secret):
        super().__init__(key, secret)
    
    def get(self, params: json):
        # TODO: update, old and does not reflect current workflow. 
        """Sends service review inquiry based on params.

        Args:
            params (json): all query paramters

        Raises:
            Exception: KeyError if missing required arg for polling 
            config (payer.id and requestTypeCode)
        """

        params = self.parseInfo(params)
        parameters = {x:params[x] for x in params.keys() if x is not None}
        body = {**parameters}

        # checking with config what params are required
        # TODO: uncomment when can check

        # try:
        #     self.checkRequiredArgs(params, params['payer']['id'],
        #                            'service-review', params['requestTypeCode'])  
        # except KeyError as err:
        #     raise Exception('Missing key search parameter(payer id or request type code)') from err

        srInquiry = requests.get(
            url="https://api.availity.com/availity/v2/service-reviews",
            headers={
                "Authorization": self.authentication,
            },
            params=body
        )

        return srInquiry.json()

