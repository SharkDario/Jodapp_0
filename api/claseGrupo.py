
class Grupo():
    def __init__(self, **kwargs):
        self.__id = kwargs.get('id', "")
        self.__nombre = kwargs.get('nombre')
        self.__integrantes = kwargs.get('integrantes', [])

    def getID(self):
        return self.__id
    
    def getNombre(self):
        return self.__nombre
    
    def getIntegrantes(self):
        return self.__integrantes
    
    def setID(self, valor):
        self.__id = valor

    def setNombre(self, valor, firebase, tipo):
        if(firebase.editarAtributos(tipo, self.getID(), {'nombre': valor})):
            self.__nombre = valor

    def setIntegrante(self, valor, firebase, tipo):
        diccioIntegrante = valor.objetoToDiccionario()
        if(firebase.editarAtributos(tipo, self.getID(), {'integrantes': diccioIntegrante}, "lista")):
            self.__integrantes.append(valor)

    def __mostrarIntegrantes(self):
        datosInt = "Integrantes\n"
        for integrante in self.__integrantes:
            datosInt += f"{integrante.mostrar()}\n"
        return datosInt

    def mostrarLista(self):
        return f"Nombre:{self.__nombre}\t"
    
    def mostrar(self):
        return f"Nombre: {self.__nombre}\n{self.__mostrarIntegrantes()}"