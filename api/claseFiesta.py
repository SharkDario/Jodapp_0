from claseEvento import Evento

class Fiesta(Evento):
    def __init__(self, nombre, fecha, ubicacion, precio, descripcion, anfitrion, fechaFin, capacidad, rango, vestimenta, bar, conservadora, categoria):
        super().__init__(nombre, fecha, ubicacion, precio, descripcion, anfitrion, fechaFin, capacidad, rango)
        self.__vestimenta = vestimenta
        self.__bar = bar
        self.__conservadora = conservadora
        self.__categoria = categoria
        self.__bandas = []

    def getVestimenta(self):
        return self.__vestimenta
    
    def getBar(self):
        return self.__bar
    
    def getConservadora(self):
        return self.__conservadora
    
    def getCategoria(self):
        return self.__categoria
    
    def getBandas(self):
        return self.__bandas
    
    def setVestimenta(self, valor):
        self.__vestimenta = valor

    def setBar(self, valor):
        self.__bar = valor

    def setConservadora(self, valor):
        self.__conservadora = valor

    def setCategoria(self, valor):
        self.__categoria = valor

    def setBanda(self, valor):
        self.__bandas.append(valor)

    def eliminarBanda(self, valor):
        self.__bandas.remove(valor)

    def __mostrarBandas(self):
        bandas=""
        for banda in self.__bandas:
            #Aqui se recorre la base de datos para ver cuales coinciden con el ID
            bandas+=f"{banda.mostrar()}\n"
        return bandas

    def mostrar(self):
        datosFiesta = super().mostrar()
        return f"{datosFiesta}\nCategoria: {self.__categoria}\nVestimenta: {self.__vestimenta}\nBar: {self.__bar}\nConservadora: {self.__conservadora}\nBandas:\n{self.__mostrarBandas()}\n"
    
    