import requests 
import json
from py_availity import Availity

"""
While not currently in use in utilities, it could be used to determine if a payer
    will allow authorizations to be submitted through the api. 
"""

class PayerList(Availity.AvailityABC):
    """ Provides access to the Healthcare Transactions Payer List API"""
    def __init__(self, key, secret):
        super().__init__(key, secret, None)

    def searchPayerList(self, parameters=None):
        """Search Payer list based on input parameters

        Args:
            parameters(json | filename | dict, optional): search parameters.
              can include payerId, transactionType, submissionMode, availability, enrollmentRequired. 
              Desc of each available at: https://developer.availity.com/blog/2025/3/25/hipaa-transactions#payer_list:~:text=payers%20and%20transactions.-,Parameters,-Parameter
        """
        # clean parameters for input
        parameters = self.parseInfo(parameters)
        parameters={x:parameters[x] for x in parameters.keys() if parameters[x] is not None}

        payerSearch = requests.get(
            url="https://api.availity.com/availity/v1/availity-payer-list",
            headers={
                "Content-Type":"application/x-www-form-urlencoded",
                "Authorization":self.authentication
                },
            params=parameters
        )

        return payerSearch.json()
