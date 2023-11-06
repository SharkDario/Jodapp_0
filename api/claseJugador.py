from clasePersona import Persona

class Jugador(Persona):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__posicion = kwargs.get('posicion')

    #def __init__(self, dni, nombre, apellido, edad, posicion):
    #    super().__init__(dni, nombre, apellido, edad)
    #    self.__posicion = posicion

    def getPosicion(self):
        return self.__posicion
    
    def setPosicion(self, valor, firebase):
        if(firebase.editarID("Jugadores", self.getDNI(), valor)):
            self.__posicion = valor

    # Polimorfismo
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Jugadores")

    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Jugadores")

    def setApellido(self, valor, firebase):
        super().setApellido(valor, firebase, "Jugadores")

    def setEdad(self, valor, firebase):
        super().setEdad(valor, firebase, "Jugadores")

    # Polimorfismo
    def mostrar(self):
        return f"{super().mostrar()}Posicion: {self.__posicion}\n"
    # Polimorfismo
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioJugador
        diccioJugador = super().objetoToDiccionario()
        diccioJugador['posicion']=self.__posicion
        return diccioJugador