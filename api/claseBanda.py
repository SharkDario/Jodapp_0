# Importa la clase Grupo
from claseGrupo import Grupo
# Define una nueva clase llamada Banda que hereda de la clase Grupo
# La clase Banda es una clase hija que se instancia dentro de la clase JodApp
class Banda(Grupo):
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Grupo utilizando kwargs
        super().__init__(**kwargs)
        # Inicializa un atributo privado __genero con el valor de kwargs['genero']
        self.__genero = kwargs.get('genero')
        
    # Getter para obtener el género de la banda
    def getGenero(self):
        return self.__genero

    # Los siguientes metodos setter volvieron a definirse (polimorfismo) para pasar el tipo especifico "Bandas"
    # Unicamente una banda puede modificarse a si misma, mediante su ID que se pasa automaticamente
    # Setter para establecer el género y actualizarlo en Firebase
    def setGenero(self, valor, firebase):
        if(firebase.editarAtributos("Bandas", self.getID(), {'genero': valor})):
            self.__genero = valor
    
    # Método de polimorfismo para establecer el nombre y actualizarlo en Firebase
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Bandas")
        
    # Método publico donde ocurre polimorfismo, para establecer un integrante y actualizarlo en Firebase
    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Bandas")
        
    # Método publico donde ocurre polimorfismo, para mostrar la lista de integrantes de la banda
    def mostrarLista(self):
        return f"{super().mostrarLista()}Genero: {self.__genero}"
        
    # Método publico donde ocurre polimorfismo, para mostrar información de la banda
    def mostrar(self):
        return f"{super().mostrar()}Genero: {self.__genero}"
