from clasePersona import Persona

class Artista(Persona):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__talento = kwargs.get('talento')

    def getTalento(self):
        return self.__talento
    
    def setTalento(self, valor, firebase):
        if(firebase.editarID("Artistas", self.getDNI(), valor)):
            self.__talento = valor

    # Polimorfismo
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Artistas")

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Artistas")

    def setApellido(self, valor, firebase):
        super().setApellido(valor, firebase, "Artistas")

    def setEdad(self, valor, firebase):
        super().setEdad(valor, firebase, "Artistas")

    # Polimorfismo
    def mostrar(self):
        return f"{super().mostrar()}Talento: {self.__talento}\n"
    # Polimorfismo
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioArtista
        diccioArtista = super().objetoToDiccionario()
        diccioArtista['talento']=self.__talento
        return diccioArtista
    
