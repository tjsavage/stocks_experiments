from datetime import datetime, timedelta
from stock_lists.company_list import CompanyList
from statlib import stats
import random

def run_experiment(company_list = CompanyList(list_name='sandp500'), sample_days=50, start_date=datetime.today() - timedelta(500), day_range=500, percent_correct=0.5, stocks_per_day=10):
    "Returns a list of daily deltas"
    deltas = []
    for day_num in range(sample_days):
        delta = None
        while delta == None:
            date = start_date + timedelta(random.randint(0, day_range))
            delta = get_daily_delta(date, company_list, percent_correct, stocks_per_day)
            if delta:
                deltas.append(delta)
        
    return deltas
        
        
def get_daily_delta(date, company_list, percent_correct=1.0, num_stocks=10):
    delta = 0
    delta_flag = False
    companies = random.sample(company_list.get_companies(), num_stocks)    

    for company in companies:
        opening = company.opening_price(date)
        closing = company.closing_price(date)
        if opening and closing:
            delta_flag = True
            if random.random() < percent_correct:
                delta += abs(opening - closing) / opening
            else:
                delta -= abs(opening - closing) / opening
    
    if delta_flag:
        return delta

if __name__ == "__main__": 
    start_date = datetime.strptime(raw_input("Start date: "), '%Y%m%d')
    day_range = int(raw_input("Day Range: "))
    sample_days = int(raw_input("Sample days: "))
    company_list = CompanyList(raw_input("Company List: "))
    stocks_per_day = int(raw_input("Stocks per day: "))
    percents_correct = [float(p) for p in raw_input("Percents correct: ").split(",")]
    
    results = {}

    for trial in range(len(percents_correct)):
        deltas = run_experiment(company_list = company_list, sample_days=sample_days, start_date = start_date, day_range = day_range, percent_correct=percents_correct[trial], stocks_per_day=stocks_per_day)
        print "Percent correct: %f, %s" % (percents_correct[trial], str(deltas))
        print "\t (%f, %f)" % (stats.mean(deltas), stats.stdev(deltas))
        results[percents_correct[trial]] = deltas
    
    print results
