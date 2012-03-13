import os
from pystockquotes import company

class CompanyList:
    def __init__(self, list_name=None, ticker_string=None, input_str=None):
        if list_name:
            self.read_companies_from_file(list_name)
        elif ticker_string:
            self.read_companies_from_string(ticker_string)
        elif input_str:
            if ".txt" in input_str:
                self.read_companies_from_file(input_str)
            else:
                self.read_companies_from_string(input_str)
                
    def read_companies_from_file(self, list_name):
        self.list_name = list_name
        file = open(os.path.join(os.path.dirname(__file__), self.list_name + ".txt"), "r")
        
        self.companies = []
        for line in file.read().splitlines():
            if len(line) > 0:
                self.companies.append(company.Company(line))
    
    def read_companies_from_string(self, ticker_string):
        self.companies = []
        for ticker in ticker_string.split(","):
            self.companies.append(company.Company(ticker.strip()))
    
    def get_companies(self):
        return self.companies

    def __len__(self):
        return len(self.companies)

    def __repr__(self):
        return str(self.companies)
    
    def __str__(self):
        return " ".join([str(c) for c in self.companies])
