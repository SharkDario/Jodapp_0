from claseGrupo import Grupo
# Define una nueva clase llamada Banda que hereda de la clase Grupo
class Banda(Grupo):
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Grupo utilizando kwargs
        super().__init__(**kwargs)
        # Inicializa un atributo privado __genero con el valor de kwargs['genero']
        self.__genero = kwargs.get('genero')
        
    # Getter para obtener el género de la banda
    def getGenero(self):
        return self.__genero
        
    # Setter para establecer el género y actualizarlo en Firebase
    def setGenero(self, valor, firebase):
        if(firebase.editarAtributos("Bandas", self.getID(), {'genero': valor})):
            self.__genero = valor
            
    # Método de polimorfismo para establecer el nombre y actualizarlo en Firebase
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Bandas")
        
    # Método de polimorfismo para establecer un integrante y actualizarlo en Firebase
    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Bandas")
        
    # Método de polimorfismo para mostrar la lista de integrantes de la banda
    def mostrarLista(self):
        return f"{super().mostrarLista()}Genero: {self.__genero}"
        
    # Método de polimorfismo para mostrar información de la banda
    def mostrar(self):
        return f"{super().mostrar()}Genero: {self.__genero}"
