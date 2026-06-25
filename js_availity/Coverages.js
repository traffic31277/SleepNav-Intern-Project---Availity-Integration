import axios from 'axios';

export const url = "/v1/coverages";

/**
 * Polls the coverage API given the patient information (memberID, DOB, State). 
 * @param {bool} returnIds If returning search result Ids (details can be returned from getCoverageSearch).
 *  Otherwise returns full coverage details.
 * @param {dict} patientInfo Specify patients information. Defaults to patient.json.
 * @returns {list} A list of the plans a patient by their ids or the coverage details.
 */

export async function coveragePolling(parameters, returnIds=false) {
    try {
        const poll = await axios.post(
            url,
            parameters,
            { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );
        
        let coverages = poll.data['coverages'];
        const ids = [];

        for (let i = 0; i < coverages.length; i++) {
            ids.push(coverages[i]['id']);
        };

        if (returnIds) {return ids;}
        else {
            return await getCoverageSearch(ids);
        };

    } catch(err) {
        console.error('Error fetching data:', err);
    };
};

/**
 * Coverage Details from ids.
 * @param {list} ids ids returned from coveragePolling. 
 * @returns A list of coverage details.
 */

export async function getCoverageSearch(ids) {
    const results = [];
    for (let i = 0; i < ids.length; i++) {
        try {
            const search = await axios.get(
                url + `/${ids[i]}`,
                {},
            );
            results.push(search.data);
        } catch(err) {
            console.error('Error fetching data:', err);
        }
    };
    return results;
};