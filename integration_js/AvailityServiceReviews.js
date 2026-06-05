import patient from './_patient.json' with {type: 'json'};
import subscriber from './_subscriber.json' with {type: 'json'};
import provider from './_provider.json' with {type: 'json'};
import axios from 'axios';

const url = "/v2/service-reviews";
let sessionId = "0";

export async function pollAuthorizations(requestTypeCode=null, payerId=null, submitterId=null,
    toDate=null, fromDate=null
) {
    let body = Object.assign({}, [patient, subscriber, provider]);
    try {
        const poll = await axios.get(
            url,
            {
                params: body,
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            },
        );

        sessionId =  poll.headers['Location'].slice(poll.headers['Location'].lastIndexOf("/")+1);
        return sessionId;

    } catch(err) {
        console.log("error polling auths: ", err['response']['data']['error'])
    };
};

export async function authsbyId(session=sessionId) {
    try {
        const auth_res = await axios.get(
            url, 
            { params: { 'sessionId':session } }
        );
        
        let reviews = [];
        for (let i = 0; i < auth_res.text['serviceReviews'].length; i++) {
            reviews.push(
                {
                    'id': auth_res.text['serviceReviews'][i]['id'], 
                    'statusCode': auth_res.text['serviceReviews'][i]['statusCode']
                })
    };

    } catch (err) {
        console.log("error pulling auth information: ", err['response']['data']['error'])        
    }

};
