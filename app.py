import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, jsonify

def scrape_stockbeep(mode):
    result_arr = []
    if mode == 'down':
        url = 'https://stockbeep.com/table-data/gap-down-stocks?hash=4b6b14a2ec0312fff4d0e4955285c691&country=us&time-zone=480&sort-column=gap&sort-order=asc&_=1613421148844'
    
    elif mode == 'up':
        url = 'https://stockbeep.com/table-data/gap-up-stocks?hash=c607a9b6fce5964fe43a926e8875cc3c&country=us&time-zone=480&sort-column=gap&sort-order=asc&_=1613424875878'
    
    elif mode == 'trending':
        url = 'https://stockbeep.com/table-data/trending-stocks?hash=9ca490d673396cdeb85a7b0e479a7f90&country=us&time-zone=480&sort-column=sschgp&sort-order=desc&_=1613425492941'
        
    elif mode == 'downtrend':
        url = 'https://stockbeep.com/table-data/downtrend-stocks?hash=b8c2b85cd8d63ae25e6a5b0ed58db5dd&country=us&time-zone=480&sort-column=sschgp&sort-order=asc&_=1613503991857'
    elif mode == 'unusual-vol':
        url = 'https://stockbeep.com/table-data/unusual-volume-stocks?hash=c99c8cc88e45755bd24c317d4e1c5403&country=us&time-zone=480&sort-column=ssrvol&sort-order=desc&_=1613504692483'
    
    
    r = requests.get(url)
    results = r.json()['data']
    
    for result in results:
        obj = {}
        if mode == 'down' or mode == 'up':
            if mode == 'down':
                time = result['lotime']
                low = result['sslow']
                
            elif mode == 'up':
                time = result['sstime']
                high = result['sshigh']
             
            chop = result['chgop']
            chop_perc = result['chgopp']
            dollar = result['ssdlr']
            vol = result['ssvol']
            rvol = result['ssrvol']
            ticker = result['sscode'].split('>')[1].split('<')[0].strip()
            comment = result['sscomment']
            cap = result['sscap']
            gap = result['gap']
            name = result['ssname']
            last = result['sslast']
            
            if mode == 'down':
                obj['Low'] = low
                
            elif mode == 'up':
                obj['High'] = high
                
            obj['Time'] = time    
            obj['ChOp'] = chop
            obj['ChOp%'] = chop_perc
            obj['$'] = dollar
            obj['Vol'] = vol
            obj['Rvol'] = rvol
            obj['Ticker'] = ticker
            obj['Comment'] = comment
            obj['Cap'] = cap
            obj['Gap'] = gap
            obj['Name'] = name
            obj['Last'] = last
        
        if mode == 'trending' or mode == 'downtrend':
            if mode == 'downtrend':
                low = result['sslow']
                time = result['lotime']
                
            elif mode == 'trending':
                time = result['sstime']
                high = result['sshigh']
                
            chg = result['sschg']
            chgp = result['sschgp']
            five_d = result['5d']
            cap = result['sscap']
            name = result['ssname']
            last = result['sslast']
            comment = result['sscomment']
            vol = result['ssvol']
            rvol = result['ssrvol']
            dollar = result['ssdlr']
            ticker = result['sscode'].split('>')[1].split('<')[0].strip()
            
            if mode == 'trending':
                obj['High'] = high
                
            elif mode == 'downtrend':
                obj['Low'] = low
                
            obj['Chg%'] = chg
            obj['Chg%'] = chgp
            obj['5D%'] = five_d
            obj['Cap'] = cap
            obj['Comment'] = comment
            obj['Name'] = name
            obj['Last'] = last
            obj['Time'] = time
            obj['Vol'] = vol
            obj['Rvol'] = rvol
            obj['$'] = dollar
            obj['Ticker'] = ticker
            
        if mode == 'unusual-vol':
            time = result['sstime']
            high = result['sshigh']
            chg = result['sschg']
            chgp = result['sschgp']
            name = result['ssname']
            last = result['sslast']
            comment = result['sscomment']
            ticker = result['sscode'].split('>')[1].split('<')[0].strip()
            dollar = result['ssdlr']
            vol = result['ssvol']
            rvol = result['ssrvol']
            five_m_vol = result['ss5mvol']
            cap = result['sscap']
            
            obj['Vol'] = vol
            obj['Rvol'] = rvol
            obj['Ticker'] = ticker
            obj['Comment'] = comment
            obj['Cap'] = cap
            obj['Name'] = name
            obj['Last'] = last
            obj['$'] = dollar
            obj['5mvol'] = five_m_vol
            obj['High'] = high
            obj['Time'] = time
            obj['Chg%'] = chg
            obj['Chg%'] = chgp
            
        
            
            
            
        
        result_arr.append(obj)
        
    return result_arr
    
    
  
  
    
    
def scrape_marketbeat():
    result_arr = []
    url = 'https://www.marketbeat.com/ipos/lockup-expirations/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tbody_rows = soup.find('table', class_='scroll-table').find('tbody').findAll('tr')
    
    for row in tbody_rows:
        has_good_company_td = False
        obj = {}
        tdatas = row.findAll('td')
        for index, tdata in enumerate(tdatas):
            if index == 0:
                try:
                    company_initial = tdata.a.findChildren("div" , recursive=False)
                    has_good_company_td = True
                except Exception as e:
                    pass
                
                if has_good_company_td:
                    if len(company_initial) == 2:
                        obj['Company_Name'] = company_initial[1].text.strip()
                    
                    else:
                        obj['Company_Name'] = company_initial[2].text.strip()

                else:
                    tdata.text.strip()
                
            elif index == 1:
                current_price = tdata.text.strip()
                obj['Current_Price'] = current_price
            elif index == 2:
                exp_date = tdata
                
            elif index == 3:
                num_of_shares = tdata.text.strip()
                obj['Num_Of_Shares'] = num_of_shares
                
            elif index == 4:
                init_share_price = tdata.text.strip()
                obj['Init_Share_Price'] = init_share_price
                
            elif index == 5:
                offer_size = tdata.text.strip()
                obj['Offer_Price'] = offer_size
                
            elif index == 6:
                date_priced = tdata.text.strip()
                obj['Date_Priced'] = date_priced
        
        result_arr.append(obj)
        
    return result_arr
        
            
    

def scrape_chartmill():
    ''' Left halfway because api does not return complete resut '''
    api_url = 'https://www.chartmill.com/chartmill-rest/holding/insider/largest_trans/'
    url = 'https://www.chartmill.com/stock/insider'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    target_table = soup.body
    print(target_table)


  


def scrape_barchart():
    url = 'https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol%2CbaseSymbol%2CbaseLastPrice%2CbaseSymbolType%2CsymbolType%2CstrikePrice%2CexpirationDate%2CdaysToExpiration%2CbidPrice%2Cmidpoint%2CaskPrice%2ClastPrice%2Cvolume%2CopenInterest%2CvolumeOpenInterestRatio%2Cvolatility%2CtradeTime%2CsymbolCode&meta=field.shortName%2Cfield.type%2Cfield.description&orderBy=volumeOpenInterestRatio&orderDir=desc&baseSymbolTypes=stock&between(volumeOpenInterestRatio%2C1.24%2C)=&between(lastPrice%2C.10%2C)=&between(tradeTime%2C2021-02-17%2C2021-02-18)=&between(volume%2C500%2C)=&between(openInterest%2C100%2C)=&in(exchange%2C(AMEX%2CNASDAQ%2CNYSE))=&page=1&limit=100&raw=1'
    r = requests.get(url)
    token = r.headers['X-Amz-Cf-Id']
    print(token)
    result_arr = []
    headers = {
    'authority': 'www.barchart.com',
    'method': 'GET',
    'path': '/proxies/core-api/v1/options/get?fields=symbol%2CbaseSymbol%2CbaseLastPrice%2CbaseSymbolType%2CsymbolType%2CstrikePrice%2CexpirationDate%2CdaysToExpiration%2CbidPrice%2Cmidpoint%2CaskPrice%2ClastPrice%2Cvolume%2CopenInterest%2CvolumeOpenInterestRatio%2Cvolatility%2CtradeTime%2CsymbolCode&meta=field.shortName%2Cfield.type%2Cfield.description&orderBy=volumeOpenInterestRatio&orderDir=desc&baseSymbolTypes=stock&between(volumeOpenInterestRatio%2C1.24%2C)=&between(lastPrice%2C.10%2C)=&between(tradeTime%2C2021-02-17%2C2021-02-18)=&between(volume%2C500%2C)=&between(openInterest%2C100%2C)=&in(exchange%2C(AMEX%2CNASDAQ%2CNYSE))=&page=1&limit=100&raw=1',
    'scheme': 'https',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'laravel_token=eyJpdiI6InBIeDJXUk1SZEFxbmxGRWJmQVRhV3c9PSIsInZhbHVlIjoiK1FzbitTaDVtcGQ2MmNkcTFTVXc3NEQ1WTRDbkQvZERIMUdEeU9HMkU4aHk3L0d0Qm1yN2p1U0Vjd0txNkk1WEdDL0FtSkRVdkp0Q1Joa05RSzlDOXdMUlgxQWJBcE1uQW5oU2FTc1FzbCtVSHlsN0x3SnhIZ2wzTlVpNHoraWora1pxR2ZnMnQxdWJWd3F3aDVtT3hsMisyb3QvWWJwVUd2NExYeWVETTltOGdsa2hibWJocjhLZVROQmhnVTJjZVJnMnpmZmlla3BJUnRSY3kveXpsTWwxZ2YyV0tPL1Q2cUkxSHY2aEtpV1VLTU1uRHVxUmZOT1AzVk9lZW4xTCIsIm1hYyI6Ijg3OWVlNjBmMjc0NGFkZWUyMTBjYzc3MThlY2E0OTMyMjc1OTJkYjA5MzgxMTUyMjVmYTI1NGQxOWU3MDcyMDAifQ%3D%3D; XSRF-TOKEN=eyJpdiI6Imp1V1NoNHNHbVRuUWp3SGRmVUR0dkE9PSIsInZhbHVlIjoiU1VIQ0JCT3B3RDBhM0MxeG5QeGQwRHIrUGQ2am1UNkQyWTluS1RLMmdYWmdzeXFSRzc2Q3ZRUU4zZnVteDNGdCIsIm1hYyI6ImFiOWRhZGE0ZTIxZTg5MDdhZTA4YmU2MmE4NGEzOTc5ZmMxNDY3NzEyNDE3MGFhMzVmODUzN2I0ODk2MTU5NDQifQ%3D%3D; laravel_session=eyJpdiI6IkZ5Q2FmekpiV05xRk40UkZIR0g4Qnc9PSIsInZhbHVlIjoiZWwrSUZKbTFOdHdhelBLU1NaUWdaV1hjTjZYdWtJdzJSK0t1MGFNU2c5OGlZVm14YW1hY2U4WWh5Z1h2czhZUyIsIm1hYyI6ImJmOWQ4ZmYwMzNhMGI1MmNmYWJjNDJiNDQyZmYwZTNjNmJmNGY5ZTFjZGRmMjg2ZDc2YTFlNzJmYWE2ZjYzOWIifQ%3D%3D; market=eyJpdiI6ImpTdGNVb2Y5K1hTa2EzRTcxeFoyNVE9PSIsInZhbHVlIjoiZUVDWS9Uc251YWQ2WGZ0dU5BSmthdz09IiwibWFjIjoiNTc0NDJjM2E2NTRiMGMwNDkzZGU5NzBiZDFlMDA0OTllYWQ4MWRiMzlmYzU4ZjBlY2IxZWJkOGM2NDU5NDc5NCJ9; _gcl_au=1.1.726442713.1613589955; _ga=GA1.2.1408868009.1613589957; _gid=GA1.2.787419582.1613589957; _gat_UA-2009749-51=1; bcFreeUserPageView=0; futures-02242021PageView=1; futures-02242021WebinarClosed=true',
    'pragma': 'no-cache',
    'referer': 'https://www.barchart.com/options/unusual-activity/stocks',
    'sec-ch-ua': '"Chromium";v="89", ";Not\"A\\Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4326.0 Safari/537.36',
    #'x-xsrf-token': 'eyJpdiI6Imp1V1NoNHNHbVRuUWp3SGRmVUR0dkE9PSIsInZhbHVlIjoiU1VIQ0JCT3B3RDBhM0MxeG5QeGQwRHIrUGQ2am1UNkQyWTluS1RLMmdYWmdzeXFSRzc2Q3ZRUU4zZnVteDNGdCIsIm1hYyI6ImFiOWRhZGE0ZTIxZTg5MDdhZTA4YmU2MmE4NGEzOTc5ZmMxNDY3NzEyNDE3MGFhMzVmODUzN2I0ODk2MTU5NDQifQ=='
    'x-xsrf-token': token
    }
    r = requests.get(url, headers=headers)
    data = r.json()['data']
    
    for item in data:
        obj = {}
        symbol = item['symbol']
        price = item['baseLastPrice']
        type = item['symbolType']
        strike = item['strikePrice']
        exp_date = item['expirationDate']
        dte = item['daysToExpiration']
        bid = item['bidPrice']
        midpoint = item['midpoint']
        ask = item['askPrice']
        last = item['lastPrice']
        volume = item['volume']
        open_int = item['openInterest']
        vol_oi = item['volumeOpenInterestRatio']
        last_trade = item['tradeTime']
        
        obj['Symbol'] = symbol
        obj['Price'] = price
        obj['Type'] = type
        obj['Strike'] = strike
        obj['Expiration_Date'] = exp_date
        obj['Dte'] = dte
        obj['Bid'] = bid
        obj['Midpoint'] = midpoint
        obj['Ask'] = ask
        obj['Last'] = last
        obj['Volume'] = volume
        obj['Open_Interest'] = open_int
        obj['VOL_OI'] = vol_oi
        obj['Last_Trade'] = last_trade
        
        result_arr.append(obj)
        
    return result_arr
        
        
        
        
def scrape_stockmarket_mba():
    url = 'https://stockmarketmba.com/listofshellcompanies.php'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    soup = BeautifulSoup(str(soup.table), 'html.parser')
    target_table = soup.findAll('tr')[1:-1]
    result_arr = []
    
    for row in target_table:
        #print(row)
        #break
        obj = {}
        for index, td in enumerate(row.findAll('td')):
            if index == 0:
                obj['Symbol'] = td.text.strip()
                
            elif index == 1:
                obj['Name'] = td.text.strip()
                
            elif index == 2:
                obj['Ipo_Date'] = td.text.strip()
                
            elif index == 3:
                obj['Market_Cap'] = td.text.strip()
                
            elif index == 4:
                obj['Merger_Pending'] = td.text.strip()
                
            elif index == 5:
                obj['Leverage_Factor'] = td.text.strip()
                
            elif index == 6:
                obj['Momentum_Factor_Ten'] = td.text.strip()
                
            elif index == 7:
                obj['Momentum_Factor_Two_Hunderd'] = td.text.strip()
                
            elif index == 8:
                obj['Last_Close_Price'] = td.text.strip()
                
            elif index == 9:
                obj['Shares_Outstanding'] = td.text.strip()
                
            elif index == 10:
                obj['Average_Trading_Volume'] = td.text.strip()
                
            elif index == 11:
                obj['%Traded'] = td.text.strip()
                
            elif index == 12:
                obj['Action'] = td.text.strip()
                
        result_arr.append(obj)
        
    return result_arr
            
                
                
app = Flask(__name__)


@app.route('/stockbeep/down')
def stockbeep_down():
    result = scrape_stockbeep(mode='down')
    return jsonify(result)
    
    
    
    
@app.route('/stockbeep/up')
def stockbeep_up():
    result = scrape_stockbeep(mode='up')
    return jsonify(result)
    
    
    
    
@app.route('/stockbeep/trending')
def stockbeep_trending():
    result = scrape_stockbeep(mode='trending')
    return jsonify(result)
    
    
    
@app.route('/stockbeep/unusual-vol')
def stockbeep_unusualvol():
    result = scrape_stockbeep(mode='unusual-vol')
    return jsonify(result)
    
        
@app.route('/stockbeep/downtrend')
def stockbeep_downtrend():
    result = scrape_stockbeep(mode='downtrend')  
    return jsonify(result)  

 


@app.route('/stockmarket-mba')
def mba():
    result = scrape_stockmarket_mba()
    return jsonify(result)


     
        
if __name__ == '__main__':
    app.run(debug=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        







  

#scrape_stockbeep(mode='unusual-vol')
#scrape_marketbeat()
#scrape_barchart()
#print(scrape_stockmarket_mba())










