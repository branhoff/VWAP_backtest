import numpy as np

def calc_vwap(price, volume, period_lookback):
    """
    Calculates the volume-weighted average price (VWAP) for a given period of time.
    The VWAP is calculated by taking the sum of the product of each price and volume over a given period, 
    and dividing by the sum of the volume over that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        volume (numpy.ndarray): A list or array of volumes, corresponding to the prices.
        period_lookback (int): The number of days to look back when calculating VWAP.
        
    Returns:
        numpy.ndarray: An array of VWAP values, one for each day in the input period.
    """
    vwap = np.zeros(len(price))
    for i in range(period_lookback, len(price)):
        lb = i - period_lookback  # lower bound
        ub = i + 1  # upper bound
        vwap[i] = (price[lb:ub] * volume[lb:ub]).sum() / volume[lb:ub].sum()
    return vwap

def calc_smap(price, period_lookback):
    """
    Calculates the simple moving average price (SMAP) for a given period of time.
    The SMAP is calculated by taking the sum of prices over a given period, and dividing by the number of days in that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        period_lookback (int): The number of days to look back when calculating SMAP.
        
    Returns:
        numpy.ndarray: An array of SMAP values, one for each day in the input period.
    """
    smap = np.zeros(len(price))
    for i in range(period_lookback, len(price)):
        lb = i - period_lookback  # lower bound
        ub = i + 1  # upper bound
        smap[i] = np.sum(price[lb:ub]) / (period_lookback + 1)
    return smap

def set_signal(metric, price, lookback):
    """
    Set the signal array based on the comparison of the price and metric arrays.
    If the price is greater than the metric and the index is greater than or equal to lookback, 
    the signal will be set to 1. Otherwise, the signal will be set to 0.
    
    Parameters:
        metric (numpy.ndarray): The metric array to compare against
        price (numpy.ndarray): The price array to compare with
        lookback (int): The minimum index to set signal
        
    Returns:
        numpy.ndarray: An array of signals
    """
    signal = np.zeros(len(price)+1)
    condition = (price > metric) & (np.arange(len(price)) >= lookback) & (np.arange(len(price)) < len(price))
    signal[1:len(price)+1] = np.where(condition, 1, 0)
    return signal

def set_value(signal,openprice):
    """
    Set the value array based on the signal array and the openprice array
    
    Parameters:
        signal (numpy.ndarray): An array of signals
        openprice (numpy.ndarray): The openprice array
        
    Returns:
        numpy.ndarray: An array of values
    """
    value = np.ones(len(signal))
    delta = (openprice[1:] - openprice[:-1])/(openprice[:-1])
    value[1:] = value[:-1]*(1 + signal[:-1]*delta)
    return value
