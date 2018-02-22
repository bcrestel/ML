import pandas as pd

def loadfile(filenameIBM):
    df = pd.read_csv(filenameIBM, header=None, skiprows=1, 
                     delim_whitespace=True,
        names = ['date', 'MOBIL', 'IBM', 'WEYER', 'CITCRP', 'MARKET', 'RKFREE'])
    df.date = pd.to_datetime(
            df.date.apply(lambda x: str(int(x)) + '-' + str(int(100*(x-int(x))+1))))
    return df

def compounded(df):
    """ convert simple returns into compounded returns """
    return (1.0 + df).cumprod() - 1.0

if __name__ == "__main__":
    df = loadfile('stocksIBMandCo.txt')
    df['MARKET_cpd'] = compounded(df.MARKET)
    df.MARKET_cpd.plot()    