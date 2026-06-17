import requests
import json
from abc import ABC

class AvailityABC(ABC):
    """Abstract class for all Availity API objects."""
    def __init__(self, key, secret, patientJSON: str=None):
        self.resetToken(key, secret)

    def parseInfo(self, jsonFile=None) -> dict:
        """Parses json file or filename and returns corresponding python dictonary.

        Args:
            jsonFile (json | string | dict, optional): Defaults to None (returns {}).
        """
        try: 
            return json.load(open(jsonFile))
        except (TypeError, OSError):
            try:
                return json.loads(json.dumps(jsonFile))
            except:
                return {}
        except:
            return {}
            
    def resetToken(self, key=None, secret=None, login=None):
        """Retrieves 5 minute API access token and sets self.authentication accordingly.\n
        All args default to None to allow for option of input key, secret or login file.\n
        Prioritizes manual key/secret input.
        
        Args:
            key (string, optional): API Key.
            secret (string, optional): API secret.
            login (json | string, optional): filename of json with login or json itself.
        """
        if key is not None and secret is not None:
            _key = key
            _secret = secret
        elif login is not None:
            try:
                loginInfo = self.parseInfo(login)
                _key = loginInfo['key']
                _secret = loginInfo['secret']
            except KeyError:
                print("Error resetting token: Invalid login input (login cred files missing key or secret)")

        token_request = requests.post(
            url=r'https://api.availity.com/v1/token',
            headers={
                'Content-Type':'application/x-www-form-urlencoded'
            },
            data={
                'grant_type':'client_credentials',
                'scope':'healthcare-hipaa-transactions-demo healthcare-hipaa-transactions-demo-demo',
                'client_id':_key,
                'client_secret':_secret
            }).json()

        try:        
            token = token_request['access_token']
            self.authentication = "Bearer {}".format(token)
        except: 
            print((
                f"Authentication Token could not be set."
                f"\n{token_request['error']} : {token_request['error_description']}"))
            
    def checkRequiredArgs(self, params, payerId, type, subTypeId=None):
        
        body = { "payerId":payerId, "type":type}
        if subTypeId is not None:
            body['subTypeId':subTypeId]

        config = requests.get(
            url=r"https://api.availity.com/v1/configurations",
            headers={
                "Authorization": self.authentication,
            },
            data=body
        ).json()
        
        req = []
        allowed = []

        for con in config['configurations']:
            elements = con['elements'].keys()
            for element in elements:
                if con['elements'][element]['required'] == True:
                    req.append(element)
                if con['elements'][element]['allowed'] == True:
                    allowed.append(element)

        try:
        # Will throw if missing
            for par in req:
                _ = params[par]

            # will throw if not in allowed list
            for par in params.keys():
                allowed.remove(par)
        
        except KeyError as err:
            raise Exception('Missing required parameter') from err
        
        except ValueError as err:
            raise Exception('Disallowed paramter input') from err
