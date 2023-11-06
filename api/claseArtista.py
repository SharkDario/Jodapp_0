from clasePersona import Persona

# Define una nueva clase llamada Artista que hereda de la clase Persona
class Artista(Persona):
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

    # Métodos de polimorfismo para actualizar datos en Firebase
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Artistas")

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Artistas")

    def setApellido(self, valor, firebase):
        super().setApellido(valor, firebase, "Artistas")

    def setEdad(self, valor, firebase):
        super().setEdad(valor, firebase, "Artistas")

    # Método de polimorfismo para mostrar información del artista
    def mostrar(self):
        return f"{super().mostrar()}Talento: {self.__talento}\n"
    # Método de polimorfismo para convertir el objeto Artista en un diccionario
    def objetoToDiccionario(self):
        # Convierte los datos de la persona en un diccionario
        # El dni no se guarda porque sera el child para guardar el diccioArtista
        diccioArtista = super().objetoToDiccionario()
        # Agrega el atributo talento al diccionario
        diccioArtista['talento']=self.__talento
        return diccioArtista
    
