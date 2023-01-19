import json
import requests
import os
from environs import Env

env = Env()
env.read_env() # read .env file, if it exists


def get_price_json(ticker: str) -> dict:
	"""
    This function takes a ticker symbol as an input, and returns the daily time series of the stock price in json format.

    Parameters:
    	ticker (str): The stock ticker symbol.

    Returns:
    	json: A json containing the daily time series of the stock price.

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
	tickers = ["MSFT", "BAC", "AAPL"]
	for ticker in tickers:

		price_json = get_price_json(ticker)
		save_json(price_json, ticker, "data/")

if __name__ == "__main__":
	main()