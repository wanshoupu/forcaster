#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td
STARTTIME = dt(2012,1,1,0,0,0)
FIG_DIR='resources/'

def parse(timestamp):
#    keys = ['mo', 'dd', 'hh', 'mi', 'ss']
    dt.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')
    import re
    return dt.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')

def parseJson(str):
    import json
    return [parse(ts) for ts in json.loads(str)]

def loadFile():
    import sys
    inputfile = sys.argv[1]
    with open(inputfile, 'r') as f:
        return f.readlines()[0]

def groupByHour(timestamp):
    from itertools import groupby
    truncDatetime = [d.replace(minute=0, second=0, microsecond=0) for d in timestamp]
    frequency = [(key, len(list(group))) for key, group in groupby(truncDatetime)]
    return [list(f) for f in zip(*frequency)]

def isoYearStart(iso_year):
    fourth_jan = dt(iso_year, 1, 4)
    delta = td(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def isocalendarToDate(iso_year, iso_week, iso_day):
    year_start = isoYearStart(iso_year)
    return year_start + td(days=iso_day-1, weeks=iso_week-1)

def groupByWeek(timestamp):
    from itertools import groupby
    isocalendar = [d.isocalendar() for d in timestamp]
    truncDatetime = [isocalendarToDate(i[0], i[1], 1) for i in isocalendar]
    frequency = [(key, len(list(group))) for key, group in groupby(truncDatetime)]
    return [list(f) for f in zip(*frequency)]

def hist(data):
    fig = plt.figure()
    length = len(data)
    import math
    width = int(math.sqrt(length))
    height = int((length / width) + (1 if length % width else 0))
    for d in range(0,length):
        plt.subplot(width, height, d+1)
        plt.title(data[d]['title'])
        n, bins, patches = plt.hist(data[d]['data'], 60, normed=0, facecolor='green', alpha=0.75)
    return plt


def scatter(data):
    fig = plt.figure()
    length = len(data)
    import math
    width = int(math.sqrt(length))
    height = int((length / width) + (1 if length % width else 0))
    ax = None
    for d in range(0,length):
        distincts = [len(set(data[d]['data'][1])), len(set(data[d]['data'][0]))]
        if ax : 
            ax = plt.subplot(width, height, d+1, sharey = ax)
        else:
            plt.subplot(width, height, d+1)
        H, xedges, yedges = np.histogram2d(data[d]['data'][0], data[d]['data'][1], bins=(distincts))
        plt.imshow(H, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
        plt.title(data[d]['title'])
    return plt

def toNumHours(timestamps):
    return list(abs(t-STARTTIME).total_seconds() / 3600.0 for t in timestamps)

def plot(data):
    fig = plt.figure()
    length = len(data)
    for d in range(0,length):
        hours = toNumHours(data[d]['data'][0])
        plt.plot(hours, data[d]['data'][1], label=data[d]['label'])
        if data[d].has_key('ylabel'):
            plt.ylabel(data[d]['ylabel'])
        if data[d].has_key('xlabel'):
            plt.xlabel(data[d]['xlabel'])
        if data[d].has_key('title'):
            plt.title(data[d]['title'])
        plt.legend(shadow=True, fancybox=True, loc='upper left')
    return plt

if __name__ == '__main__':
    #datetime
    input = parseJson(loadFile())
    plt = plot([
        {'data' : groupByWeek(input), 'title' : 'Demand curve', 'ylabel' : 'Request count', 'label' : 'Weekly'},
        {'data' : groupByHour(input), 'ylabel' : 'Request count', 'xlabel' : 'Hour since 2012-01-01', 'label' : 'Hourly'},
        ])
    plt.savefig(FIG_DIR+'demand_curve.png', bbox_inches='tight')

    plt = hist([{'data' : [y.weekday() for y in input], 'title' : 'Day of week'},
        {'data' : [y.day for y in input],'title' : 'Day of month'},
        {'data' : [y.hour for y in input],'title' : 'Hour of day'}, 
        {'data' : [y.isocalendar()[1] for y in input], 'title' : 'Week of year'}, 
        ])
    plt.savefig(FIG_DIR+'hist_pattern.png', bbox_inches='tight')

    plt = scatter([{'data' : [[y.weekday() for y in input], [y.hour for y in input], ], 'title' : 'Hour vs day of week'},
        {'data' : [[y.day for y in input], [y.hour for y in input],],'title' : 'hour vs day of month'},
        ])
    plt.savefig(FIG_DIR+'week_hour_pattern.png', bbox_inches='tight')
