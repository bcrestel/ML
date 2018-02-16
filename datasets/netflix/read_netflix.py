import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
import itertools

def read_netflix(filename):
    print('Read data')
    df = pd.read_csv(filename, header=None, names=['custID', 'rating', 'date'])
    # define a column with movieID
    df['movieID'] = df['custID']
    df.loc[~df['movieID'].str.endswith(':'),'movieID'] = np.NaN
    df['movieID'].fillna(method='ffill',inplace=True)
    df['movieID'] = df['movieID'].str[:-1]
    # remove unused rows with movieID
    df.drop(df[df.custID.str[-1]==':'].index, inplace=True)

    return df


def totaldistr(df):
    # distribution of ratings
    return 100.0*(df.groupby('rating').count()/df.groupby('rating').count().sum())['movieID']

def distrratingpermovie(df):
    return (100.0*df.groupby(['movieID','rating']).count()/df.groupby(['movieID','rating']).count().groupby('movieID').sum())['custID']

def moviematrix(df):
    """ construct matrix of movie ratings
    rows=users, cols=movies"""
    print('Compute characteristics for movie matrix')
    mmcomp = df.drop('date', axis=1)\
                .groupby('custID')\
                .agg({'movieID':lambda x:x.tolist(),\
                      'rating':lambda x:x.tolist()})
    data = np.array([int(x) for x in itertools.chain.from_iterable(mmcomp.rating.values)], dtype=np.float)
    cols = np.array([int(x) for x in itertools.chain.from_iterable(mmcomp.movieID.values)], dtype=np.int)-1
    rr = mmcomp.reset_index().apply(lambda x: [x.name for ii in x.movieID], axis=1)
    rows = np.array(list(itertools.chain.from_iterable(rr)), dtype=np.int)
    return data, rows, cols

    
    

if __name__ == "__main__":
    df = read_netflix('combined_data_1_short.txt')
    td = totaldistr(df)
    tdpm = distrratingpermovie(df)
    data, rows, cols = moviematrix(df)
    spmat = coo_matrix((data, (rows, cols)))
    dfm = pd.SparseDataFrame(spmat)