# Availity Integration Python Module
*Middleware that extracts information from Availity API. Python and JavaScript versions available.*

## Tech Stack
### Python
Built in python 3.14.5 using [requests](https://docs.python-requests.org/en/latest/index.html) library. 

Python documentation available [here](https://traffic31277.github.io/SleepNav-Intern-Project---Availity-Integration/availity_python.html).

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
