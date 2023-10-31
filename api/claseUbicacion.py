
class Ubicacion():
    def __init__(self, latitud, longitud, descripcion):
        self.__latitud = latitud
        self.__longitud = longitud
        self.__descripcion = descripcion

    def getLatitud(self):
        return self.__latitud
    
    def getLongitud(self):
        return self.__longitud
    
    def getDescripcion(self):
        return self.__descripcion
    
    def setLatitud(self, valor):
        self.__latitud = valor
    
    def setLongitud(self, valor):
        self.__longitud = valor
    
    def setDescripcion(self, valor):
        self.__descripcion = valor