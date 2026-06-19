import { coveragePolling } from "./AvailityCoverages.js";
import { checkRequiredArgs } from "./AvailityConfig.js";
import { authsbyId, pollAuthorizations } from "./AvailityServiceReviews.js";

//TODO: write docstrings

/**
 * Pulls from requested API based on input parameters
 * @param {json} params search parameters
 * @param {string} api The name of the api being called (coverages or serviceReviews)
 * @returns api results
 */
async function getFromApi(params, api) {
    if (api === "coverages") {
        let c = await coveragePolling()
        c = await c[0];
        return c;
    }
    else if (api == "serviceReviews") {
        ids = await pollAuthorizations();
        return await authsbyId(ids);
    }
    else {
        throw "Did not enter valid api, choose 'coverages' or 'serviceReview'";
    }
}

/**
 * Pulls insurance information for all plans returned from params. 
 * @param {json} parameters list of search paramters for searching
 * @returns {json} all necessary insurance plan information for validation (status, start/end dates, type)
 */
export async function validateInsurance(parameters) {

    // should grab only 1 coverage, but will return a list of any coverage
    // results. entering enough details in the search should only return
    // the 1 set of details.
    let coverage = await getFromApi(parameters, "coverages"); 
    let res = [];

    // should only be 1-3 plans. 
    for (let plan of coverage.plans) {
        let planInfo = {};

        for (let item of ['status','statusCode','eligibilityStartDate',
            'eligibilityEndDate', 'insuranceTypeCode','type']) {
            planInfo[item] = plan[item];
        }
        res.push(planInfo)
    };

    res.push({'outOfState':coverage.supplementalInformation.outOfArea});
    return res;
}

/**
 * Pull benefits information
 * 
 * @param {json} parameters search parameters for benefits
 * @returns json of all benefits statuses, start/end dates, the 
 * patients relationship to the subscriber, if the patient has 
 * medicare, and if HST's are covered.
 */
export async function pullBenefits(parameters) {
    let coverages = await getFromApi(parameters, "coverages");
    // let srInfo = await getFromApi(parameters, "serviceReviews");

    let res = [];
    for (let plan of coverages.plans) {
        let planInfo = {};
        for (let item of ['status','statusCode','eligibilityStartDate', 'eligibilityEndDate']) {
            planInfo[item] = plan[item];
        }
        
        res.push(planInfo);
    };

    // res.push({'relationship': srInfo.patient.subscriberRelationshipCode},
    //     {'isMedicare': srInfo.patient.medicareCoverage});

    // TODO: figure out how to tell if HST is covered
    return res;
}

/**
 * Info on if prior auth is required and if it isn't, 
 * what the status is for (if there exists) a requet for one.
 * @param {json} parameters all search parameters
 * @returns if auth is required, the auth start date, auth end date, 
 * auth reference number, and auth status
 */
export async function getAuthInfo(parameters) {
    //TODO: reexamine how to do this
    let res = {"authRequired": await getFromApi(parameters, "coverages")};    // in coverages.plans.benefits.authorizationRequired
    let srInfo = await getFromApi(parameters, "serviceReviews");
    res.push({
        "authStartDate": srInfo.procedures.certificationEffectiveDate,
        "authEndDate": srInfo.procedures.certificationExperationDate,
        "authNumber": srInfo.certificationNumber,
        "authStatus": srInfo.statusCode
    });

    return res;
}

/**
 * Get all payment/benefit info (deductibles, coPay, etc.) for Medical Care benefits
 * @param {json} parameters all search parameters
 * @returns 
 */
export async function patientPaymentInfo(parameters) {
    //TODO: figure out how to determine if in network
    let network = "inNetwork";
    let coverages = await getFromApi(parameters, "coverages");

    let res = [];
    for (let plan of coverages.plans) {
        let planBen = {"status":plan["status"]};
        for (let benefit of plan.benefits) {
            if (benefit["name"] != "Medical Care") { continue };
            
            let benefits = {"OOPRemaining": benefit.costContainment};
        
            for (let i of ['outOfPocket', 'deductibles', 'coInsurance', 'coPay']) {
                try {
                    benefits[i] = (
                            benefit.amounts[i][network].amount,
                            benefit.amounts[i][network].unit    
                        )
                } catch (err) { };
            };

            planBen["benefits"] = benefits;
        };
        res.push(planBen);
    };

    return res;
}
