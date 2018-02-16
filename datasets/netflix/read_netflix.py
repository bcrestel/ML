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

def groupbycustID(df):
    return df.drop('date', axis=1)\
            .groupby('custID')\
            .agg({'movieID':lambda x:x.tolist(),\
                  'rating':lambda x:x.tolist()})
    
def moviematrix(mmcomp):
    """ construct matrix of movie ratings
    rows=users, cols=movies"""
    print('Compute characteristics for movie matrix')
    data = np.array([float(x) for x in itertools.chain.from_iterable(mmcomp.rating.values)], dtype=np.float)
    cols = np.array([int(x) for x in itertools.chain.from_iterable(mmcomp.movieID.values)], dtype=np.int)-1
    rr = mmcomp.reset_index().apply(lambda x: [x.name for ii in x.movieID], axis=1)
    rows = np.array(list(itertools.chain.from_iterable(rr)), dtype=np.int)
    return data, rows, cols


def normalizedf(df):
    print('Normalize ratings per customer')
    dfmean = df.apply(lambda x : np.array(x.rating).mean(), axis=1)
    dfstd = df.apply(lambda x : np.array(x.rating).std(), axis=1)
    normalized = df.rating.apply(lambda x: 
        [(ii-np.array(x).mean())/np.array(x).std() if np.array(x).std() > 0 
         else 0.0 for ii in x])
    return dfmean, dfstd, normalized

def removesingleratings(df):
    print('remove customers with a single rating')
    return df[df.apply(lambda x : len(x.movieID), axis=1) > 1]
    
    

if __name__ == "__main__":
    df = read_netflix('combined_data_1_short.txt')
    td = totaldistr(df)
    tdpm = distrratingpermovie(df)
    
    mmcomp = groupbycustID(df)
    mmcomp = removesingleratings(mmcomp)
    means, stds, normalizedratings = normalizedf(mmcomp)
    mmcomp.rating = normalizedratings
    
    data, rows, cols = moviematrix(mmcomp)
    print('Assemble sparse dataframe')
    spmat = coo_matrix((data, (rows, cols)))
    dfm = pd.SparseDataFrame(spmat)
    