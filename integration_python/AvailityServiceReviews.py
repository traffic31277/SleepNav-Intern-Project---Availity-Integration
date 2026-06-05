import requests
import json
from AvailityAbstract import AvailityABC

class ServiceReview(AvailityABC):
    def __init__(self, key, secret, patientJSON = None, providerJSON = None, subscriberJSON = None):
        super().__init__(key, secret, patientJSON, providerJSON, subscriberJSON)
    
    def pollAuth(self, reqTypeCode: str, payerId: str, submitterId=None,
                 todate=None, fromDate=None):
        
        body = {**self.provider, **self.patient, **self.subscriber}

        srInquiry = requests.get(
            url="https://api.availity.com/availity/v2/service-reviews",
            headers={
                "Authorization": self.authentication,
                "X-Api-Mock_Scenario-ID": "SRI-GetComplete-i"
            },
            params=body
        )

        print(srInquiry.json())