
class Ubicacion():
    def __init__(self, latitud, longitud, descripcion):
        # Constructor de la clase que inicializa los atributos privados
        self.__latitud = latitud
        self.__longitud = longitud
        self.__descripcion = descripcion

    # Método para obtener el valor de la latitud
    def getLatitud(self):
        return self.__latitud
        
    # Método para obtener el valor de la longitud
    def getLongitud(self):
        return self.__longitud
        
    # Método para obtener la descripción de la ubicación
    def getDescripcion(self):
        return self.__descripcion
        
    # Método para modificar el valor de la latitud
    def setLatitud(self, valor):
        self.__latitud = valor

    # Método para modificar el valor de la longitud 
    def setLongitud(self, valor):
        self.__longitud = valor
        
    # Método para modificar la descripción de la ubicación
    def setDescripcion(self, valor):
        self.__descripcion = valor
