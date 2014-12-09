#!/usr/bin/env python

def parse(timestamp):
#    keys = ['mo', 'dd', 'hh', 'mi', 'ss']
    from datetime import datetime as dt
    dt.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')
    import re
    return dt.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')

def loadInput():
    import sys
    import json
    import unicodedata
    inputfile = sys.argv[1]
    with open(inputfile, 'r') as f:
        line = f.readlines()[0]
        return [parse(ts) for ts in json.loads(line)]

def groupByHour(timestamp):
    from itertools import groupby
    truncDatetime = [d.replace(minute=0, second=0, microsecond=0) for d in timestamp]
    from datetime import datetime as dt
    STARTTIME = dt(2012,1,1,0,0,0)
    frequency = [(abs(key-STARTTIME).total_seconds() / 3600.0, len(list(group))) for key, group in groupby(truncDatetime)]
    return zip(*frequency)

def groupByWeek(timestamp):
    from itertools import groupby
    truncDatetime = [d.isocalendar()[1] for d in timestamp]
    from datetime import datetime as dt
    STARTTIME = dt(2012,1,1,0,0,0)
    frequency = [(key, len(list(group))) for key, group in groupby(truncDatetime)]
    return zip(*frequency)

def hist(data):
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    length = len(data)
    import math
    width = int(math.sqrt(length))
    height = int((length / width) + (1 if length % width else 0))
    for d in range(0,length):
        plt.subplot(width, height, d+1)
        plt.title(data[d]['title'])
        n, bins, patches = plt.hist(data[d]['data'], 60, normed=0, facecolor='green', alpha=0.75)

    plt.show()


def scatter(data):
    import matplotlib.pyplot as plt
    import numpy as np

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

    plt.show()

def plot(data):
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    length = len(data)
    import math
    width = int(math.sqrt(length))
    height = int((length / width) + (1 if length % width else 0))
    if(width < height):
        width,height = height,width

    ax = None
    for d in range(0,length):
        if ax : 
            ax = plt.subplot(width, height, d+1, sharey = ax)
        else:
            plt.subplot(width, height, d+1)
        plt.plot(data[d]['data'][0], data[d]['data'][1], 'g-')
        if data[d].has_key('ylabel'):
            plt.ylabel(data[d]['ylabel'])
        if data[d].has_key('xlabel'):
            plt.xlabel(data[d]['xlabel'])
        if data[d].has_key('title'):
            plt.title(data[d]['title'])

    plt.show()


def main():
    #datetime
    input = loadInput()
    plot([
        {'data' : groupByWeek(input), 'title' : 'Demand curve', 'ylabel' : 'Request count', 'xlabel' : 'Week of year'},
        {'data' : groupByHour(input), 'ylabel' : 'Request count', 'xlabel' : 'Hour since 2012-01-01'},
        ])

    hist([{'data' : [y.weekday() for y in input], 'title' : 'Day of week'},
        {'data' : [y.day for y in input],'title' : 'Day of month'},
        {'data' : [y.hour for y in input],'title' : 'Hour of day'}, 
        {'data' : [y.isocalendar()[1] for y in input], 'title' : 'Week of year'}, 
        ])

    scatter([{'data' : [[y.weekday() for y in input], [y.hour for y in input], ], 'title' : 'Hour vs day of week'},
        {'data' : [[y.day for y in input], [y.hour for y in input],],'title' : 'hour vs day of month'},
        ])

    return input

main()