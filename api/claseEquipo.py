from claseGrupo import Grupo

class Equipo(Grupo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__deporte = kwargs.get('deporte')

    def getDeporte(self):
        return self.__deporte
    
    def setDeporte(self, valor, firebase):
        if(firebase.editarAtributos("Equipos", self.getID(), {'deporte': valor})):
            self.__deporte = valor

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Equipos")

    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Equipos")

    def mostrarLista(self):
        return f"{super().mostrarLista()}Deporte: {self.__deporte}"

    def mostrar(self):
        return f"{super().mostrar()}Deporte: {self.__deporte}"