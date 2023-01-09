import requests
import os
from environs import Env

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"function":"TIME_SERIES_DAILY","symbol":"MSFT","outputsize":"compact","datatype":"json"}

env = Env()
env.read_env() # read .env file, if it exists

headers = {
	"X-RapidAPI-Key": os.getenv("X_RAPID_API_KEY"),
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)