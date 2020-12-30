import pandas as pd

def get_week_label(week_start):
    if week_start == "All time":
        return week_start
    week_end = week_start + pd.DateOffset(days=6)
    return "{}-{}".format(week_start.strftime("%m/%d"), week_end.strftime("%m/%d"))


def get_week_options(weeks):
    return [{"label": "All time", "value": None}] + list(map(lambda week_start: {"label": get_week_label(week_start), "value": week_start}, weeks))


def filter_by_week_option_value(weekly, value, group_fn):
    if not value:
        return group_fn(weekly)
    else:
        return weekly.loc[value]