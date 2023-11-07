# Importa la clase Grupo
from claseGrupo import Grupo

# Define una nueva clase llamada Equipo que hereda de la clase Grupo
# Equipo es instanciada dentro de la clase JodApp
class Equipo(Grupo):
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
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

    # En los siguientes metodos Setter ocurre polimorfimo
    # Debido a que ya fueron definidos en la clase Grupo
    # Sin embargo, ahora se les pasa el tipo especifico ("Equipos")
    # Para establecer el nombre y actualizarlo en Firebase
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Equipos")
        
    # Método donde ocurre polimorfismo, para establecer un integrante y actualizarlo en Firebase
    def setIntegrante(self, valor, firebase):
        super().setIntegrante(valor, firebase, "Equipos")
        
    # En este metodo publico ocurre polimorfismo debido a que se vuelve a definir 
    # Mostrando tambien los datos especificos de Equipo en formato horizontal
    def mostrarLista(self):
        return f"{super().mostrarLista()}Deporte: {self.__deporte}"
        
    # En este metodo publico ocurre polimorfismo debido a que se vuelve a definir 
    # Mostrando tambien los datos especificos de Equipo
    def mostrar(self):
        return f"{super().mostrar()}Deporte: {self.__deporte}"
