/**
 * 
 * 
 * @module Config
 */


import axios from 'axios';
export const url = "/v1/configurations";

export async function checkRequiredArgs(params, payerId, type, subtypeId) {
    const results = [];
    try {
        const search = await axios.get(
            url,
            {   "payerId":payerId,
                "type": type,
                'subtypeId':subtypeId
            }
        );

        let configs = search.data;
        const req = [];
        const allowed = [];

        for (let con in configs['configurations']) {
            for (let element in con['elements']) {
                if (configs['configurations'][con]['elements'][element]['required'] == True) {
                    req.push(element);
                }
                if (configs['configurations'][con]['elements'][element]['allowd'] == True) {
                    allowed.push(element);
                };
            };
        };

        for (let par of req) {
            if (!(par in params)) {
                throw `Doesn't include required paramter: ${par}`;
            };
        };
        
        const filterAllowed = (value, i, arr) => {
            if (!(value in allowed)) {
                return true;
            };
            return false;
        };

        const filteredAllowed = params.filter(filterAllowed);

        return params;

    } catch(err) {
        
    }
}