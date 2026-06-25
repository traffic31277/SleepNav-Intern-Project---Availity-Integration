import _login from './_login.json' with {type: 'json'};
import { coveragePolling, getCoverageSearch } from './AvailityCoverages.js';
import { pullBenefits, validateInsurance,patientPaymentInfo } from './AvailityFunctions.js';
import { pollAuthorizations, authsbyId } from './AvailityServiceReviews.js';
// import { searchPayerList } from './AvailityPayerList.js';
import axios from 'axios';

// config stuff
axios.defaults.baseURL="https://api.availity.com";

/** 
* Returns an authorization token that lasts 5 minutes.
* @param {string} key - The api key, defaults to API_KEY in login.json.
* @param {string} secret - The api secret, defaults to API_SECRET in login.json.
* @return {string} The token returned given the credentials
*/
async function getToken(key=_login.API_KEY, secret=_login.API_SECRET) {
    const url = "/v1/token";
    try {
        const response = await axios.post(
            url, 
            {
                "grant_type": "client_credentials",
                "scope": "healthcare-hipaa-transactions-demo-demo healthcare-hipaa-transactions-demo",
                "client_id": key,
                "client_secret": secret,
            },
            { headers: { "Content-Type": "application/x-www-form-urlencoded", } }
        )
        return response.data['access_token'];
    
    } catch(err) {
        console.error('Error fetching data:', err);
    }
};

/**
 * Sets the authorization token to a new 5 minute token.
 */
export async function resetToken() {
    let token = await getToken(_login.API_KEY, _login.API_SECRET)
    axios.defaults.headers.common['Authorization'] = "Bearer " + token;
};

/**
 * TESTING MAIN FUNCTIONS
 */


await resetToken();

let data = {
    "payer":{
        "id": "123"
    }
}
console.log(await patientPaymentInfo(data));