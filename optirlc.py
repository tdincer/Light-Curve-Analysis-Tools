import numpy as np
import pandas as pd

_author_ = 'Tolga Dincer'
_email_ = ['tolga.dincer@yale.edu', 'tolgadincer@gmail.com']
_maintainer_ = 'Tolga Dincer'
_version_ = '17.07.07'
_laststableversion_ = '17.07.07'


def binning(data, vTime, vMag, vMage, binsize, *vfilename):
    """
    Takes the time series data and bins it with a given binsize.
    :param data (pd.DataFrame): pandas DataFrame which contains the time series.
    :param vTime (str): name of the time variable in the dataframe
    :param vMag (str): name of the magnitude variable in the dataframe.
    :param vMage (str): name of the magnitude error variable in the data frame.
    :param binsize (float): binsize in units of the time given in time series data.
    :param vfilename (str): file name, if the result will be written to a file.
    :return: pandas DataFrame which contains only time, magnitude, and magnitude error.
    """

    time = np.array([])
    mag = np.array([])
    err = np.array([])

    inittime = np.floor(min(data[vTime]))
    finaltime = np.ceil(max(data[vTime]))

    datalen = len(data)

    while inittime < finaltime:
        inittime = np.floor(inittime)
        endday = inittime + 1
        expr = vTime + ' >= ' + str(inittime) + ' & ' + vTime + '<'+str(endday)

        datas = data.query(expr)

        subinittime = min(datas[vTime])-0.000001
        subendtime = subinittime + binsize

        while subinittime < endday:
            exprs = vTime + ' >= ' + str(subinittime) + ' & ' + vTime + ' < '+str(subendtime)
            datass = datas.query(exprs)
            datasslen = len(datass)
        
            time = np.append(time, np.mean(datass[vTime]))
            ma = datass[vMag].mean()
            er = np.sqrt(np.sum(datass[vMage]**2.))/len(datass)
            mag = np.append(mag, ma)
            err = np.append(err, er)

            if max(datass.index) < max(datas.index):
                subinittime = datas[vTime].loc[max(datass.index)+1] - 0.000001
                subendtime = subinittime + binsize
            else:
                break

        if max(datas.index)+1 < datalen:
            inittime = data[vTime].loc[max(datas.index)+1]-0.000001
        else:
            break

    binneddata = {'time': time, 'mag': mag, 'err': err}
    binneddataframe = pd.DataFrame(data = binneddata)

    print vfilename[0]

    if len(vfilename) > 0:
        binneddataframe.to_csv(vfilename[0], index=False)

    return binneddataframe