from clasePersona import Persona
# Define la clase Jugador que hereda de Persona
class Jugador(Persona):
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Persona utilizando super()
        super().__init__(**kwargs)
        self.__posicion = kwargs.get('posicion')

    def getPosicion(self):
        return self.__posicion
    
    def setPosicion(self, valor, firebase):
        if(firebase.editarID("Jugadores", self.getDNI(), valor)):
            self.__posicion = valor

        # Polimorfismo: Sobrescribe el método setDNI de la clase base Persona
    def setDNI(self, valor, firebase):
                # Llama al método setDNI de la clase base Persona utilizando super() y especifica el tipo "Jugadores"
        super().setDNI(valor, firebase, "Jugadores")
    # Polimorfismo: Sobrescribe el método setNombre de la clase base Persona
    def setNombre(self, valor, firebase):
            # Llama al método setNombre de la clase base Persona utilizando super() y especifica el tipo "Jugadores"
        super().setNombre(valor, firebase, "Jugadores")

    # Polimorfismo: Sobrescribe el método setApellido de la clase base Persona
    def setApellido(self, valor, firebase):
        # Llama al método setApellido de la clase base Persona utilizando super() y especifica el tipo "Jugadores"
        super().setApellido(valor, firebase, "Jugadores")

    # Polimorfismo: Sobrescribe el método setEdad de la clase base Persona
    def setEdad(self, valor, firebase):
        # Llama al método setEdad de la clase base Persona utilizando super() y especifica el tipo "Jugadores"
        super().setEdad(valor, firebase, "Jugadores")

    # Polimorfismo: Sobrescribe el método mostrar de la clase base Persona
    def mostrar(self):
        # Devuelve una cadena que muestra la información del jugador incluyendo los datos heredados de Persona
        return f"{super().mostrar()}Posicion: {self.__posicion}\n"
    # Polimorfismo: Sobrescribe el método objetoToDiccionario de la clase base Persona
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioJugador
        # Convierte la información del jugador en un diccionario, incluyendo los datos heredados de Persona
        diccioJugador = super().objetoToDiccionario()
        diccioJugador['posicion']=self.__posicion
        return diccioJugador
