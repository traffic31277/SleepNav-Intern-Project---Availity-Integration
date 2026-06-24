"""
# Availity Integration Python Module

Module for middleware between the Availity Healthcare Transactions API and SleepNav. 

## Dependencies/Install

Built in python 3.14.5

```bash
pip install requests
```

Documentation made with pdoc

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

**Response:**
*full response should include more info (see validateInsurance() function documentation) this is what is available in the demo

```shell
[
  {'status': 'Active - Services Capitated', 'statusCode': '3'},
  {'status': 'Active Coverage', 'statusCode': '1'},
  {'OutOfState': False}
]
```

"""