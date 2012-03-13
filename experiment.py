from datetime import datetime, timedelta
from stock_lists.company_list import CompanyList
from statlib import stats
import random
import smtplib
from email.mime.text import MIMEText
import sys

class ExperimentResult:
        def __init__(self, deltas, time_delta=None):
            self.deltas = deltas
            self.time_delta = time_delta
        
        def stdev(self):
            return stats.stdev(self.deltas)
        
        def mean(self):
            return stats.mean(self.deltas)
        
        def value(self, initial_value):
            final_value = initial_value
            for delta in self.deltas:
                final_value = final_value * (1 + delta)
            return final_value
        
        def profit(self, initial_value):
            return self.value(initial_value) - initial_value
        
        def daily_value(self, initial_value):
            day_value = []
            current_value = initial_value
            for delta in self.deltas:
                current_value = current_value * (1.0 + delta)
                day_value.append(current_value)
            return day_value
        
        def daily_profit(self, initial_value):
            daily_values = self.daily_value(initial_value)
            profits = []
            for day in range(len(daily_values)):
                if day == 0:
                    profit = daily_values[0] - initial_value
                else:
                    profit = daily_values[day] - daily_values[day-1]
                profits.append(profit)
            return profits
        
        def avg_daily_profit(self, initial_value):
            return stats.mean(self.daily_profit(initial_value))
                
        def __str__(self):
            result = "Mean: %f \n Stdev: %f \n Profit on $10,000: $%f" % (self.mean(), self.stdev(), self.profit(10000))
            result += "\n Avg daily profit on $10,000: $%f" % (self.avg_daily_profit(10000))
            if self.time_delta:
                result += "\n Elapsed: %s" % str(self.time_delta)
            return result
        
        
class Experiment:
    def __init__(self, company_list, sample_days=50, start_date=datetime.today() - timedelta(500), day_range=500, percent_correct=0.5, email=None):
        self.company_list = company_list
        self.sample_days = sample_days
        self.start_date = start_date
        self.day_range = day_range
        self.percent_correct = percent_correct
        self.email = email
        
    def run_experiment(self):
        "Returns a list of daily deltas"
        start_time = datetime.now()
        deltas = []
        for day_num in range(sample_days):
            delta = None
            while delta == None:
                date = start_date + timedelta(random.randint(0, day_range))
                delta = self.get_daily_delta(date)
                if delta:
                    deltas.append(delta)
            
        self.deltas = deltas
        elapsed = datetime.now() - start_time
        self.result = ExperimentResult(self.deltas, time_delta=elapsed)
        
        if self.email:
            self.email_result()
            
            
    def get_daily_delta(self, date):
        delta = 0
        delta_flag = False
        companies = self.company_list.get_companies()   
    
        for company in companies:
            opening = company.opening_price(date)
            closing = company.closing_price(date)
            if opening and closing:
                delta_flag = True
                if random.random() < self.percent_correct:
                    delta += abs(opening - closing) / opening
                else:
                    delta -= abs(opening - closing) / opening
        
        if delta_flag:
            return delta
    
    def email_result(self):
        user = "stocks@taylorsavage.com"
        password = 'pali2009adm'
        
        email_body = str(self) + "\n\n" + str(self.result)
        
        msg = MIMEText(email_body)
        msg['Subject'] = "Stock Experiments Result"
        msg['From'] = "stocks@taylorsavage.com"
        msg['To'] = self.email
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, self.email, msg.as_string())
        server.close()
        
        print "Sent email to %s" % self.email
    
    def print_result(self):
        print str(self.result)
        
    def __str__(self):
        return "Experiment: Investing in %s, %d day sample, population beginning %s over %d days, with %f percent prediction accuracy." % (str(self.company_list),
                                                                        self.sample_days,
                                                                        str(self.start_date),
                                                                        self.day_range,
                                                                        self.percent_correct)
                                                                    
        

if __name__ == "__main__": 
    if len(sys.argv) == 1:
        start_date = datetime.strptime(raw_input("Start date: "), '%m/%d/%Y')
        day_range = int(raw_input("Day Range: "))
        sample_days = int(raw_input("Sample days: "))
        company_list = CompanyList(input_str=raw_input("Company List: "))
        percents_correct = [float(p) for p in raw_input("Percents correct: ").split(",")]
        email = raw_input("Email: ")
    else:
        start_date = datetime.strptime("1/1/2010", "%m/%d/%Y")
        day_range = 730
        sample_days = 150
        company_list = CompanyList(input_str="^NDX")
        percents_correct = [0.51, .6, .95]
        email = "taylor@taylorsavage.com"
    
    for pc in percents_correct:
        exp = Experiment(company_list, sample_days, start_date, day_range, pc, email)
        exp.run_experiment()
        print str(exp)
        exp.print_result()