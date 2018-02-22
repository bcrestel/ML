import pandas as pd

def loadfile():
    df = pd.read_csv('stocksIBMandCo.txt', header=None, skiprows=1, 
                     delim_whitespace=True,
        names = ['date', 'MOBIL', 'IBM', 'WEYER', 'CITCRP', 'MARKET', 'RKFREE'])
    df.date = df.date.astype(str)
    df.date = pd.to_datetime(df.date.str.split('.').str.join('-'))
    return df

def compounded(df):
    return (1.0 + df).cumprod() - 1.0

if __name__ == "__main__":
    df = loadfile()
    df['MARKET_cpd'] = compounded(df.MARKET)
    df.MARKET_cpd.plot()    