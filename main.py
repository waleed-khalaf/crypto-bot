import datetime
import os
from datetime import datetime as dt
from coinbase.wallet.client import Client


api_endpoint = "https://api.coinbase.com/v2/"
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]

# Creating Client object to connect to coinbase API
client = Client(API_KEY, API_SECRET)


def get_balance_total() -> str:
    """Uses coinbase API to get information on holdings in fiat and crypto wallets and displays the amount of each
    for each wallet, in GBP, then sums the values and displays the total amount. """
    total = 0
    message = []
    accounts = client.get_accounts().data
    for wallet in accounts:
        message.append(str(wallet['name']) + ' ' + str(wallet['native_balance']))
        value = str(wallet['native_balance']).replace('GBP', '')
        total += float(value)

    message.append('Total Balance: ' + str(total) + ' GBP')
    return '\n'.join(message)


# Creating datetime Object in format YYYY-MM-DD for api call
def get_last_weeks_prices(cryptocurrency) -> dict:
    """Uses coinbase `.get_spot_price` method with the dates of the last week and returns the spot price for BTC in
    GBP for those dates as a dictionary."""
    # TODO : Change doc string to reflect change in variable 'cryptocurrency'
    today = dt.today()
    # Finds the past n dates to make a dictionary of prices on those specific dates to calculate 50 SMA.
    past_weeks_dates = [(today - datetime.timedelta(i)).strftime("%Y-%m-%d") for i in range(1, 51)]
    spot_price_dict = {date: client.get_spot_price(date=date, currency_pair=f"{cryptocurrency}-GBP")["amount"] for date
                       in
                       past_weeks_dates}

    return spot_price_dict

# TODO: Build coin class that takes in the name of the cryptocurrency and then inherits from the coinbase class to
#  have necessary functionality to be able to get price of coin relative to GBP
