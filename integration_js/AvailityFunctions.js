import { coveragePolling } from "./AvailityCoverages";
import { checkRequiredArgs } from "./AvailityConfig";
import { pollAuthorizations } from "./AvailityServiceReviews";

export async function validateInsurance() {

    // should grab only 1 coverage, but will return a list of any coverage
    // results. entering enough details in the search should only return
    // the 1 set of details.
    let coverage = coveragePolling(false)[0];   
    
    let res = [];

    // should only be 1-3 plans. 
    for (let plan of coverage.plans) {
        res.push({
            "status":plan.status,
            "statusCode":plan.statusCode,
            "startDate": plan.eligibilityStartDate,
            "endDate": plan.eligibilityEndDate,
            "insuranceType": plan.insuranceTypeCode,
        })
    };

    res.push({'outOfState':coverage.supplementalInformation.outOfArea});
    return res;
}

export async function pullBenefits() {
    let coverages = coveragePolling();
    let srInfo = pollAuthorizations();

    let res = {"plans":[]};
    for (plan of coverages.plans) {
        res.plans.push({
            "status":plan.status,
            "startDate":plan.eligibilityStartDate,
            "endDate":plan.eligibilityEndDate,
            "benefits":plan.benefits
        });
    };

    res.push({
        'relationship': srInfo.patient.subscriberRelationshipCode,
        'isMedicare': srInfo.patient.medicareCoverage
    });

    // TODO: figure out how to tell if HST is covered
    return res
}

export async function getAuthInfo() {
    let res = {"authRequired": coveragePolling()[0]};    // in coverages.plans.benefits.authorizationRequired
    let srInfo = pollAuthorizations();
    res.push({
        "authStartDate": srInfo.procedures.certificationEffectiveDate,
        "authEndDate": srInfo.procedures.certificationExperationDate,
        "authNumber": srInfo.certificationNumber,
        "authStatus": srInfo.statusCode
    });

    return res;
}

export async function patientPaymentInfo() {
    //TODO: figure out how to determine if in network
    network = "inNetwork";

    let coverages = coveragePolling();

    //TODO: figure out better way to do this
    let res = {"plans": []};
    for (let plan of coverages) {
        let planBen = [];
        for (let benefit of plan.benefits) {
            let benefits = {
                "name":benefit.name,
                "outOfPocketRemaining":benefit.costContainment
            };
        
            for (let i of ['outOfPocket', 'deductibles', 'coInsurance', 'coPay']) {
                benefit[i] = (
                    benefit.amounts.i.network.amount,
                    benefit.amounts.i.network.unit    
                )
            };
        
            planBen.append(benefits);
        };
        res.append(planBen);
    };

    return res;
}

