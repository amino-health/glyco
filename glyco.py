import pandas as pd
import logging
from matplotlib import pyplot as plt

from datetime import timedelta as tdel

import os
from os.path import isfile, join, getctime
from datetime import datetime as dt

from utils import weekday_map, is_weekend, nearest, nearest_deriv

DAT_LBL = '_date'
T_LBL = 'dtime'
G_LBL = 'Historic Glucose mmol/L'
SESSION_LEN_SEC = 2*60*60



"""
Freestyle Libre data prep
"""
def get_glucose_from_file(file_path, skiprows=1,
                          origin_t='Device Timestamp',
                          fmt='%d-%m-%Y %H:%M',
                          glbl=G_LBL,
                          t_lbl=T_LBL,
                          date_lbl=DAT_LBL, i_by_time=True,
                          set_deriv=True, interp='polynomial', ord=2):
    df = pd.read_csv(file_path, skiprows=skiprows)
    logging.log(logging.INFO, "Shape: {}\nColumns: {}".format(str(df.shape), str(df.columns)))
    df[t_lbl]=pd.to_datetime(df[origin_t], format=fmt)
    df[date_lbl]=df[t_lbl].dt.date
    df['hour'] = df[t_lbl].dt.hour
    df['dayofweek'] = df[t_lbl].dt.weekday
    df['weekday'] = df['dayofweek'].map(weekday_map)
    df['weekend'] = df['dayofweek'].map(is_weekend)
    if i_by_time:
        df.set_index(t_lbl, inplace=True)
        df['tid'] = df.index
        df.sort_index(inplace=True)
    if set_deriv:
        set_derivative(df, tlbl='tid', glbl=glbl)
    df[glbl] = df[glbl].interpolate(method=interp, order=ord)
    return df


def get_group_by_date(glucose_df, date_lbl=DAT_LBL, g_lbl=G_LBL):
    group= glucose_df.groupby([date_lbl])[g_lbl]
    g_df = group.mean()
    g_df['min'] = group.min()
    g_df['max'] = group.max()
    return g_df


def set_derivative(df, tlbl='tid', glbl=G_LBL):
    df['dg'] = df[glbl].diff()
    df['dt'] = df[tlbl].diff().dt.total_seconds()
    df['dg_dt'] = df.dg / df.dt
    return df


def get_meals_from_file():


    return

def get_perc(df, glbl=G_LBL, group_lbl='hour'):
    grouped = df.groupby([group_lbl])[glbl]
    mean = grouped.mean()
    dev = grouped.std()
    low95 = mean - 1.96*dev
    high95 = mean + 1.96 * dev
    low99 = mean - 3*dev
    high99 = mean + 3*dev
    low68 = mean - dev
    high68 = mean + dev
    return mean, dev, low95, high95, low68, high68, low99, high99

def get_percentile_dist(df, dist, glbl=G_LBL, group_lbl='hour'):
    grouped = df.groupby([group_lbl])[glbl]
    mean = grouped.mean()
    med = grouped.median()
    dev = grouped.std()
    perc_l = [grouped.quantile(q) for q in dist]
    perc_h = [grouped.quantile(1-q) for q in dist]
    return mean, dev, med, perc_l, perc_h

"""
Meal Pictures Data Prep
"""

def shift_fwd(t, h=1, m=0):
    return t+ tdel(hours=h, minutes=m)

def shift_back(t, h=1, m=0):
    return t- tdel(hours=h, minutes=m)

def get_meals(photos_path, shift_fn = shift_fwd):
    if not shift_fn:
        raise Exception('NOT SHIFTING TIME?')
    files_ts = [ (shift_fn(dt.fromtimestamp(os.stat(photos_path+f).st_mtime)), f) # shift by one hour
    for f in os.listdir(photos_path) if isfile(join(photos_path, f))]
    fs = [(f[0].day, f[0].hour, f[0].minute, f[0].hour*100+f[0].minute, "{}:{}".format(f[0].hour, f[0].minute), f[0], f[0], f[0].date(), f[1]) for f in files_ts]
    return pd.DataFrame(fs,
                        columns=['day', 'hour', 'minute', 'time_fmt','time_str', 'idx','ctime', 'cdate', 'filename'])

def get_indexed_meals(photos_path, idx, session_len_s=SESSION_LEN_SEC, shift_fn = shift_fwd):
    df = get_meals(photos_path, shift_fn)
    df.set_index([idx], inplace=True)
    df.sort_index(inplace=True)
    df['dt'] = df.ctime.diff().dt.total_seconds()
    df['session_start'] = (df.dt.isnull()) | (df.dt > session_len_s)
    df['meal_id'] = df[df['session_start']].ctime.rank(method='first').astype(int)
    df['meal_id'] = df['meal_id'].fillna(method='ffill').astype(int)
    return df



"""
PLOTTING
"""
def plot_glucose_summary(glucose, glbl = G_LBL):
    start_plot()
    plt.plot(glucose[glbl], label='Interstitial glucose trend (mmol/L)')
    plt.plot(glucose[glbl].rolling(10).mean(), label='Rolling average (mmol/L)')
    plt.axhline(y=glucose[glbl].mean(), label='Mean at {:.2}'.format(glucose[glbl].mean()))
    plt.axhline(y=7, label='Spike Limit', linestyle='--')

    end_plot()


def plot_meal_lines(mdf, i=0):
    [plt.axvline(m[i]) for m in mdf.iterrows()]





def plot_percentiles(df, dist=[0.01, 0.05], glbl = G_LBL, group_lbl='hour', whole=True, clr='blue'):
    mean, dev, med, perc_l, perc_h = get_percentile_dist(df, dist, glbl, group_lbl)
    if whole:
        start_plot()
    plt.plot(med)
    for i in range(len(dist)):
        plt.fill_between(med.index, perc_l[i], perc_h[i], color=clr, alpha=0.2)
    if whole:
        end_plot()

def plot_glucose_perc(df, glbl = G_LBL, group_lbl='hour'):
    mean, dev, low95, high95, low68, high68, low99, high99 = get_perc(df, glbl, group_lbl)
    start_plot()

    plt.plot(mean)
    plt.fill_between(mean.index, low68, high68, alpha=0.4)
    plt.fill_between(mean.index, low95, high95, alpha=0.2)
    plt.fill_between(mean.index, low99, high99, alpha=0.1)

    end_plot()

def cust_plot(df, glbl=G_LBL, group_lbl='hour'):
    mean, dev, low95, high95, low68, high68, low99, high99 = get_perc(df, glbl, group_lbl)


    plt.plot(mean)
    plt.fill_between(mean.index, low68, high68, alpha=0.4)
    plt.fill_between(mean.index, low95, high95, alpha=0.2)
    plt.fill_between(mean.index, low99, high99, alpha=0.1)



def plot_box_compare(df, outliers=False, compare_by='weekend', label_map = None, glbl = G_LBL):
    start_plot()
    all_vals = df[compare_by].unique()
    all_vals.sort()
    if label_map is None:
        plt.boxplot([df[df[compare_by] == i][glbl].dropna() for i in all_vals],
                labels= all_vals,
                showfliers=outliers)
    else:
        plt.boxplot([df[df[compare_by] == i][glbl].dropna() for i in all_vals],
                    labels=label_map(all_vals),
                    showfliers=outliers)

    plt.title('Comparing by: {}. {} outliers.'.
              format(compare_by, 'Showing' if outliers else 'Not showing'))
    end_plot()

def end_plot():
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def start_plot(l=8, w=6):
    plt.figure(num=None, figsize=(l, w), dpi=120, facecolor='w', edgecolor='k')


"""

"""