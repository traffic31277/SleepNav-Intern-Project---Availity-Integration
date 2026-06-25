import patient from './_patient.json' with {type: 'json'};
import subscriber from './_subscriber.json' with {type: 'json'};
import provider from './_provider.json' with {type: 'json'};
import axios from 'axios';

const url = "/v1/availity-payer-list";

/**
 * Searches payer list based on search parameters
 * @param {dict} parameters Params for payer search. options are: payerId, transactionType, 
 *   submissionMode, availability, enrollment, limit, offset. 
 * @returns Search results
 */
export async function searchPayerList(parameters) {        
    try {
        const search_results = await axios.get(
            url, 
            {
                headers: {"Content-Type":"x-www-form-urlencoded"},
                params: parameters
            }
        );

        return search_results.data;

    } catch(err) {
        console.error('Error fetching data:', err);
    }
}