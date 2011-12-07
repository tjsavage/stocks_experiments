import os
from pystockquotes import company

class CompanyList:
	def __init__(self, list_name="sandp500"):
		self.list_name = list_name
		file = open(os.path.join(os.path.dirname(__file__), self.list_name + ".txt"), "r")
		
		self.companies = []
		for line in file.read().splitlines():
			if len(line) > 0:
				self.companies.append(company.Company(line))

	
	def get_companies(self):
		return self.companies

	def __len__(self):
		return len(self.companies)

	def __repr__(self):
		return str(self.companies)
