VWAP Backtest

Project intends to test whether a stock's Volume Weighted Average Price serves as a better indicator of a asset's future price than the Simple Average Price with an identical lookback range.

## Setup
Note that the version of Pandas module `from pandas.plotting import _converter` does not play well with Python versions greater that `3.7`.

Run the `install_dependencies.sh` script from the project root directory to create a virtual environment and install the necessary packages.

Currently, we are using Alpha Vantage's Endpoints to collect data.

See: https://rapidapi.com/alphavantage/api/alpha-vantage/endpoints

Sign up for an account and retrieve an API key from Alpha Vantage. Once you have subscribed to the Stock Time Series `TIME_SERIES_DAILY` you can pull stock historical daily price data.

Create a `.env` file at the root of the project directory and add an environment variable `X_RAPID_API_KEY=your_api_key`

## Rerunning the analysis `vwap_vs_smap_equity.ipynb`
If you wish to rerun the jupyter notebook cells, be sure that your notebook's kernel is appropriately pointed to the virtual environment `.venv` we created.

## TODOs for Developers
1. Needs to be more dynamic and pull data directly from data provider's API

2. Should probably show graph of return growth for the the buy/hold, VWAP, and SMAP strategy

3. What are the two plot graphs trying to communicate?

4. Why does the plot of the line on the second chart (strategy value vs. benchmark value) not seem to fit the data points

5. We should introduce and better explain what we hope to achieve by this analysis

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
