import numpy as np

def calc_vwap(price, volume, period_lookback):
    """
    Calculates the volume-weighted average price (VWAP) for a given period of time.
    The VWAP is calculated by taking the sum of the product of each price and volume over a given period, 
    and dividing by the sum of the volume over that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        volume (numpy.ndarray): A list or array of volumes, corresponding to the prices.
        period_lookback (int): The number of units to look back when calculating VWAP.
        
    Returns:
        numpy.ndarray: An array of VWAP values, one for each unit in the input period.
    """
    vwap = np.zeros(len(price))
    for i in range(period_lookback, len(price)):
        lb = i - period_lookback  # lower bound
        ub = i + 1  # upper bound
        volume_sum = volume[lb:ub].sum()
        if volume_sum > 0:
            vwap[i] = (price[lb:ub] * volume[lb:ub]).sum() / volume_sum
        else:
            vwap[i] = np.nan
    return vwap

def calc_vwap_fast(price, volume, period_lookback):
    """
    Calculates the volume-weighted average price (VWAP) for a given period of time.
    Uses numpy methods instead of python loops for a much more efficient calculation.
    The VWAP is calculated by taking the sum of the product of each price and volume over a given period, 
    and dividing by the sum of the volume over that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        volume (numpy.ndarray): A list or array of volumes, corresponding to the prices.
        period_lookback (int): The number of units to look back when calculating VWAP.
        
    Returns:
        numpy.ndarray: An array of VWAP values, one for each unit in the input period.
    """
    # Calculate product of price and volume
    price_volume = price * volume
    # Use convolve to get the rolling sum of product of price and volume and volume array
    price_volume_conv = np.convolve(price_volume, np.ones(period_lookback+1), mode='valid')
    # Use convolve to get the rolling sum of volume
    volume_conv = np.convolve(volume, np.ones(period_lookback+1), mode='valid')
    # Create a mask to check if the volume sum is greater than 0
    mask = volume_conv > 0
    # Initialize the vwap array
    vwap = np.zeros(len(price))
    # Use the mask to check if volume sum is greater than zero, if it is, proceed with the division and store the result in vwap array, otherwise store NaN
    vwap[period_lookback:] = np.where(mask, price_volume_conv / volume_conv, np.nan)
    return vwap

def calc_smap(price, period_lookback):
    """
    Calculates the simple moving average price (SMAP) for a given period of time.
    The SMAP is calculated by taking the sum of prices over a given period, and dividing by the number of units in that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        period_lookback (int): The number of units to look back when calculating SMAP.
        
    Returns:
        numpy.ndarray: An array of SMAP values, one for each unit in the input period.
    """
    smap = np.zeros(len(price))
    for i in range(period_lookback, len(price)):
        lb = i - period_lookback  # lower bound
        ub = i + 1  # upper bound
        smap[i] = np.sum(price[lb:ub]) / (period_lookback + 1)
    return smap

def calc_smap_fast(price, period_lookback):
    """
    Calculates the simple moving average price (SMAP) for a given period of time.
    Uses numpy methods instead of python loops for a much more efficient calculation.
    The SMAP is calculated by taking the sum of prices over a given period, and dividing by the number of units in that period.
    
    Parameters:
        price (numpy.ndarray): A list or array of prices.
        period_lookback (int): The number of units to look back when calculating SMAP.
        
    Returns:
        numpy.ndarray: An array of SMAP values, one for each unit in the input period.
    """
    # Use convolve to get the rolling sum of prices
    price_conv = np.convolve(price, np.ones(period_lookback+1), mode='valid')
    # Initialize the smap array
    smap = np.zeros(len(price))
    # Calculate the smap using the rolling sum of prices and store the result in smap array
    smap[period_lookback:] = price_conv / (period_lookback + 1)
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


def main():
    import timeit

    price = np.random.random(10000)
    volume = np.random.random(10000)

    print(calc_vwap(price, volume, 100))
    print(calc_vwap_fast(price, volume, 100))
    print()
  
    print(calc_smap(price, 100))
    print(calc_smap_fast(price, 100))
    print()


if __name__ == "__main__":
    main()
