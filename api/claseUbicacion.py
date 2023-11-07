# Se define la clase Ubicacion
# Es una clase contenida por la clase Evento
# Se realiza la instancia de esta clase al instanciar alguna de las hijas de Evento (Fiesta, Concierto o Match) dentro de la clase JodApp
class Ubicacion():
    def __init__(self, latitud, longitud, descripcion):
        # Constructor de la clase que inicializa los atributos privados
        # Latitud y Longitud guardan las coordenadas
        self.__latitud = latitud
        self.__longitud = longitud
        # Contiene la descripcion de la ubicacion en formato cadena
        self.__descripcion = descripcion

    # Método publico para obtener el valor de la latitud
    def getLatitud(self):
        return self.__latitud
        
    # Método publico para obtener el valor de la longitud
    def getLongitud(self):
        return self.__longitud
        
    # Método publico para obtener la descripción de la ubicación
    def getDescripcion(self):
        return self.__descripcion
        
    # Método publico para modificar el valor de la latitud
    def setLatitud(self, valor):
        self.__latitud = valor

    # Método publico para modificar el valor de la longitud 
    def setLongitud(self, valor):
        self.__longitud = valor
        
    # Método publico para modificar la descripción de la ubicación
    def setDescripcion(self, valor):
        self.__descripcion = valor
