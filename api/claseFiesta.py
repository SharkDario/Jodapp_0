# Importa la clase Evento
from claseEvento import Evento
# Define una nueva clase llamada Fiesta que hereda de la clase Evento
# Esta es instanciada dentro de la clase JodApp
class Fiesta(Evento):
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
    def __init__(self, **kwargs):
        # Llama al constructor de la clase base Evento utilizando kwargs
        super().__init__(**kwargs)
        # Vestimenta guarda el codigo de vestimenta, como casual, formal, disfraces, etc.
        self.__vestimenta = kwargs.get('vestimenta')
        # Bar guarda el valor de verdad, True o False, si existe o no en la fiesta
        self.__bar = kwargs.get('bar')
        # Conservadora guarda el valor de verdad, True o False, si se permite o no llevar conservadora
        self.__conservadora = kwargs.get('conservadora')
        # Categoria de la fiesta, cumpleannos, aniversario, casamiento
        self.__categoria = kwargs.get('categoria')
        # Lista que contiene los IDs de las bandas que van a estar en la fiesta
        self.__bandas = kwargs.get('bandas', [])

    # Getters para obtener atributos específicos de Fiesta
    def getVestimenta(self):
        return self.__vestimenta
    
    def getBar(self):
        return self.__bar
    
    def getConservadora(self):
        return self.__conservadora
    
    def getCategoria(self):
        return self.__categoria
    
    def getBandas(self):
        return self.__bandas
    
    # Metodos Setter donde ocurre polimorfismo debido a que ya fueron definidas dentro de Evento
    # Vuelven a definirse con el tipo especifico "Fiestas", unicamente una fiesta puede modificarse a si misma
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Fiestas")

    def setFecha(self, valor, firebase):
        super().setFecha(valor, firebase, "Fiestas")

    def setUbicacion(self, valor, firebase):
        super().setUbicacion(valor, firebase, "Fiestas")

    def setPrecio(self, valor, firebase):
        super().setPrecio(valor, firebase, "Fiestas")

    def setDescripcion(self, valor, firebase):
        super().setDescripcion(valor, firebase, "Fiestas")

    def setAnfitrion(self, valor, firebase):
        super().setAnfitrion(valor, firebase, "Fiestas")

    def setAsistente(self, valor, firebase):
        super().setAsistente(valor, firebase, "Fiestas")

    def setFechaFin(self, valor, firebase):
        super().setFechaFin(valor, firebase, "Fiestas")

    def setCapacidad(self, valor, firebase):
        super().setCapacidad(valor, firebase, "Fiestas")

    def setRango(self, valor, firebase):
        super().setRango(valor, firebase, "Fiestas")


    # Setters para establecer atributos específicos de Fiesta y actualizar en Firebase
    # Unicamente una fiesta puede modificarse a si misma mediante su ID que obtiene mediante el metodo getID
    def setVestimenta(self, valor, firebase):
        # Primero se cambia en la bd y devuelve True, asi que se cambia del atributo
        if(firebase.editarAtributos("Fiestas", self.getID(), {'vestimenta': valor})):
            self.__vestimenta = valor

    def setBar(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'bar': valor})):
            self.__bar = valor

    def setConservadora(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'conservadora': valor})):
            self.__conservadora = valor

    def setCategoria(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'categoria': valor})):
            self.__categoria = valor

    def setBanda(self, valor, firebase):
        if(firebase.editarAtributos("Fiestas", self.getID(), {'bandas': valor}, "lista")):
            self.__bandas.append(valor)


    # Método privado para mostrar las bandas en formato de cadena
    def __mostrarBandas(self):
        bandas=""
        for banda in self.__bandas:
            #Aqui se recorre la base de datos para ver cuales coinciden con el ID
            bandas+=f"{banda.mostrar()}\n"
        return bandas

    
    # Método publico para eliminar una banda del evento
    def eliminarBanda(self, idBanda, firebase):
        if idBanda in self.__bandas:
            # Antes se debe eliminar de la bd
            # Como es una agregacion solo puedo eliminar el ID de mi listaBandas dentro de la fiesta
            firebase.eliminarID("Fiestas", self.getID(), 'bandas', idBanda)
            self.__bandas.remove(idBanda)
    
    # En este metodo ocurre polimorfismo, elimina un asistente mediante el DNI del usuario y utilizando el metodo de la superclase con el tipo "Fiestas"
    def eliminarAsistente(self, idValor, firebase):
        super().eliminarAsistente(idValor, firebase, "Fiestas")

    # Método publico para mostrar información detallada de la Fiesta, incluyendo sus atributos específicos
    # En este metodo ocurre polimorfismo debido a que ya fue definido en Evento
    def mostrar(self):
        datosFiesta = super().mostrar()
        return f"{datosFiesta}\nCategoria: {self.__categoria}\nVestimenta: {self.__vestimenta}\nBar: {self.__bar}\nConservadora: {self.__conservadora}\nBandas:\n{self.__mostrarBandas()}\n"

    # Método publico para convertir el objeto Fiesta en un diccionario, incluyendo atributos específicos
    # En este metodo ocurre polimorfismo debido a que ya fue definido en Evento
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioUsuario
        diccioFiesta = super().objetoToDiccionario()
        diccioFiesta2 = {'vestimenta':self.__vestimenta, 'bar':self.__bar, 'conservadora':self.__conservadora, 'categoria':self.__categoria, 'bandas':self.__bandas}
        # Fusion de los dos diccionarios
        diccioFiesta.update(diccioFiesta2)
        return diccioFiesta
