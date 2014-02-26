__author__ = 'fernando'
import os
from os import listdir
from os.path import isfile, join
from datetime import date
import sqlite3

class DBLoader:
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
        self.__wipeDB()
        self.dbConnection = sqlite3.connect(dbFullPath)
        self.__createDB()

    def __createDB(self):
        self.dbConnection.execute("create table temperatures (dateTime text, sondaId text, temperature integer)");

    def __wipeDB(self):
        try:
            os.remove(self.dbFullPath)
        except:
            print "No se ha podido eliminar {0}", self.dbFullPath

    def run(self):
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
        fileDate = date(2000 + int(csvFile[-6:-4]),  int(csvFile[-8:-6]), int(csvFile[-10:-8]))
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
                print temperature
            except:
              print "error " + str(previousTemperature)





if __name__ == "__main__":
    db = DBLoader('/Users/fernando/SONDAS_NAI/','/Users/fernando/SONDAS_NAI/tempDatabase.db')
    db.run()