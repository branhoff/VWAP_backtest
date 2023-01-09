import numpy as np

def calc_vwap(price, volume, d):
    """Return the VWAP anchored d days back"""
    vwap = np.zeros(len(price))
    for i in range(d, len(price)):
        lb = i - d  # lower bound
        ub = i + 1  # upper bound
        vwap[i] = (price[lb:ub] * volume[lb:ub]).sum() / volume[lb:ub].sum()
    return vwap

def calc_smap(price, d):
    """Return the SMAP anchored d days back"""
    smap = np.zeros(len(price))
    for i in range(d, len(price)):
        lb = i - d  # lower bound
        ub = i + 1  # upper bound
        smap[i] = np.sum(price[lb:ub]) / (d + 1)
    return smap
