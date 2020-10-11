import pandas as pd


# M-value of Schlichtkrull
# 6 blood sugar measurements in 24 hours

# Mean average of glucose excursions
def mage(s):
    pass

# Count peaks
def count_peaks(s):
    """

    :param s: pandas series
    :return:
    """
    # smooth series

    # compute derivative

    # find peaks

    # find max derivetive
    pass

# find meal time
def find_meal_time(s, t_s):
    """

    :param s: series with glucose and time
    :param t_s: list of meal times
    :return:
    """
    # clean NaN
    meal_time_map = dict(
        [(t, None) for t in t_s]
    )

    # compute derivatives surrounding range 2 hours

    #
    return meal_time_map

# find sleep time
def find_wake_up_time(s, d):
    """

    :param s: series with glucose and time, ordered
    :param d: day
    :return:
    """
    # clean NaN

    today = s.loc[d]
    yesterday = s.loc[d-1]
    # derive s

    # find most stable
    # 95% of derivative

    #
    for i in s:
        wake = i

    return wake
