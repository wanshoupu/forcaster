from itertools import groupby
from datetime import datetime as dt
from analyzer import plot,groupByWeek, groupByHour,toNumHours,STARTTIME,FIG_DIR

STARTTIME = dt(2012,1,1,0,0,0)

def augment(x):
    return zip(*[range(0, len(x)), x])

class Trainer(object):
    # data is list of timestamps in json format
    def __init__(self, logger):
        self.trained = False
        self.logger = logger

    def train(self, timestamps):
        # features is a list of data points, each data point is a tuple of binary features
        # label are the labels of the data points
        # data and label should be of same length
        #get isoweek frequency count
        self.weeklyCount = groupByWeek(timestamps)
        self.weeklyModel = self.linReg(toNumHours(self.weeklyCount[0]), self.weeklyCount[1])

        #get hourly count
#        self.hourlyCount = groupByHour(timestamps)
        self.trained = True
        self.predict(self.weeklyCount[0])
        plt = plot([
            {'data' : groupByWeek(timestamps), 'title' : 'Demand curve', 'ylabel' : 'Request count', 'xlabel' : 'Week of year'},
            {'data' : [self.weeklyCount[0],self.predict(self.weeklyCount[0])], 'ylabel' : 'Prediction', 'xlabel' : 'Week of year'},
            ])
        return plt

    def predict(self, timestamps):
        if not self.trained:
            return None
        numHours = toNumHours(timestamps)

        if self.logger:
            self.logger.info(self.weeklyModel.coef_)
        if numHours:
            weeklyDemand = self.weeklyModel.predict(augment(numHours))
            return weeklyDemand / 7.0 / 24.0
        else:
            return None

    @staticmethod
    def linReg(x, y):
        from sklearn import linear_model
        # x: [0, 1, 2]
        # xaug: [[1, 0], [1, 1], [1, 2]]
        # y: [   0,      1,      2  ]
        clf = linear_model.LinearRegression(copy_X=True, fit_intercept=True, normalize=False)
        clf.fit (augment(x), y)
        return clf

if __name__ == '__main__':
    clf = Trainer.linReg([9, 10, 11, 12, 13, 14, 15, 16, 17, 18], [1602, 2200, 2074, 2351, 2480, 2258, 2770, 3314, 3154, 244])
    print clf.predict(augment([9,10]))
