from itertools import groupby
from datetime import datetime as dt
from analyzer import plot,groupByWeek, groupByHour,toNumHours,STARTTIME,FIG_DIR

STARTTIME = dt(2012,1,1,0,0,0)

def augment(x):
    return map(lambda e: (1,) + e, x )

def ftrzWkdHr(timestamps):
    isoweekFeature = map(lambda x : x.isocalendar()[2], timestamps)
    hourOfDayFeature = map(lambda x :x.hour, timestamps)
    return zip(isoweekFeature, hourOfDayFeature)

def trimData(groupByWeek):
    unabrdg = zip(*groupByWeek)
    del(unabrdg[-1])
    return zip(*unabrdg)

def ftrzWk(timestamps):
    return map(lambda x : (x,), toNumHours(timestamps))

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
        weeklyData = groupByWeek(timestamps)
        trimWkData = trimData(weeklyData)
        self.wkMdl = self.linReg(ftrzWk(trimWkData[0]), trimWkData[1])
        if self.logger:
            self.logger.info(self.wkMdl.coef_)

        hourlydata = groupByHour(timestamps)
        self.adjHrCnt = self.adjWkTrend(hourlydata)
        self.wkdHrMdl = self.linReg(ftrzWkdHr(hourlydata[0]), self.adjHrCnt)
        if self.logger:
            self.logger.info(self.wkdHrMdl.coef_)
        str1 = self.predict(hourlydata[0])
        self.logger.info('Shoupu Wan')
        self.logger.info(str1)

        self.trained = True

        import time
        imgname = time.strftime("%Y%m%d-%H%M%S")
        img1,img2 = imgname+'1.png',imgname+'2.png'
        plt = plot([
            {'data' : weeklyData, 'title' : 'Weekly demand curve training error', 'ylabel' : 'Request count', 'label' : 'Original data'},
            {'data' : [weeklyData[0],self.calcWeekFactor(weeklyData[0])], 'xlabel' : 'Hour', 'label' : 'Trained result'},
            ])
        plt.savefig('resources/'+img1, bbox_inches='tight')

        ovlPlt = plot([
#            {'data' : hourlydata, 'title' : 'Overall demand curve training error', 'ylabel' : 'Request count', 'label' : 'Original data'},
            {'data' : [hourlydata[0], self.predict(hourlydata[0])], 'xlabel' : 'Hour', 'label' : 'Trained result'},
            ])
        plt.savefig('resources/'+img2, bbox_inches='tight')
        return img1,img2

    def adjWkTrend(self, hourlydata):
        hourlyprediction = self.calcWeekFactor(hourlydata[0])
        return map(lambda x,y : x/y, hourlydata[1], hourlyprediction)

    def calcWeekFactor(self, timestamps):
        inputdata = ftrzWk(timestamps)
        return self.wkMdl.predict(augment(inputdata))

    def calcWeekdayHourFactor(self, timestamps):
        inputdata = ftrzWkdHr(timestamps)
        return self.wkdHrMdl.predict(augment(inputdata))

    def predict(self, timestamps):
        if not (self.trained):
            return None
        weekFactor = self.calcWeekFactor(timestamps)
        weekdayHourFactor = self.calcWeekdayHourFactor(timestamps)
        return map(lambda x,y : x * y, weekdayHourFactor, weekdayHourFactor)

#    @staticmethod
    def linReg(self, x, y):
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
