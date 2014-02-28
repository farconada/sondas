__author__ = 'fernando'
import os
from os import listdir
from os.path import isfile, join
from datetime import date, timedelta, datetime
import sqlite3

class DBHandler:
    numSondas = 18

    """
    csvFilesDirectory: fichero con las carpetas de las sondas
    dbFullPath: path absoluto al fichero sqlite
    dataInterval: intervalo entre temperaturas, en minutos
    """
    def __init__(self, csvFilesDirectory, dbFullPath, dataInterval=15):
        self.csvFilesDirectory = csvFilesDirectory
        self.dbFullPath = dbFullPath
        self.dataInterval = dataInterval
        self.dbConnection = sqlite3.connect(self.dbFullPath)

    def __createDB(self):
        self.dbConnection.execute("create table temperatures (dateTime text, sondaId text, temperature integer)");

    def __wipeDB(self):
        try:
            os.remove(self.dbFullPath)
        except:
            print "No se ha podido eliminar {0}", self.dbFullPath

    def loadData(self):
        self.__wipeDB()
        self.__createDB()

        for sonda in range(1, self.numSondas + 1):
            sondaId = "SOND{0:02d}".format(sonda)
            sondaPath = "{0}{1}/".format(self.csvFilesDirectory, sondaId)
            sondaCsvFiles = [ f for f in listdir(sondaPath) if isfile(join(sondaPath,f)) ]
            for csvFile in sondaCsvFiles:
                self.__insertCSV(sondaPath + csvFile, sondaId)


    """
    csvFile: fichero CSV con el path completo
    """
    def __insertCSV(self, csvFile, sondaId):
        temperatureDateTime = datetime(2000 + int(csvFile[-6:-4]),  int(csvFile[-8:-6]), int(csvFile[-10:-8]))
        file = open(csvFile, 'r')
        temperature = 0
        previousTemperature = 0
        for line in file:
            try:
                line = line[:-1] # se quita el salto de linea
                previousTemperature = temperature
                if line[0] == "F":
                    line = int(line[1:]) * -1
                temperature = int(line)
                if temperature > 10 or temperature < -10:
                    temperature = temperature / 10
                sql = "insert into temperatures values('{}','{}',{})".format(temperatureDateTime, sondaId, temperature)
                temperatureDateTime = temperatureDateTime + timedelta(minutes=self.dataInterval)
            except ValueError as ex:
                print ex
                sql = "insert into temperatures values('{}','{}',{})".format(temperatureDateTime, sondaId, previousTemperature)
            self.dbConnection.execute(sql)
        self.dbConnection.commit()

    """
    sondaId: una cadena con el ID de sonda
    dateIni: fecha inicial de los datos
    dateEnd: fecha final de los datos
    devuelve un conjunto de temperaturas y su fecha
    """
    def findTempBySonda(self, sondaId, dateIni, dateEnd):
        cursor = self.dbConnection.cursor()
        sql = "SELECT * FROM temperatures where sondaId=? and dateTime >= ? and dateTime <= ? order by dateTime"
        cursor.execute(sql, [sondaId, dateIni, dateEnd])
        return cursor.fetchall()

if __name__ == "__main__":
    db = DBHandler('/home/fernando/SONDAS_NAI/','/home/fernando/SONDAS_NAI/tempDatabase.db')
    db.loadData()
    lines = db.findTempBySonda('SOND01', datetime(year=2013, month=11, day=1), datetime(year=2013, month=11, day=30))
    for l in lines:
        print l