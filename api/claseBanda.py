from claseGrupo import Grupo

class Banda(Grupo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__genero = kwargs.get('genero')

    def getGenero(self):
        return self.__genero
    
    def setGenero(self, valor, firebase):
        if(firebase.editarAtributos("Bandas", self.getID(), {'genero': valor})):
            self.__genero = valor

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Bandas")

    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Bandas")

    def mostrarLista(self):
        return f"{super().mostrarLista()}Genero: {self.__genero}"

    def mostrar(self):
        return f"{super().mostrar()}Genero: {self.__genero}"