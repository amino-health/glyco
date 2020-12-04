import pandas as pd
t_ = 'timestamp_'


weekday_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
is_weekend  = lambda x: 1 if x%7>4 else 0

def add_time_index(df):
    ndf = df.copy()
    ndf[t_] = pd.to_datetime()
    ndf.set_index([t_])
    return ndf

def nearest(df, pivot):
    items = list(df.index)
    n = items.copy()
    for i in range(100):

        m = min(n, key=lambda x: abs(x - pivot))
        if pd.isna(df.loc[m][gl.G_LBL]):
            n.remove(m)
        else:
            return m

def nearest_deriv(df, pivot):
    if not 'dg_dt' in df.columns:
        print('Nope')
        return
    items = list(df.index)
    n = items.copy()
    for i in range(100):

        m = min(n, key=lambda x: abs(x - pivot))
        if pd.isna(df.loc[m]['dg_dt']):
            n.remove(m)
        else:
            return m