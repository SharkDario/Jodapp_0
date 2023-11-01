from claseEvento import Evento

# Cuando es una fiesta que ya fue creada, debo pasarle por el constructor todos los datos exactos que tiene en la bd
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
    
    #### Polimorfismo ####

    #def setID(self, firebase, diccio):
    #    diccio = self.objetoToDiccionario()
    #    super().setID(firebase, diccio, "Fiestas")
    
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Fiestas")

    def setFecha(self, valor, firebase):
        super().setFecha(valor, firebase, "Fiestas")

    def setUbicacion(self, valor, firebase):
        super().setUbicacion(valor, firebase, "Fiestas")

    def setPrecio(self, valor, firebase):
        super().setPrecio(valor, firebase, "Fiestas")

    def setDescripcion(self, valor, firebase):
        super().setDescripcion(valor, firebase, "Fiestas")

    def setAnfitrion(self, valor, firebase):
        super().setAnfitrion(valor, firebase, "Fiestas")

    def setAsistente(self, valor, firebase, tipo):
        super().setAsistente(valor, firebase, "Fiestas")

    def setFechaFin(self, valor, firebase):
        super().setFechaFin(valor, firebase, "Fiestas")

    def setCapacidad(self, valor, firebase, tipo):
        super().setCapacidad(valor, firebase, "Fiestas")

    def setRango(self, valor, firebase, tipo):
        super().setRango(valor, firebase, "Fiestas")


    ####              ####
    
    def setVestimenta(self, valor, firebase):
        # Primero se cambia en la bd y devuelve True, asi que se cambia del atributo
        if(firebase.editarAtributos("Fiestas", self.getID(), {'vestimenta': valor})):
            self.__vestimenta = valor

    def setBar(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'bar': valor})):
            self.__bar = valor

    def setConservadora(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'conservadora': valor})):
            self.__conservadora = valor

    def setCategoria(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'categoria': valor})):
            self.__categoria = valor

    def setBanda(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'bandas': valor}, "lista")):
            self.__bandas.append(valor)

    def eliminarBanda(self, idBanda, firebase):
        if idBanda in self.__bandas:
            # Antes se debe eliminar de la bd
            # Como es una agregacion solo puedo eliminar el ID de mi listaBandas dentro de la fiesta
            firebase.eliminarID("Fiestas", self.getID(), 'bandas', idBanda)
            self.__bandas.remove(idBanda)

    def __mostrarBandas(self):
        bandas=""
        for banda in self.__bandas:
            #Aqui se recorre la base de datos para ver cuales coinciden con el ID
            bandas+=f"{banda.mostrar()}\n"
        return bandas

    def mostrar(self):
        datosFiesta = super().mostrar()
        return f"{datosFiesta}\nCategoria: {self.__categoria}\nVestimenta: {self.__vestimenta}\nBar: {self.__bar}\nConservadora: {self.__conservadora}\nBandas:\n{self.__mostrarBandas()}\n"
    
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioUsuario
        diccioFiesta = super().objetoToDiccionario()
        diccioFiesta2 = {'vestimenta':self.__vestimenta, 'bar':self.__bar, 'conservadora':self.__conservadora, 'categoria':self.__categoria, 'bandas':self.__bandas}
        # Fusion de los dos diccionarios
        diccioFiesta.update(diccioFiesta2)
        return diccioFiesta