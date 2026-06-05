import requests
import json
from abc import ABC

class AvailityABC(ABC):
    def __init__(self, key, secret, patientJSON: str=None, providerJSON: str=None, subscriberJSON: str=None):
        self.patient = self.parseInfo(patientJSON)
        self.provider = self.parseInfo(providerJSON)
        self.subscriber = self.parseInfo(subscriberJSON)
        self.getToken(key, secret)

    def parseInfo(self, filename: str=None) -> dict:
        try: 
            return json.load(open(filename))
        except:
            return {}
    
    def getToken(self, key, secret) -> None:
        token_request = requests.post(
            url=r'https://api.availity.com/v1/token',
            headers={
                'Content-Type':'application/x-www-form-urlencoded'
            },
            data={
                'grant_type':'client_credentials',
                'scope':'healthcare-hipaa-transactions-demo healthcare-hipaa-transactions-demo-demo',
                'client_id':key,
                'client_secret':secret
            })
        
        token = token_request.json()['access_token']
        self.authentication = "Bearer {}".format(token)