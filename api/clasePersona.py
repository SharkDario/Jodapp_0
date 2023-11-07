# Se define la clase Persona
# Es una clase abstracta (no se realiza instancia de la misma)
# Es una clase base para las clases Usuario, Artista y Jugador
class Persona():
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
    def __init__(self, **kwargs):
        # Constructor de la clase que inicializa los atributos privados
        self.__dni = kwargs.get('dni')
        self.__nombre = kwargs.get('nombre')
        self.__apellido = kwargs.get('apellido')
        self.__edad = kwargs.get('edad')

    #Metodos getters y setterss
    def getDNI(self):
        return self.__dni
    
    def getNombre(self):
        return self.__nombre
    
    def getApellido(self):
        return self.__apellido
    
    def getEdad(self):
        return self.__edad

    # Los metodos setters utilizan la instancia de Firebase para cambiar los valores de los atributos en la base de datos
    # Estos vuelven a definirse en las clases hijas con el "tipo" especifico
    # Unicamente un objeto puede modificarse a si mismo, ya que se le pasa como argumento su propio ID/DNI
    def setDNI(self, valor, firebase, tipo):
        # Si se cambio en la bd quiere decir que era un dni distinto a uno existente, y devuelve True
        if(firebase.editarID(tipo, self.getDNI(), valor)):
            self.__dni = valor

    def setNombre(self, valor, firebase, tipo):
        # Si se cambio en la bd quiere decir que era un nombre distinto a uno existente, y devuelve True
        if(firebase.editarAtributos(tipo, self.getDNI(), {'nombre': valor})):
            self.__nombre = valor

    def setApellido(self, valor, firebase, tipo):
        if(firebase.editarAtributos(tipo, self.getDNI(), {'apellido': valor})):
            self.__apellido = valor

    def setEdad(self, valor, firebase, tipo):
        if(firebase.editarAtributos(tipo, self.getDNI(), {'edad': valor})):
            self.__edad =valor
        
    # Método que devuelve una cadena que muestra la información de la persona
    def mostrar(self):
        return f"DNI: {self.__dni}\nNombre: {self.__nombre}\nApellido: {self.__apellido}\nEdad: {self.__edad}\n"

    # Método que convierte la información de la persona en un diccionario
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccio de las clases que heredan Persona
        diccioPersona = {'nombre':self.getNombre(), 'apellido':self.getApellido(), 'edad':self.getEdad()}
        return diccioPersona
