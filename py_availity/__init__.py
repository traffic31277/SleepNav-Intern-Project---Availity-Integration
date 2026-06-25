"""
# Availity Integration Python Module

Module for middleware between the Availity Healthcare Transactions API and SleepNav. 

## Tech Stack
### Python
Built in python 3.14.5 using [requests](https://docs.python-requests.org/en/latest/index.html
) library. 

## Usage/Examples
**Example:**
```python
# validating insurance information
from availity_python.Utilities import validateInsurance

params = {
  "payer": {
    "id":"123"
  }
}

res = validateInsurance(API_KEY, API_SECRET, params)
```

**Response:**<br>
*full response should include more info (see validateInsurance() function documentation) this is what is available in the demo

```shell
[
  {'status': 'Active - Services Capitated', 'statusCode': '3'},
  {'status': 'Active Coverage', 'statusCode': '1'},
  {'OutOfState': False}
]
```

## Note
There is a discrepency in the completeness of python/js implementations. Python has more tested functionality and more complete documentation. 

"""