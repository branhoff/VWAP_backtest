# VWAP Backtest

Project intends to test whether a stock's Volume Weighted Average Price serves as a better indicator of a asset's future price than the Simple Average Price with an identical lookback range.

## Setup
Note that the version of Pandas module `from pandas.plotting import _converter` does not play well with Python versions greater than `3.7.x`. Be sure to use [`pyenv`](https://github.com/pyenv/pyenv) or some other python version manager to ensure you're using a version of Python < `3.8`.

1. Run the `install_dependencies.sh` script from the project root directory to create a virtual environment and install the necessary packages.

2. Sign up for an account [Alpha Vantage's Endpoints](https://rapidapi.com/alphavantage/api/alpha-vantage/) to collect data.

3. Once you have subscribed to the Stock Time Series `TIME_SERIES_DAILY` you can pull stock historical daily price data.

4. Create a `.env` file at the root of the project directory and add an environment variable `X_RAPID_API_KEY=your_api_key`

5. Update stock data by running the `stock_data.py` module.
    - Be wary, on the basic plan you can only make a max of 500 calls and only 5 per 60 seconds. After testing, I'm finding it's more like 3 calls every 65 seconds. It will take two days to completely refresh the SP500 and you'll need to let the `stock_data.py` script run for some time.

## Rerunning the analysis `vwap_vs_smap_equity.ipynb`
If you wish to rerun the jupyter notebook cells, be sure that your notebook's kernel is appropriately pointed to the virtual environment `.venv` we created with the `install_dependencies` script.

## TODOs
1. ~~Needs to be more dynamic and pull data directly from data provider's API~~

1. Consider using StockData as a wrapper that calls a AlphaVantage class to decouple and make refactoring easier in the future if the API changes

1. in the metadata fields of the stock price jsons, we should add fields on what relevant index it is related to. In the future, if we expand to cryptocurrencies, we'll need to add a field for asset type as well

2. Should probably show graph of return growth for the the buy/hold, VWAP, and SMAP strategy

3. What are the two plot graphs trying to communicate?

3. Need unit tests for the `metrics.py` to ensure confidence

4. Why does the plot of the line on the second chart (strategy value vs. benchmark value) not seem to fit the data points

5. Enhance introduction and purpose of analysis between VWAP and SMAP

7. Consider using backtrader or pyfolio packages to simplify calculations

9. Error discovered in the set_singal function. Signal is being set the day of the intiation. It needs to be added to the
   next row and be calculated with delay

10. Results of SMAP and VWAP seem much too similar... I would expect VWAP to be much slower than the SMAP

11. Look into using the module Seaborn for histograms - https://seaborn.pydata.org/tutorial/distributions.html

12. Need to identify large outlier created with the S&P 500 Data.
    I think this is being caused by a short timefram for the test. Need to write a script that will only capture stocks with data at least
    back to 2010 (or whenever start date is)

13. Consider including R^2 in Gaussian curve

14. I'm attempting to build out the portion of the code that will cycle through different lookbacks and repeat the calculations
in the original code. Problem is that storing that data is messy and not very adaptable. Need to research preferred way to write code so that it can flexibly store additional and new variable names without being manually hard coded in. Talk to people at RMOTR or chipy to find common solution to problem.
