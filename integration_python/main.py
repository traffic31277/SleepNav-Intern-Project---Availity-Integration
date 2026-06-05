import json
from AvailityAbstract import AvailityABC
from AvailityCoverages import Coverages
from AvailityServiceReviews import ServiceReview

def main():
    key = json.load(open('_login.json'))['API_KEY']
    secret = json.load(open('_login.json'))['API_SECRET']
    
    sr = ServiceReview(key, secret, '_patient.json')
    sr.pollAuth('AR', '123')
    
    # c = Coverages(key, secret, 'patient.json')
    # cov = c.CoveragePolling()
    # cov = c.getCoveragesSearch(cov)
    
    # print(r)

if __name__ == '__main__':
    main()
