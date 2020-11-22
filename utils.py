import pandas as pd
t_ = 'timestamp_'


weekday_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
is_weekend  = lambda x: 1 if x%7>4 else 0

def add_time_index(df):
    ndf = df.copy()
    ndf[t_] = pd.to_datetime()
    ndf.set_index([t_])
    return ndf