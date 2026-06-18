import { coveragePolling } from "./AvailityCoverages";
import { checkRequiredArgs } from "./AvailityConfig";
import { authsbyId, pollAuthorizations } from "./AvailityServiceReviews";

//TODO: write docstrings

async function getFromApi(params, api) {
    if (api === "coverages") {
        return await coveragePolling();
    }
    else if (api == "serviceReviews") {
        ids = await pollAuthorizations();
        return await authsbyId(ids);
    }
    else {
        throw "Did not enter valid api, choose 'coverages' or 'serviceReview'";
    }
}

export async function validateInsurance(parameters) {

    // should grab only 1 coverage, but will return a list of any coverage
    // results. entering enough details in the search should only return
    // the 1 set of details.
    let coverage = getFromApi(parameters, "coverages"); 
    let res = [];

    // should only be 1-3 plans. 
    for (let plan of coverage.plans) {
        let planInfo = {};
        for (let item of ['status','statusCode','eligibilityStartDate',
            'eligibilityEndDate', 'insuranceTypeCode','type']) {
            
            try {
                planInfo[item] = plan[item];
            } catch(err) {
                continue;
            };
        }
        res.push(planInfo)
    };

    res.push({'outOfState':coverage.supplementalInformation.outOfArea});
    return res;
}

export async function pullBenefits(parameters) {
    let coverages = getFromApi(parameters, "coverages");
    let srInfo = getFromApi(parameters, "serviceReviews");

    let res = [];
    for (plan of coverages.plans) {
        let planInfo = {};
        for (let item of ['status','statusCode','eligibilityStartDate']) {
            try {
                planInfo[item] = plan[item];
            } catch(err) {
                continue;
            };
        }
        res.push(planInfo);
    };

    res.push({'relationship': srInfo.patient.subscriberRelationshipCode},
        {'isMedicare': srInfo.patient.medicareCoverage});

    // TODO: figure out how to tell if HST is covered
    return res;
}

export async function getAuthInfo(parameters) {
    //TODO: reexamine how to do this
    let res = {"authRequired": getFromApi(parameters, "coverages")};    // in coverages.plans.benefits.authorizationRequired
    let srInfo = getFromApi(parameters, "serviceReviews");
    res.push({
        "authStartDate": srInfo.procedures.certificationEffectiveDate,
        "authEndDate": srInfo.procedures.certificationExperationDate,
        "authNumber": srInfo.certificationNumber,
        "authStatus": srInfo.statusCode
    });

    return res;
}

export async function patientPaymentInfo(parameters) {
    //TODO: figure out how to determine if in network
    network = "inNetwork";
    let coverages = getFromApi(parameters, "coverages");

    let res = [];
    for (let plan of coverages) {
        let planBen = {"status":plan["status"]};
        for (let benefit of plan.benefits) {
            if (benefit["name"] != "Medical Care") { continue };
            
            let benefits = {}
            try {
                benefits["OOPRemaining"] = benefit.costContainment;
            } catch (err) { };
        
            for (let i of ['outOfPocket', 'deductibles', 'coInsurance', 'coPay']) {
                benefits[i] = null
                try {
                    benefit[i] = (
                        benefit.amounts.i.network.amount,
                        benefit.amounts.i.network.unit    
                    )
                } catch (err) { continue };
            };
        
            planBen[benefit.name] = benefits;
        };
        res.append(planBen);
    };

    return res;
}

/** TESTING */
let data = {
    "payer":{
        "id": "123"
    }
}
console.log(validateInsurance(data));