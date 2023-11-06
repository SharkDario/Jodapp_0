from claseGrupo import Grupo

# Define una nueva clase llamada Equipo que hereda de la clase Grupo
class Equipo(Grupo):
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Grupo utilizando kwargs
        super().__init__(**kwargs)
        # Inicializa un atributo privado __deporte con el valor de kwargs['deporte']
        self.__deporte = kwargs.get('deporte')

    # Getter para obtener el deporte del equipo
    def getDeporte(self):
        return self.__deporte
        
    # Setter para establecer el deporte y actualizarlo en Firebase
    def setDeporte(self, valor, firebase):
        if(firebase.editarAtributos("Equipos", self.getID(), {'deporte': valor})):
            self.__deporte = valor
            
    # Método de polimorfismo para establecer el nombre y actualizarlo en Firebase
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Equipos")
        
    # Método de polimorfismo para establecer un integrante y actualizarlo en Firebase
    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Equipos")
        
    # Método de polimorfismo para mostrar la lista de integrantes del equipo
    def mostrarLista(self):
        return f"{super().mostrarLista()}Deporte: {self.__deporte}"
        
    # Método de polimorfismo para mostrar información del equipo
    def mostrar(self):
        return f"{super().mostrar()}Deporte: {self.__deporte}"
