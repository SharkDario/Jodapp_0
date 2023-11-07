# Importa la clase Persona
from clasePersona import Persona

# Define una nueva clase llamada Artista que hereda de la clase Persona
class Artista(Persona):
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Persona utilizando kwargs
        super().__init__(**kwargs)
        # Inicializa un atributo privado __talento con el valor de kwargs['talento']
        self.__talento = kwargs.get('talento')
    # Getter para obtener el talento del artista
    def getTalento(self):
        return self.__talento

    # Setter para establecer el talento y actualizarlo en Firebase
    def setTalento(self, valor, firebase):
        if(firebase.editarID("Artistas", self.getDNI(), valor)):
            self.__talento = valor

    # En los siguientes metodos ocurre polimorfimo
    # Debido a que ya fueron definidos en la clase Persona
    # Sin embargo, ahora se les pasa el tipo especifico ("Artistas")
    # Utilizan la instancia de Firebase para guardar los nuevos valores
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Artistas")

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Artistas")

    def setApellido(self, valor, firebase):
        super().setApellido(valor, firebase, "Artistas")

    def setEdad(self, valor, firebase):
        super().setEdad(valor, firebase, "Artistas")

    # En este metodo publico ocurre polimorfismo debido a que se vuelve a definir 
    # Mostrando tambien los datos especificos de Artista
    def mostrar(self):
        return f"{super().mostrar()}Talento: {self.__talento}\n"
    # En este metodo publico ocurre polimorfismo debido a que se vuelve a definir 
    # Para convertir el objeto Artista en un diccionario
    def objetoToDiccionario(self):
        # Convierte los datos de la persona en un diccionario
        # El dni no se guarda porque sera el child para guardar el diccioArtista
        diccioArtista = super().objetoToDiccionario()
        # Agrega el atributo talento al diccionario
        diccioArtista['talento']=self.__talento
        return diccioArtista
    
