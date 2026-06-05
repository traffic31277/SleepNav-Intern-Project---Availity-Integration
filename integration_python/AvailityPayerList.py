import requests 
import json
from AvailityAbstract import AvailityABC

class PayerList(AvailityABC):
    def __init__(self, key, secret, patientJSON=None, providerJSON=None, subscriberJSON=None):
        super().__init__(key, secret, patientJSON, providerJSON, subscriberJSON)

    def searchPayerList(self, payerId=None, transactionType=None, submissionMode=None, 
                        availibility=None, enrollmentRequired=None):
        """_summary_

        Args:
            payerId (str, optional): The payer's Availity-specific identifier.
            transactionType (str, optional): The code identifying the EDI/HIPAA transaction(s) supported by a payer.
            submissionMode (str, optional): Accepted method of submission. Can be: Portal, Batch, RealTime, API
            availibility (str optional): _description_.
            enrollmentRequired (bool, optional).
        """

        parameters= {"payerId":payerId, "transactionType":transactionType, "submissionMode":submissionMode,
                 "availibility":availibility, "enrollmentRequired":enrollmentRequired}
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
