from clasePersona import Persona

class Artista(Persona):
    def __init__(self, dni, nombre, apellido, edad, talento):
        super().__init__(dni, nombre, apellido, edad)
        self.__talento = talento

    def getTalento(self):
        return self.__talento
    
    def setTalento(self, valor):
        self.__talento = valor

    # Polimorfismo
    def mostrar(self):
        return f"{super().mostrar()}Talento: {self.__talento}\n"
    # Polimorfismo
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioArtista
        diccioArtista = super().objetoToDiccionario()
        diccioArtista['talento']=self.__talento
        return diccioArtista