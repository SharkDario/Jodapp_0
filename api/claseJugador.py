from clasePersona import Persona

class Jugador(Persona):
    def __init__(self, dni, nombre, apellido, edad, posicion):
        super().__init__(dni, nombre, apellido, edad)
        self.__posicion = posicion

    def getPosicion(self):
        return self.__posicion
    
    def setPosicion(self, valor):
        self.__posicion = valor

    # Polimorfismo
    def mostrar(self):
        return f"{super().mostrar()}Posicion: {self.__posicion}\n"
    # Polimorfismo
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioJugador
        diccioJugador = super().objetoToDiccionario()
        diccioJugador['posicion']=self.__posicion
        return diccioJugador