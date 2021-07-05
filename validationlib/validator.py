import json
from bs4 import BeautifulSoup

class Validator():
    def __init__(self, file):
        self.file = file
        self.isJson = False
        self.isXML = False
        self.amount_without_taxes = ''
        self.total_rate =0.0
        self.total_amount = 0.0
        self.data ={}

    def check_file(self):
        if self.file.lower().endswith('.json'):
            self.data = open(self.file, 'r').read()
            self.isJson = True
        elif  self.file.lower().endswith('.xml'):
            data = open(self.file, 'r').readlines()
            content = "".join(data) #ARRAY TO STRING
            self.data = BeautifulSoup(content, "lxml")
            self.isXML = True
        else:
            print("This file extension isn\'t supported")
            return ValueError
            
        if self.validate_the_file():
            print(f'All is Correct. Total of {self.total_amount} does include the taxes')
        else:
            print(f'Something went wrong. Total of {self.total_amount} does not include taxes')

    def validate_the_file(self):
        if self.isXML:
            self.amount_without_taxes = float(self.data.find('net_sales_money').amount.text)
            self.total_amount = float(self.data.find('total_money').amount.text)
            taxes = self.data.find('taxes')
            # TODO check if there is more than 1 tax rate applicable
            if taxes:
                tax = float(self.data.find('taxes').rate.text)
                amount_with_tax = float("{:.2f}".format(self.amount_without_taxes + (self.amount_without_taxes*tax)))
                return round(amount_with_tax) == self.total_amount
            return False
        else:
            data = json.loads(self.data)
            taxes = data['taxes']
            self.amount_without_taxes = float(data['itemization'][0]['net_sales_money']['amount'])
            self.total_amount = float(data['total_collected_money']['amount'])
            tax_ids = []
            tax_rates = []
            if len(taxes)>1:
                for tax in taxes:
                    if tax['id'] not in tax_ids:
                        tax_ids.append(tax['id'])     
                        tax_rates.append(tax['rate'])     
            if len(tax_rates)>1:
                for rate in tax_rates:
                    self.total_rate += float(rate)
                amount_with_tax = float("{:.2f}".format(self.amount_without_taxes + (self.amount_without_taxes*self.total_rate)))
                return round(amount_with_tax) == self.total_amount
            else:
                tax = float(tax_rates[0])
                amount_with_tax = float("{:.2f}".format(self.amount_without_taxes + (self.amount_without_taxes*tax)))
                return round(amount_with_tax) == self.total_amount
            return False
            