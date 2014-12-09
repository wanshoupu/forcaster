from itertools import groupby
from datetime import datetime as dt
from analyzer import groupByWeek, groupByHour

STARTTIME = dt(2012,1,1,0,0,0)

class Trainer(object):
    # data is list of timestamps in json format
    def __init__(self, data):
        self.timestamps = data

    # features is a list of data points, each data point is a tuple of binary features
    # label are the labels of the data points
    # data and label should be of same length
    def preprocessing(self):
        #get isoweek frequency count
        self.weeklyCount = groupByWeek(self.timestamps)

        #get hourly count
        self.hourlyCount = groupByHour(self.timestamps)

        #start training
        self._train()

    def _train(self):
        self.weeklyModel = self.linReg(self.weeklyCount)
        self.trained = True

    def predict(self, timestamp):
        if not self.trained:
            return None
        isoweek = timestamp.isocalendar()[1]
        weeklyDemand = self.weeklyModel.predict(isoweek)
        return weeklyDemand / 7.0 / 24.0

    @staticmethod
    def linReg(x, y):
        from sklearn import linear_model
        # x: [[0, 0], [1, 1], [2, 2]]
        # y: [   0,      1,      2  ]
        clf = linear_model.LinearRegression(copy_X=True, fit_intercept=True, normalize=False)
        clf.fit (x, y)
        print dir(clf)
        print clf.coef_
        return clf

if __name__ == '__main__':
    Trainer.linReg([[0, 0], [1, 1], [2, 2]], [0,1,2])
