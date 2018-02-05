import pandas as pd
import numpy as np


def read_netflix(filename):
    df = pd.read_csv(filename, header=None, names=['custID', 'rating', 'date'])
    # define a column with movieID
    df['movieID'] = df['custID']
    df.loc[~df['movieID'].str.endswith(':'),'movieID'] = np.NaN
    df['movieID'].fillna(method='ffill',inplace=True)
    df['movieID'] = df['movieID'].str[:-1]
    # remove unused rows with movieID
    df.drop(labels=(df['rating'] == np.NaN), axis=0, inplace=True)

    return df


def totaldistr(df):
    # distribution of ratings
    return 100.0*(df.groupby('rating').count()/df.groupby('rating').count().sum())['movieID']

def distrratingpermovie(df):
    return (100.0*df.groupby(['movieID','rating']).count()/df.groupby(['movieID','rating']).count().groupby('movieID').sum())['custID']


if __name__ == "__main__":
    df = read_netflix('combined_data_1_short.txt')
    td = totaldistr(df)
    tdpm = distrratingpermovie(df)
