"""
Author: Rafael Tedesco - rocket.py
Date: 13/05/20
"""

from datetime import datetime

import pandas as pd

FIXEDTAX = 0.36
DAYTAX = 0.09


records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564627800, 'start': 1564626000}
]


def _cost_by_period(duration, start, end):
    if (int(start.hour) >= 6) and (int(end.hour) <= 22):
        return FIXEDTAX + (duration.seconds//60) * DAYTAX
    else:
        return FIXEDTAX


def _call_cost(calls):
    start_call = datetime.fromtimestamp(calls['start'])
    end_call = datetime.fromtimestamp(calls['end'])
    duration = end_call - start_call
    cost = f'{_cost_by_period(duration, start_call, end_call):,.2f}'
    return float(cost)


def get_costs(records):
    for calls in records:
        calls.update({'cost': _call_cost(calls)})
    return records


def classify_by_phone_number(records):
    total_bills = []
    records_cost = get_costs(records)
    df_bills = pd.DataFrame(records_cost)
    group_bills = df_bills.groupby('source')['cost'].sum()\
        .reset_index().rename(columns={'cost':'total'})\
        .sort_values(by='total', ascending=False)
    sources = [s for s in group_bills['source']]
    totals = [tt for tt in group_bills['total']]
    for bill in zip(sources, totals): 
        total_bills.append({'source': bill[0], 'total': round(bill[1], 2)})
    return total_bills
