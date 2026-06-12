import json
from AvailityAbstract import AvailityABC
from AvailityCoverages import Coverages
from AvailityServiceReviews import ServiceReview
from AvailityPayerList import PayerList
import requests


def validateInsurance(key, secret):
    c = Coverages(key, secret, patientJSON='_patient.json')
    coverages = c.coveragePolling()

    for plan in coverages['plans']:
        res = {
            "startDate": plan['eligibilityStartDate'],
            "endDate": plan['eligibilityEndDate'],
            "insuranceType": plan['insuranceTypeCode'],
            "planType": plan['type'],
        }

    res['OutOfState': coverages['supplementalInformation']['outOfArea']]
    return res

def pullBenefits(key, secret):
    c = Coverages(key, secret)
    s = ServiceReview(key, secret)

    coverages = c.coveragePolling()
    srInfo = s.pollAuth()

    # plans
    res = {"plans":[]}
    for plan in coverages['plans']:
        res['plans'].append({
            "startDate": plan['eligibilityStartDate'],
            "endDate": plan['eligibilityEndDate'],
        })

    res['relationship':coverages['patient'['subscriberRelationshipCode']]]
    res['isMedicare'] = srInfo['patient']['medicareCoverage']

    
    # if HST is covered
    # will have to look at full complete response body, difficult to tell
    # with the documentation
    return res

def getAuthInfo(key, secret):
    s = ServiceReview(key, secret)
    c = Coverages(key, secret)
    authReq = c.coveragePolling()[0][""]
    srInfo = s.pollAuth()

    res = {
        "authRequired":authReq,
        "authStartDate":srInfo['procedures']['certificationEffectiveDate'],
        "authEndDate":srInfo['procedures']['certificationExperationDate'],
        "authNumber":srInfo['certificationNumber'],
        "authStatus":srInfo['statusCode']
    }

    return res

def patientPaymentInfo(key, secret):
    network = 'inNetwork'

    c = Coverages(key, secret)
    coverages = c.coveragePolling()
    
    res = {"plans":[]}
    for plan in coverages['plans']:
        planBen = []
        for benefit in plan['benefits']: 
            benefits = {"name":benefit['name'], "outOfPocketRemaining":benefit['costContainment']}
            for i in ['deductible', 'outOfPocket', 'deductibles', 'coInsurance', 'coPay']:
                benefits[i] = (benefit['amounts'][i][network]['amount'],
                               benefit['amounts'][i][network]['unit'])
                
            planBen.append(benefits)

    res.append(planBen)

    return res