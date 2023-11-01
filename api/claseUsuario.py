from clasePersona import Persona

class Usuario(Persona):
    def __init__(self, dni, nombre, apellido, edad, correo, user, listaEventos=[], listaAmigos=[], listaEventosAsistidos=[]):
        super().__init__(dni, nombre, apellido, edad)
        self.__correo = correo
        self.__user = user
        self.__listaEventos = listaEventos
        self.__listaAmigos = listaAmigos
        self.__listaEventosAsistidos = listaEventosAsistidos

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
    # Polimorfismo
    def setDNI(self, valor, firebase):
        super().setDNI(valor, firebase, "Usuarios")
    # Polimorfismo
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
    # Metodo privado para mostrar tanto los eventos Asistidos como los eventos creados
    def mostrarEventos(self, listaEventosBD, lista="Asistidos", eventoNombre="Eventos"):
        # La listaEventosBD se genera desde clase Firebase mediante el atributo listaEventos o listaEventosAsistidos
        # lista puede ser Asistidos o Creados
        # eventoNombre puede ser Eventos, Fiestas, Conciertos, Matchs
        eventos = f"Lista de {eventoNombre} {lista}"
        for evento in listaEventosBD:
            eventos+=evento.mostrarLista()
        return eventos

    def editarEvento(self, tipo, idEvento, diccio, firebase):
        if idEvento in self.__listaEventos:
            # Se puede editar mediante la bd de firebase
            # Tipo puede ser Fiestas, Conciertos o Matchs
            firebase.editarAtributos(tipo, idEvento, diccio)

    def eliminarEvento(self, tipo, idEvento, firebase):
        if idEvento in self.__listaEventos:
            # Antes se debe eliminar de la bd
            # tipo puede ser Fiestas, Conciertos, Matchs
            firebase.eliminarDiccionario(tipo, idEvento)
            firebase.eliminarID("Usuarios", self.getDNI(), 'listaEventos', idEvento)
            self.__listaEventos.remove(idEvento)

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

    def eliminarAmigo(self, idAmigo, firebase):
        if idAmigo in self.__listaAmigos:
            #Antes se debe eliminar al self como amigo de este
            # Se elimina el segundo usuario de la listaAmigos del primer usuario (self)
            firebase.eliminarID("Usuarios", self.getDNI(), "listaAmigos", idAmigo)
            # Se elimina el primer usuario (self) de la listaAmigos del segundo usuario
            firebase.eliminarID("Usuarios", idAmigo, "listaAmigos", self.getDNI())
            self.__listaAmigos.remove(idAmigo)

    #Correo: {self.__correo}\n el correo no se deberia mostrar
    # Polimorfismo
    def mostrar(self):
        return f"{super().mostrar()}Usuario: {self.__user}\n"
    # Polimorfismo
    def objetoToDiccionario(self):
        # El dni no se guarda porque sera el child para guardar el diccioUsuario
        diccioUsuario = super().objetoToDiccionario()
        diccioUsuario2 = {'correo':self.__correo, 'user':self.__user, 'listaEventos':self.__listaEventos, 'listaAmigos':self.__listaAmigos, 'listaEventosAsistidos':self.__listaEventosAsistidos}
        # Fusion de los dos diccionarios
        diccioUsuario.update(diccioUsuario2)
        return diccioUsuario