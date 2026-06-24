import json
from availity_python import Coverages, ServiceReviews
from hashlib import md5

def retrieveInfo(key: str, secret: str, params, api: str) -> str:
    """Retrieve cached response info

    Args:
        params (json): parameters for search, should not cause issue if 
            filled with more information than strictly necessary, given 
            parameter cleaning. 

    Returns:
        tuple[str, str]: (hash for coverages results, hash for service review results)
    """
    if api == "coverages":
        apiEntry = Coverages.Coverages(key, secret)
    elif api == "serviceReview":
        apiEntry = ServiceReviews.ServiceReview(key, secret)
    else:
        raise Exception("Did not enter valid api, choose 'coverages' or 'serviceReview'")

    JSONresult = apiEntry.get(params)
    hash = md5(json.dumps(JSONresult, sort_keys=True, indent=2).encode("utf-8")).hexdigest()
      
    with open(f'..\\cache\\{hash}', 'w+', encoding="utf-8") as file:
        json.dump(JSONresult, file)

    return hash

def readCachedFile(key, secret, params, hash:tuple[str, str]=None):
    """pull cached/cache api results for parsing

    Args:
        params (json): parameters for search, should not cause issue if 
        filled with more information than strictly necessary, given 
        parameter cleaning.
        hash (tuple[str, str], optional): (name of api, results). 
        Defaults to None. If none is entered, new results will be pulled and hashed.

    Returns:
        json: results for covered and service reviews with format: 
        {
            "{hash[0]}": {
                "hash": "{hash{1}}",
                "data": "{api results}"
                }
        }
    """
    try:
        res = {}
        with open(f"..\\cache\\{hash[1]}", 'r', encoding='utf-8') as file:
            res["hash"] =  hash[1]
            res["type"] = hash[0]
            res["data"] = json.load(file)
        return res
    except Exception:
        _hash = retrieveInfo(key, secret, params, hash[0])
        return readCachedFile(key, secret, params, (hash[0], _hash))

def getFromApi(key: str, secret: str, params, api: str):
    if api == "coverages":
        api = Coverages.Coverages(key, secret)
    elif api == "serviceReview":
        api = ServiceReviews.ServiceReview(key, secret)
    else:
        raise Exception("Did not enter valid api, choose 'coverages' or 'serviceReview'")
    
    return api.get(params)

# ------ # 
def validateInsurance(key, secret, params, hash=None):
    """Pulls insurance information for all plans returned from params. 

    Args:
        params (set of all search parameters)
        hash (string, optional): the hash for the coverage results if had. 
        Defaults to None. Pulls new info if none specified. 

    Returns:
        list[json]: list of plan info, each plan result contains:
            status (active, etc.), statusCode, eligibilityStartDate, eligibilityEndDate,
            insuranceTypeCode (HMO?, etc), type (Medical Care, Vision, etc.)
    """

    if hash is None:
        coverages = getFromApi(key, secret, params, "coverages")['coverages'][0]
    else:
        ApiResults = readCachedFile(key, secret, params, ("coverages", hash))
        coverages = ApiResults['data']['coverages'][0]

    res = []

    # There should only be 1-3 plans, if theres more than that narrow search parameters. 
    for plan in coverages['plans']:
        planInfo = {}
        for item in ['name','status','statusCode','eligibilityStartDate','eligibilityEndDate',
                     'insuranceTypeCode','type']:
            try:
                planInfo[item] = plan[item]
            except:
                continue

        res.append(planInfo)

    res.append({'OutOfState': coverages['supplementalInformation']['outOfArea']})
    return res

def pullBenefits(key, secret, params, hashes:tuple=None):
    """Pull benefits information, to include plan start/end dates, 
    relationship to subscriber, if they have medicare, and if
    HSTs are covered*

    *not currently available

    Args:
        params (json): all search parameters
        hashes (tuple, optional): should be (coverages, serviceReview)
        if included. Defaults to None, where that info is pulled.

    Returns:
        list[json]: results
    """

    coverages = getFromApi(key, secret, params, "coverages")['coverages'][0]
    # srInfo = getFromApi(key, secret, params, "serviceReview")['serviceReview'][0]
    
    # ApiResults = readCachedFile(key, secret, params, ("coverages", hashes[0]))
    # coverages = ApiResults['data']['coverages'][0]

    # ApiResults = readCachedFile(key, secret, params, ("serviceReview", hashes[1]))
    # srInfo = ApiResults['data']['serviceReview'][0]

    # plans
    res = []
    for plan in coverages['plans']:
        planInfo = {}
        for item in ['status', 'eligibilityStartDate','eligibilityEndDate']:
            try:
                planInfo[item] = plan[item]
            except:
                continue
        res.append(planInfo)
        
    res.append({'relationship': coverages['patient']['subscriberRelationshipCode']})
    # res['isMedicare'] = srInfo['patient']['medicareCoverage']

    # if HST is covered
    # will have to look at full complete response body, difficult to tell
    # with the documentation
    return res

def getAuthInfo(key, secret, params, hashes:tuple=None):
    """Info on if prior auth is required and if it isn't, 
    what the status is for (if there exists) a requet for one.

    Args:
        params (json): all search parameters
        hashes (tuple, optional): should be (coverages, serviceReview)
        if included. Defaults to None, where that info is pulled.

    Returns:
        json: if auth is required, the auth start date, auth end date,
        auth reference number, and auth status
    """
    
    authReq = getFromApi(key, secret, params, "coverages")['coverages'][0]
    # srInfo = getFromApi(key, secret, params, "serviceReview")['serviceReview'][0]


    # ApiResults = readCachedFile(key, secret, params, ("coverages", hashes[0]))
    # authReq = ApiResults['data']['coverages'][0]

    # ApiResults = readCachedFile(key, secret, params, ("serviceReview", hashes[1]))
    # srInfo = ApiResults['data']['serviceReview'][0]

    srInfo = None

    # Look over once I can pull actual references
    res = {
        "authRequired":authReq,
        "authStartDate":srInfo['procedures']['certificationEffectiveDate'],
        "authEndDate":srInfo['procedures']['certificationExperationDate'],
        "authNumber":srInfo['certificationNumber'],
        "authStatus":srInfo['statusCode']
    }

    return res

def patientPaymentInfo(key, secret, params, hash=None):
    """Get all payment/benefit info (deductibles, coPay, etc.) for Medical Care benefits

    Args:
        params (json): all search parameters
        hash (string, optional): the hash for the coverage results if had. 
        Defaults to None. Pulls new info if none specified. 

    Returns:
        list[json]: list of plans and all of their benefits
    """
    #TODO: figure out how to determine if in network
    network = 'inNetwork'

    coverages = getFromApi(key, secret, params, "coverages")['coverages'][0]
    # ApiResults = readCachedFile(key, secret, params, ("coverages",hash))
    # coverages = ApiResults['data']['coverages'][0]

    res = [] 
    for plan in coverages['plans']:
        planBen = {"status":plan["status"]}
        for benefit in plan['benefits']:
            if benefit['name'] != 'Medical Care':
                continue

            benefits = {}
            try: 
                benefits["OOPRemaining"] = benefit["CostContainment"]   # cost containment is OOP remaining
            except:
                pass

            for i in ['outOfPocket', 'deductibles', 'coInsurance', 'coPayment']:
                benefits[i] = None

                try:
                    benefits[i] = (benefit['amounts'][i][network]['amount'],
                                benefit['amounts'][i][network]['unit'])
                except:
                    continue

            planBen[benefit["name"]] = benefits
            
        res.append(planBen)

    return res
