# Importa la clase Persona 
from clasePersona import Persona
# Se define la clase Usuario que hereda de la clase Persona
class Usuario(Persona):
    # En el constructor se encuentra **kwargs 
    # Es el parámetro que nos permite crear objetos a partir de pasarle un diccionario con todos los valores de los atributos
    # Como la base de datos de Firebase guarda en formato diccionario, es una forma más sencilla de volver a crear los objetos
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__correo = kwargs.get('correo')
        self.__user = kwargs.get('user')
        # La siguiente lista guarda los IDs de los eventos creados por el usuario
        self.__listaEventos = kwargs.get('listaEventos', [])
        # La siguiente lista guarda los DNIs de los amigos del usuario
        self.__listaAmigos = kwargs.get('listaAmigos', [])
        # La siguiente lista guarda los IDs de los eventos a los que asiste el usuario
        self.__listaEventosAsistidos = kwargs.get('listaEventosAsistidos', [])
    
    # Metodos Getter para obtener los valores de los atributos
    def getCorreo(self):
        return self.__correo
    
    def getUser(self):
        return self.__user
    
    def getEventos(self):
        return self.__listaEventos
    
    def getAmigos(self):
        return self.__listaAmigos
    
    def getAsistencias(self):
        return self.__listaEventosAsistidos

    #Metodos Setter donde ocurre polimorfismo
    # Debido a que ya fueron definidos en la clase Persona
    # Sin embargo, ahora se les pasa el tipo especifico ("Usuarios")
    # Necesitan de la instancia de firebase para cambiar sus valores mediante su DNI
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Usuarios")
    # Polimorfimos
    def setNombre(self, valor, firebase):
        super().setNombre(valor, firebase, "Usuarios")
    # Polimorfismo
    def setApellido(self, valor, firebase):
        super().setApellido(valor, firebase, "Usuarios")
    #Polimorfismo
    def setEdad(self, valor, firebase):
        super().setEdad(valor, firebase, "Usuarios")

    def setCorreo(self, valor, firebase, userAuth):
        # Si se cambio en la bd quiere decir que era un correo distinto a uno existente, y devuelve True
        if(firebase.editarAtributos("Usuarios", self.getDNI(), {'correo': valor}, userAuth)):
            self.__correo = valor
    
    def setUser(self, valor, firebase):
        # Si se cambio en la bd quiere decir que era un user distinto a uno existente, y devuelve True
        if(firebase.editarAtributos("Usuarios", self.getDNI(), {'user': valor})):
            self.__user = valor
    
    def setEvento(self, idEvento, firebase):
        if(firebase.editarAtributos("Usuarios", self.getDNI(), {'listaEventos':idEvento}, "lista")):
            self.__listaEventos.append(idEvento)
    
    def setAmigo(self, idAmigo, firebase):
        if(firebase.editarAtributos("Usuarios", self.getDNI(), {'listaAmigos':idAmigo}, "lista")):
            self.__listaAmigos.append(idAmigo)
    
    def setAsistencia(self, idEvento, firebase):
        if(firebase.editarAtributos("Usuarios", self.getDNI(), {'listaEventosAsistidos':idEvento}, "lista")):
            self.__listaEventosAsistidos.append(idEvento)

    #Metodos publicos para mostrar los amigos, fiestas asistidas, y fiestas creadas
    def mostrarAmigos(self, listaAmigosBD):
        # La listaAmigosBD se genera desde clase Firebase mediante el atributo listaAmigos de la clase Usuario
        amigos="Lista de amigos:\n"
        for amigo in listaAmigosBD:
            amigos+=amigo.mostrar()
        return amigos
    # Metodo publico para mostrar tanto los eventos Asistidos como los eventos creados
    def mostrarEventos(self, listaEventosBD, lista="Asistidos", eventoNombre="Eventos"):
        # La listaEventosBD se genera desde clase Firebase mediante el atributo listaEventos o listaEventosAsistidos
        # lista puede ser Asistidos o Creados
        # eventoNombre puede ser Eventos, Fiestas, Conciertos, Matchs
        eventos = f"Lista de {eventoNombre} {lista}"
        for evento in listaEventosBD:
            eventos+=evento.mostrarLista()
        return eventos
    # Metodo publico para editar un evento mediante el id del mismo que se debe encontrar dentro de la lista de eventos creados por el usuario
    def editarEvento(self, tipo, idEvento, diccio, firebase):
        if idEvento in self.__listaEventos:
            # Se puede editar mediante la bd de firebase
            # Tipo puede ser Fiestas, Conciertos o Matchs
            firebase.editarAtributos(tipo, idEvento, diccio)
    # Metodo publico para eliminar un evento mediante el id del mismo que se debe encontrar dentro de la lista de eventos creados por el usuario
    def eliminarEvento(self, tipo, idEvento, firebase):
        if idEvento in self.__listaEventos:
            # Antes se debe eliminar de la bd
            # tipo puede ser Fiestas, Conciertos, Matchs
            firebase.eliminarDiccionario(tipo, idEvento)
            firebase.eliminarID("Usuarios", self.getDNI(), 'listaEventos', idEvento)
            self.__listaEventos.remove(idEvento)
    # Metodo publico para eliminar una asistencia mediante el id del evento que se debe encontrar en la lista de eventos asistidos del usuario
    def eliminarAsistencia(self, tipo, idEvento, firebase):
        if idEvento in self.__listaEventosAsistidos:
            # Antes se debe eliminar de la bd
            # tipo puede ser Fiestas, Conciertos, Matchs
            # Se elimina el dni de los asistentes del evento
            firebase.eliminarID(tipo, idEvento, "asistentes", self.getDNI())
            # Se elimina el id del evento de la lista de los eventos Asistidos
            firebase.eliminarID("Usuarios", self.getDNI(), "listaEventosAsistidos", idEvento)
            # Se elimina de la lista de eventos asistidos del objeto
            self.__listaEventosAsistidos.remove(idEvento)
    # Metodo publico para eliminar un amigo mediante el idAmigo que debe encontrarse dentro de la lista de amigos del usuario
    def eliminarAmigo(self, idAmigo, firebase):
        if idAmigo in self.__listaAmigos:
            #Antes se debe eliminar al self como amigo de este
            # Se elimina el segundo usuario de la listaAmigos del primer usuario (self)
            firebase.eliminarID("Usuarios", self.getDNI(), "listaAmigos", idAmigo)
            # Se elimina el primer usuario (self) de la listaAmigos del segundo usuario
            firebase.eliminarID("Usuarios", idAmigo, "listaAmigos", self.getDNI())
            self.__listaAmigos.remove(idAmigo)

    # En este metodo publico ocurre polimorfismo ya que vuelve a definise mostrando los datos especificos del usuario
    def mostrar(self):
        return f"{super().mostrar()}Usuario: {self.__user}\n"
    # En este metodo publico ocurre polimorfismo ya que vuelve a definirse convirtiendo al objeto Usuario en un diccionario
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioUsuario
        diccioUsuario = super().objetoToDiccionario()
        diccioUsuario2 = {'correo':self.__correo, 'user':self.__user, 'listaEventos':self.__listaEventos, 'listaAmigos':self.__listaAmigos, 'listaEventosAsistidos':self.__listaEventosAsistidos}
        # Fusion de los dos diccionarios
        diccioUsuario.update(diccioUsuario2)
        return diccioUsuario
