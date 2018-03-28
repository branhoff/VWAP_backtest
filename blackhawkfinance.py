import requests
import pandas   as pd
import datetime as dt
import numpy    as np
import matplotlib.pyplot as plt
import time     as modtime


def get_intraday_data( stock    = 'SPY'   ,
                       period   = '60'    ,
                       days     = '1'      ):
    """ Get the historical intraday data of a stock from google finance 

        * stock    - ticker symbol
        * period   - time in seconds between data points
        * days     - number of days to go back (30ish max)

        Note that some minute data is missing from google.

        Return in a data frame.                                         """
    

    # setup the web query
    # ------------------------------------------------------------------- #
    rooturl = 'https://www.google.com/finance/getprices'
    query   = '?q={stock}&i={period}&p={days}d'\
                    .format(
                    stock=stock, 
                    period=period, 
                    days=days)
    url     = rooturl + query
    r = requests.get(url, headers={'Accept-Encoding':'gzip,deflate'})
    data = r.content.splitlines()
    # ------------------------------------------------------------------- #


    # Put the data in a pandas dataframe and return
    # ------------------------------------------------------------------- #
    # get the column headers and time stamp information. Then truncate headers
    i = 0
    for row in data:
        if 'COLUMNS' in row:
            columns = row.split('=')[1].split(',')
        if row[0] == 'a':
            data = data[i:]
            break    
        i += 1

    # split the data into columns
    tmp  = data
    data = []
    # process the rows
    for row in tmp:
        # convert the time interval to seconds and add to start time
        if (row.split(',')[0][0] == 'a' ):
            start_time = row.split(',')[0]
            start_time = dt.datetime.fromtimestamp(int(start_time[1:]))
            tdelta = 0
        else:
            tdelta = int(row.split(',')[0])
        # append the row to the data
        curtime = start_time + tdelta*dt.timedelta(0,int(period))
        data.append( [curtime] + [float(item) for item in row.split(',')[1:]] )

    # assign to a pandas data frame
    df = pd.DataFrame(data,columns=columns)

    # also return the average price
    df['PRICE'] = (df['HIGH'] + df['LOW'])/2

    # return the data frame
    return df
    # ------------------------------------------------------------------- #


def get_historical_data( stock     = 'SPY',
                         startdate = None ,
                         enddate   = None ,
                         dropnan   = False,
                         source    = 'GOOGLE' ):
    """ Get the historical daily data of a stock from google finance or yahoo finance

        * stock     - ticker symbol
        * startdate - the start date as MMDDYYYY (as an integer)
        * enddate   - the start date as MMDDYYYY (as an integer)
        * dropnan   - drop any days where, for whatever reason, we do not have some datapoint
        * source    - get the data from either GOOGLE or YAHOO

        Note that some minute data is missing from google.

        Return in a data frame.                                         """
    

    # Routine to get data from google
    if source == 'GOOGLE':
        df = get_historical_google( stock, startdate, enddate )
    elif source == 'YAHOO':
        df = get_historical_yahoo( stock, startdate, enddate )
    else:
        print("Error. get_historical_data source {} is unknown".format(source))
        return 0

    
    # calculate and return the average price
    df['AVEPRICE'] = (df['HIGH'] + df['LOW'])/2

    # drop any columns that have nan, if requested
    if dropnan: df = df.dropna()
    
    # send the data back
    return df.reset_index(drop=True)
        
    
def get_historical_google( stock, startdate, enddate ):
    """ Get the historical daily data of a stock from google finance

        * stock     - ticker symbol
        * startdate - the start date as MMDDYYYY (as an integer)
        * enddate   - the start date as MMDDYYYY (as an integer)

        Note that some minute data is missing from google.

        Return in a data frame.                                         """
    
    
    # set default start and end date, if none given
    # ------------------------------------------------------------------- #
    # the start date
    if startdate == None:
        sdate  = dt.datetime.now()
    else:
        sdate     = dt.date(int(startdate[4:8]), int(startdate[0:2]), int(startdate[2:4]) )
    # format for the google query
    smonth = sdate.strftime('%b')
    sday   = sdate.strftime('%d')
    syear  = sdate.strftime('%Y')

    # the end date
    if enddate == None:
        edate  = dt.datetime.now()
    else:
        edate   = dt.date(int(enddate[4:8]), int(enddate[0:2]), int(enddate[2:4]) )
    # format for the google query
    emonth = edate.strftime('%b')
    eday   = edate.strftime('%d')
    eyear  = edate.strftime('%Y')
    # ------------------------------------------------------------------- #


    # setup the google web query
    # ------------------------------------------------------------------- #
    rooturl = 'https://finance.google.com/finance/historical'
    # make the query
    query     = '?q={stock}&startdate={smonth}+{sday}%2C+{syear}&enddate={emonth}+{eday}%2C+{eyear}&output=csv'\
                    .format(stock    = stock,
                            smonth   = smonth,
                            sday     = sday,
                            syear    = syear,
                            emonth   = emonth,
                            eday     = eday,
                            eyear    = eyear)
    url = rooturl + query
    print("Getting historical data from: {}".format(url))
    r = requests.get(url)
    data = r.content.decode('utf-8').splitlines()
    # ------------------------------------------------------------------- #

    # Parse data into pandas data frame and return
    # ------------------------------------------------------------------- #
    # get the column headers and time stamp information. Then truncate headers
    columns = data[0][1:].split(',')
    # make column labels uppercase to have same format as intraday
    columns = [ col.upper() for col in columns ]
    # get rid of header column
    data    = data[1:]
    # split the data into columns
    tmp  = data
    data = []
    time = []
    for row in tmp:
        # get the date for the current row
        curdate = row.split(',')[0]
        # convert data to floats - some volume data isnt available and is 
        # reported as '-', so here I set to nan
        line = []
        for item in row.split(',')[1:]:
            try:
                line.append(float(item))
            except:
                line.append(np.nan)
        # append the date and float values to the data list
        data.append([curdate] + line)

    # assign to a pandas array
    df = pd.DataFrame(data,columns=columns)

    # return the data frame ordered from oldest to newest
    return df.iloc[::-1]
    # ------------------------------------------------------------------- #

    
    
def get_historical_yahoo( stock, startdate, enddate ):
    """ Get the historical daily data of a stock from yahoo finance

        * stock     - ticker symbol
        * startdate - the start date as MMDDYYYY (as an integer)
        * enddate   - the start date as MMDDYYYY (as an integer)

        Return in a data frame.                                         """
    
    
    # set default start and end date, if none given
    # ------------------------------------------------------------------- #
    # the start date
    if startdate == None:
        sdate  = dt.datetime.now()
    else:
        sdate     = dt.date(int(startdate[4:8]), int(startdate[0:2]), int(startdate[2:4]) )
        
    # convert to timestamp for yahoo query
    sdate = int(modtime.mktime( sdate.timetuple() ))
    
    # the end date
    if enddate == None:
        edate  = dt.datetime.now()
    else:
        edate   = dt.date(int(enddate[4:8]), int(enddate[0:2]), int(enddate[2:4]) )

    # convert to timestamp for yahoo query
    edate = int(modtime.mktime( edate.timetuple() ))
    # ------------------------------------------------------------------- #


    # setup the yahoo web query
    # ------------------------------------------------------------------- #
    # first we have to get a cookie crumb, otherwise yahoo wont let us access the data #
    #                          ** THIS MAY BREAK EASILY, SO BEWARE **
    url = 'https://finance.yahoo.com/quote/{stock}/history/?period1={sdate}&period2={edate}&interval=1d&filter=history&frequency=1d'.format(stock=stock,sdate=sdate,edate=edate)
    r   = requests.get(url, headers={'Accept-Encoding':'gzip,deflate'})
    for item in r.content.decode('utf-8').split(','):
        if 'CrumbStore' in item:
            crumb = item.split(":")[2].split('"')[1].decode('unicode-escape')
    cookie = r.cookies
    
    # now that we have to cookie and crumb, yahoo will let us download the data
    rooturl = 'https://query1.finance.yahoo.com/v7/finance/download/{stock}'.format(stock=stock)
    query   = '?period1={sdate}&period2={edate}&interval=1d&events=history&crumb={crumb}'\
                    .format(sdate = sdate,
                            edate = edate,
                            crumb = crumb)
    url = rooturl + query
    print("Getting historical data from: {}".format(url))
    r = requests.get(url,cookies=cookie)
    data = r.content.decode('utf-8').splitlines()
    # ------------------------------------------------------------------- #

    # Parse data into pandas data frame and return
    # ------------------------------------------------------------------- #
    # get the column headers and time stamp information. Then truncate headers
    columns = data[0][:].split(',')
    # make column labels uppercase to have same format as intraday
    columns = [ col.upper() for col in columns ]
    # get rid of header column
    data    = data[1:]
    # split the data into columns
    tmp  = data
    data = []
    time = []
    for row in tmp:
        # get the date for the current row
        curdate = row.split(',')[0]
        # convert data to floats - some volume data isnt available and is 
        # reported as '-', so here I set to nan
        line = []
        for item in row.split(',')[1:]:
            try:
                line.append(float(item))
            except:
                line.append(np.nan)
        # append the date and float values to the data list
        data.append([curdate] + line)

    # assign to a pandas array
    df = pd.DataFrame(data,columns=columns)

    # return the data frame ordered from oldest to newest
    return df
    return df.iloc[::-1].reset_index(drop=True)
    # ------------------------------------------------------------------- #

    
    
def plot(y,labels=None,title=None):
    """Plot y values, can be passed as a list to plot multiple curves at once"""
    
    plt.figure(1)

    # Handle if a list of y values is passed, else only a single array
    if isinstance(y, list):
        for i in range(len(y)):
            # get x values
            ys = y[i]
            xs = np.linspace( 0, len(ys), num=len(ys))
            if labels:
                plt.plot(xs, ys, label=labels[i])
            else:
                plt.plot(xs, ys )
    else:
        ys = y
        xs = np.linspace( 0, len(ys), num=len(ys))
        if labels:
            plt.plot(xs, ys, label=labels)
        else:
            plt.plot(xs, ys)

    if labels:
        plt.legend()
    if title:
        plt.title(title)
    plt.show()
    plt.close()

def get_vwap(volume, price):
    """Calculate the vwap from a volume and price array"""

    vwap =  (volume*price).cumsum()/volume.cumsum()
    return vwap

def get_value( signal, price ):
    """Return the value of investment based on price and buy/sell signal. 
    
    WARNING: Be careful that you index the signal correctly. The signal in index i should be calculated on data based on any data before that in row i, but not on the data in i. Otherwise, this will lead to overly generous returns. This routine assumes that you buy the stock the instant the market opens on the next day. It may be beneficial to pass the opening day price rather than the average price for the day. Then you assume you make all trades as soon as possible on the current day.
    
    I think this correctly handles the signal, as it rolls it forward one day
    """

    # calculate the percent change from yesterday's price
    delta = np.divide( price - np.roll(price,1), np.roll(price,1)*1. )
    delta[0] = 0.  # we dont know the change on the first day, so just set to none
    
    # initialize value
    value = np.zeros(len(delta))
    value[0] = 1. # assume our starting value is 1

    # align the signals -- I think this is correct -- check with brandon
    signal = np.roll(signal,1)
    signal[0] = 0
    
    # caluclate the value of the stock
    for n in range(1, len(delta)):
        value[n] = (1. + signal[n]*delta[n]) * value[n-1]
   
    return value
