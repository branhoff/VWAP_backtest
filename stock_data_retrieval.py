import json
import requests
import os
from environs import Env

from bs4 import BeautifulSoup
env = Env()
env.read_env() # read .env file, if it exists. Needed to securely retrieve API_KEY(s)


def get_stocks_from_sp500() -> dict:
    """
    Scrapes the S&P 500 constituents tickers and name from the wikipedia page and returns them as a dictionary
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    # parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", id="constituents")
    rows = table.select("tr") # select all the rows within that table
    
    stocks = {}
    for row in rows:
        cells = row.select("td") # select all the cells within the current row
        if len(cells)>0: # check that the row has cells (to skip the header row)
            ticker = cells[0].text.strip()
            security = cells[1].text.strip()
            stocks[ticker] = security
    return stocks



def get_price_json(ticker: str) -> dict:
    """
    This function takes a ticker symbol as an input, and returns the daily time series of the stock price in json format.

    Parameters:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A json containing the daily time series of the stock price.

    """

    # current API is https://rapidapi.com/alphavantage/api/alpha-vantage/endpoints

    url = "https://alpha-vantage.p.rapidapi.com/query"
    
    headers = {
    "X-RapidAPI-Key": os.getenv("X_RAPID_API_KEY"),
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    querystring = {"function": "TIME_SERIES_DAILY",
                   "symbol": ticker,
                   "outputsize": "compact",
                   "datatype": "json"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.status_code)
    return response.json()

def save_json(json_data: dict, file_name: str, file_path: str) -> None:
    """
    This function takes a json data, and file name, and file path as inputs, and saves the json data to a local directory with the given file name and path.

    Parameters:
        json_data (dict): The json data that needs to be saved.
        file_name (str): The desired name of the file.
        file_path (str): The directory where the file should be saved.

    Returns:
        None: The function saves the json data to a local directory, and prints the message after saving the json file.
    """

    with open(f"{file_path}/{file_name}.json", "w") as outfile:
        json.dump(json_data, outfile)
    print(f"{file_name}.json saved in {file_path}")

def main() -> None:
    """
    This function takes a list of ticker symbols, it calls the get_price method for each ticker, and saves the json data to a local directory.

    Returns:
        None: The function saves the json data of each ticker to a local directory, and prints the message after saving the json file.

    """

    stocks = get_stocks_from_sp500()
    print(stocks)
    # tickers = ["MSFT", "BAC", "AAPL"]
    # for ticker in tickers:

    # 	price_json = get_price_json(ticker)
    # 	save_json(price_json, ticker, "data/")

if __name__ == "__main__":
    main()