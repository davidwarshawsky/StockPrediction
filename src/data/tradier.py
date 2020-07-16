import requests
from urllib.error import HTTPError

# Tradier DOES NOT provide historic options data

api_keys = ['Bearer 0OTsK4NA7XzXXE3mSk05sJls9WAj', 'Bearer ASSXgYl15sWHMjDwDSs05myw9N26']


def get_option_expirations(symbol):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/expirations',

                            params={'symbol': symbol, 'includeAllRoots': 'true', 'strikes': 'true'},

                            headers={'Authorization': api_keys[0], 'Accept': 'application/json'}
                            )
    if response.status_code != 200:
        raise HTTPError("Expected status code: 200 Actual status code: {} with reason {}".format(
            response.status_code, response.reason))

    expirations_dict = response.json()['expirations']
    if expirations_dict is None:
        message = "Check symbol and api key, got symbol: <{}> and api_key <{}>".format(symbol, api_keys[0])
        raise ValueError(message)

    expirations_dict = expirations_dict['expiration']
    dates_list = [x['date'] for x in expirations_dict]
    strikes_list = [x['strikes']['strike'] for x in expirations_dict]
    return dates_list, strikes_list

def get_strikes(symbol:str, date:str) -> list:
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/strikes',
                            params={'smbol': symbol, 'expiration': date},
                            headers={'Authorization': api_keys[0], 'Accept': 'application/json'}
                            )
    if response.status_code != 200:
        raise HTTPError("Expected status code: 200 Actual status code: <{}> with reason <{}>".format(
            response.status_code, response.reason))
    strikes_dict = response.json()
    if strikes_dict['strikes'] is None:
        message = "Check symbol and date, got symbol: <{}> and date <{}>".format(symbol, date)
        raise ValueError(message)
    strikes_list = strikes_dict['strikes']['strike']
    return strikes_list

def get_option_chains(symbol:str,date:str):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                            params={'symbol': symbol, 'expiration': date, 'greeks': 'true'},
                            headers={'Authorization': api_keys[0], 'Accept': 'application/json'}
                            )
    if response.status_code != 200:
        raise HTTPError("Expected status code: 200 Actual status code: <{}> with reason <{}>".format(
            response.status_code, response.reason))
    chains_dict = response.json()['options']
    if chains_dict is None:
        message =  "Check symbol and date, got symbol: <{}> and date <{}>".format(symbol, date)
        raise ValueError(message)
    chains_list = chains_dict['option']
    return chains_list

if __name__ == '__main__':
    dates,strikes = get_option_expirations("GOOG")
    chains = get_option_chains("GOOG",dates[0])


