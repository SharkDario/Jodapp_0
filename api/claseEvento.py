
class Evento():
    def __init__(self, nombre, fecha, ubicacion, precio, descripcion, anfitrion, fechaFin, capacidad, rango, asistentes=[]):
        # El ID se genera desde la base de datos de Firebase al guardar el objeto,
        # Con el metodo setID se guarda el valor del ID
        self.__id=""
        self.__nombre = nombre
        self.__fecha = fecha
        self.__ubicacion = ubicacion
        self.__precio = precio
        self.__descripcion = descripcion
        self.__anfitrion = anfitrion
        # Si el objeto se crea por primera vez sera una lista vacia
        # En cambio, si ya existe en la base de datos
        # se pasara la lista con los IDs de los asistentes
        self.__asistentes = asistentes
        self.__fechaFin = fechaFin
        self.__capacidad = capacidad
        self.__rango = rango

    def getID(self):
        return self.__id
    
    def getNombre(self):
        return self.__nombre
    
    def getFecha(self):
        return self.__fecha
    
    def getUbicacion(self):
        return self.__ubicacion
    
    def getPrecio(self):
        return self.__precio
    
    def getDescripcion(self):
        return self.__descripcion
    
    def getAnfitrion(self):
        return self.__anfitrion
    
    def getFechaFin(self):
        return self.__fechaFin
    
    def getAsistentes(self):
        return self.__asistentes
    
    def getCapacidad(self):
        return self.__capacidad
    
    def getRango(self):
        return self.__rango
    
    def setNombre(self, valor):
        self.__nombre = valor

    def setFecha(self, valor):
        self.__fecha = valor

    def setUbicacion(self, valor):
        self.__ubicacion = valor

    def setPrecio(self, valor):
        self.__precio = valor

    def setDescripcion(self, valor):
        self.__descripcion = valor

    def setAnfitrion(self, valor):
        self.__anfitrion = valor

    def setAsistente(self, valor):
        self.__asistentes.append(valor)

    def setFechaFin(self, valor):
        self.__fechaFin = valor

    def setCapacidad(self, valor):
        self.__capacidad = valor

    def setRango(self, valor):
        self.__rango = valor

    def setID(self, valor):
        self.__id = valor

    def __capacidadActual(self):
        return self.__capacidad-self.cantidadAsistentes()

    # El metodo se define publico ya que ademas de ser usado dentro de __capacidadActual
    # y los metodos mostrar, tambien sera utilizado para realizar comparaciones entre eventos
    def cantidadAsistentes(self):
        return len(self.__asistentes)

    def eliminarAsistente(self, valor):
        self.__asistentes.remove(valor)
    #Datos generales
    def mostrarLista(self):
        return f"{self.__nombre}\t{self.__fecha}\t{self.__fechaFin}\t{self.__precio}\t{self.__capacidad}\t{self.__capacidadActual()}\t{self.cantidadAsistentes()}\t{self.__rango}"
    
    def mostrarAsistentes(self, usuarios):
        cadenaAsistentes = "Asistentes\n"
        for asistente in self.__asistentes:
            for usuario in usuarios:
                if asistente==usuario.getDNI():
                    cadenaAsistentes += f"{usuario.mostrar()}\n"
                    break
    #Datos especificos
    def mostrar(self):
        return f"Nombre: {self.__nombre}\nFecha: {self.__fecha}\nFecha fin: {self.__fechaFin}\nPrecio: {self.__precio}\nCapacidad: {self.__capacidad}\nCapacidad actual: {self.__capacidadActual()}\nCantidad de asistentes: {self.cantidadAsistentes()}\nRango: {self.__rango}"
    