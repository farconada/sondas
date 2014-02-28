__author__ = 'fernando'
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
from numpy import array
from DBHandler import DBHandler

class ChartGenerator:

    def __init__(self, data):
        self.data = array(data)

    def generate(self):
        print self.data[:,0]
        x = array([datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d,s, t in self.data])
        plt.plot(x, self.data[:,2])
        plt.show()

if __name__ == "__main__":
    db = DBHandler('/home/fernando/SONDAS_NAI/','/home/fernando/SONDAS_NAI/tempDatabase.db')
    #db.loadData()
    lines = db.findTempBySonda('SOND04', datetime(year=2013, month=10, day=1), datetime(year=2013, month=10, day=30))
    chart = ChartGenerator(lines)
    chart.generate()
