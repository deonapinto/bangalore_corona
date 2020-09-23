import csv
import pandas as pd
import numpy as np
import os
import os.path
from os import path
from cor import WebScraper
import threading

__states=None
__districts=None

def load_states():
    global __states
    print('calling read_samplce_csv')
    df=read_sample_csv()
    print('got response from read_samplce_csv')
    __states=df['state'].unique()
    __states = __states.tolist()

def load_district(state):
    global __districts
    df=read_sample_csv()
    inpst=df.loc[df['state']==state]
    __districts=inpst.district.unique().tolist()
    return __districts

def get_states():
    return __states

def add_and_get_email(district,email):
    df=read_sample_csv()
    inpds=df.loc[df['district']==district]
    inpds['email']=email
    inpds.to_csv(r'userID.csv',mode='a',header=False,index=False,quoting=csv.QUOTE_NONNUMERIC)
    print('added email :', email)
    return inpds.values.tolist()

def read_sample_csv():
    if not path.exists('sample.csv'):
        t = WebScraper(callback=load_states)
        t.start()
        return pd.DataFrame(data= [[None for _ in range(6)]], columns=('state','district','case','cured','active','death'))
    else:
        return pd.read_csv("sample.csv")
if __name__=='__main__':
    load_states()
    load_district()
    print(__states)
    print(__districts)