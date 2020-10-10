import pandas as pd
t_ = 'timestamp_'


def add_time_index(df):
    ndf = df.copy()
    ndf[t_] = pd.to_datetime()
    ndf.set_index([t_])
    return ndf