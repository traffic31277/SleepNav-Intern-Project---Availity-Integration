/**
 * 
 * @module Token
 */
// import { searchPayerList } from './AvailityPayerList.js';
import axios from 'axios';
import _login from './_login.json' with {type: "json"};

// config stuff
axios.defaults.baseURL="https://api.availity.com";

/** 
* Returns an authorization token that lasts 5 minutes.
* @param {string} key - The api key, defaults to API_KEY in login.json.
* @param {string} secret - The api secret, defaults to API_SECRET in login.json.
* @return {string} The token returned given the credentials
*/
async function getToken(key=API_KEY, secret=API_SECRET) {
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

