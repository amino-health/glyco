import pandas as pd
import logging
DAT_LBL = '_date'
T_LBL = 'dtime'
G_LBL = 'Historic Glucose mmol/L'

def get_glucose_from_file(file_path, origin_t='Device Timestamp', fmt='%d-%m-%Y %H:%M', t_lbl=T_LBL, date_lbl=DAT_LBL, i_by_time=True):
    df = pd.read_csv(file_path)
    logging.log(logging.INFO, "Shape: {}\nColumns: {}".format(str(df.shape), str(df.columns)))
    df[t_lbl]=pd.to_datetime(df[origin_t], format=fmt)
    df[date_lbl]=df[t_lbl].date
    if i_by_time:
        df.set_index(t_lbl, inplace=True)
    return df

def get_group_by_date(glucose_df, date_lbl=DAT_LBL, g_lbl=G_LBL):
    group= glucose_df.groupby([date_lbl])[G_LBL]
    g_df = group.mean()
    g_df['min'] = group.min()
    g_df['max'] = group.max()
    return g_df

def get_meals_from_file():
    return
