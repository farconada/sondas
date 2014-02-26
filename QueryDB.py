__author__ = 'fernando'

class QueryDB:

    """
    dbFullPath: path absoluto al fichero sqlite
    """
    def __init__(self, dbFullPath):
        self.dbFullPath = dbFullPath

    """
    sondaId: una cadena con el ID de sonda
    dateIni: fecha inicial de los datos
    dateEnd: fecha final de los datos
    devuelve un conjunto de temperaturas y su fecha
    """
    def findTempBySonda(self, sondaId, dateIni, dateEnd):
        pass