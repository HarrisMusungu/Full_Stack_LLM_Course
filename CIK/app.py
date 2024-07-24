import requests
from collections import namedtuple


Sec = namedtuple('Sec', ['name', 'ticker', 'cik_id'])

class SecEdgard:
    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.namedict = {}
        self.ticketdict = {}
        self.cikdict = {}


        headers = {'user-agent' : 'MLT FEL hmusungu03@gmail.com'}
        response = requests.get(self.fileurl, headers = headers)

        self.filejson = response.json()
        self.cik_json_to_dict()


    
    def cik_json_to_dict(self):
        for _, value in self.filejson.items():
            cik_id = value["cik_str"]
            company_name = value["title"]
            ticker = value["ticker"]

            self.namedict[company_name] = cik_id
            self.ticketdict[ticker] = cik_id
            self.cikdict[cik_id] = (company_name, ticker)
    
    def name_to_cik(self, name):
        if name not in self.namedict:
            raise BaseException("Cant find name in dictionary")
        
        cik_id = self.namedict[name]
        _, ticker = self.cikdict[cik_id]

        return Sec(name=name, ticker=ticker, cik_id=cik_id)
    
    def ticker_to_cik(self, ticker):
        if ticker not in self.ticketdict:
            raise BaseException("Cant find ticker in dictionary")
        
        cik_id = self.ticketdict[ticker]
        company_name, _ = self.cikdict[cik_id]

        return Sec(name=company_name, ticker=ticker, cik_id=cik_id)


if __name__ == "__main__":
    url = "https://www.sec.gov/files/company_tickers.json"
    edgar = SecEdgard(url)

    print(edgar.name_to_cik('United Maritime Corp'))
    print(edgar.ticker_to_cik('USEA'))

