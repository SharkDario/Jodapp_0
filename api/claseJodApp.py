# Se importan los siguientes recursos para crear la aplicacion Flask
# Flask clase principal para instanciar una app Flask
# render_template genera una pagina web a partir de un html y datos
# request representa la solicitud HTTP del cliente
# flash almacena mensajes que seran recuperados por los html al ser renderizados
# redirect genera una respuesta que redirige al cliente a un URL diferente
# url_for genera una URL para un punto final
from flask import Flask, render_template, request, flash, redirect, url_for
# Se importan las siguientes clases de las cuales se instanciaran objetos de las mismas dentro de la clase JodApp
from claseFirebase import Firebase
from claseUsuario import Usuario
from claseFiesta import Fiesta
from claseBanda import Banda
from claseArtista import Artista
#from claseJugador import Jugador
#from claseEquipo import Equipo
# Se importa los siguientes recursos de matplotlib para realizar graficos y codificarlos para mostrarlos dentro de la app web
import matplotlib.pyplot as plt
import io, base64
import matplotlib
# Se importa time para el tiempo en ese momento del servidor
import time
# Se define la clase JodApp, es la clase principal que permite a la app web de Flask funcionar
# Tiene asociaciones con todas las clase importadas, ya que realiza instancias de las mismas en los distintos metodos
# Tiene una relacion de composicion con la clase Firebase, ya que necesita de la misma para la base de datos en tiempo real y la autenticacion de Firebase
# Tambien tiene una relacion de composicion con la clase Flask, ya que realiza una instancia de la misma
class JodApp:
    # Constructor de la clase JodApp
    def __init__(self):
        # Los atributos son publicos debido a que es necesario para que la aplicacion funcione correctamente entre clases
        # Se realiza una instancia de la clase Firebase
        self.firebase = Firebase()
        # Se realiza una instancia de la clase Flask para la aplicacion web
        self.app = Flask(__name__)
        # Genera una clave secreta para la sesion
        self.app.secret_key = "holaMundo"
        # Se definen las distintas rutas y metodos asociados de la aplicacion
        self.app.route('/')(self.home)
        self.app.route('/login')(self.login)
        self.app.route('/signup', methods=['POST', 'GET'])(self.signup)
        self.app.route('/registrarte', methods=['POST', 'GET'])(self.registrarte)
        self.app.route('/iniciarSesion', methods=['POST', 'GET'])(self.iniciarSesion)
        self.app.route('/creacionEvento', methods=['POST'])(self.creacionEvento)
        self.app.route('/crearEvento', methods=['POST'])(self.crearEvento)
        self.app.route('/verListaEventos', methods=['POST'])(self.verListaEventos)
        self.app.route('/verListaDeSusEventos', methods=['POST'])(self.verListaDeSusEventos)
        # Estas rutas vuelven a redirigir a creacionEvento, una vez creado un Artista, Banda, Jugador o Equipo
        self.app.route('/crearArtista', methods=['POST', 'GET'])(self.crearArtista)
        self.app.route('/crearBanda', methods=['POST', 'GET'])(self.crearBanda)
        self.app.route('/crearJugador', methods=['POST', 'GET'])(self.crearJugador)
        self.app.route('/crearEquipo', methods=['POST', 'GET'])(self.crearEquipo)
        self.app.route('/verFiesta', methods=['POST'])(self.verFiesta)
        self.app.route('/accionEvento', methods=['POST'])(self.accionEvento)
        self.app.route('/reestablecerContrasenna', methods=['POST'])(self.reestablecerContrasenna)

    # Metodo privado para formatear el tiempo del servidor
    def __formatoServidorTiempo(self):
        # Obtiene el tiempo local del servidor
        servidorTiempo = time.localtime()
        # Formatea el tiempo en formato hora minuto segundo
        return time.strftime("%I:%M:%S %p", servidorTiempo)

    # Metodo privado que obtiene los datos de una lista de objetos de Eventos (Fiesta, Concierto o Match)
    # Utiliza el metodo mostrarLista para obtener la cadena y luego la divide en una lista
    # Esta lista luego sera llevada a un html para ser mostrada en distintos campos al ver el evento
    def __listaDatosEventos(self, listaEventosObjetos):
        listaDatosEventos = []
        for evento in listaEventosObjetos:
            idEvento = evento.getID()
            cadena = evento.mostrarLista()
            listaEvento = cadena.split("$&$")
            # Esto servira para ser mostrado en el html
            listaEvento.insert(0, idEvento)
            listaDatosEventos.append(listaEvento)
        return listaDatosEventos

    # Metodo privado para obtener el grafico de barras con los diez eventos mas asistidos
    # listaOrdenada es una lista de diccionarios que contiene informacion sobre las fiestas
    # Cada diccionario contiene dos claves, 'c' para la cantidad de asistenes y 'f' para los nombres de las fiestas
    # Retorna la imagen codificada en str que representa la imagen del grafico codificado en base64
    def __graficoBarrasMasAsistentes(self, listaOrdenada):
        # Crea una nueva figura
        plt.figure()
        # Extrae la cantidad de asistentes y los nombres de las fiestas de la lista ordenada
        cantidadesAsistentes = [fiesta['c'] for fiesta in listaOrdenada[:10]]
        nombresFiestas = [fiesta['f'] for fiesta in listaOrdenada[:10]]
        # Crea el grafico de barras
        plt.bar(nombresFiestas, cantidadesAsistentes)
        # Etiqueta los ejees y le da un titulo al grafico
        plt.xlabel('Nombre de la Fiesta')
        plt.ylabel('Cantidad de Asistentes')
        plt.title('Cantidad de Asistentes por Fiesta')
        # Se obtiene la figura actual
        fig = plt.gcf()
        # Crea un objeto BytesIO para guardar la imagen
        output = io.BytesIO()
        # Guarda la figura en el objeto BytesIO
        fig.savefig(output, format='png')
        # Cierra la figura para liberar memoria
        plt.close()
        # Codifica la imagen en base64 y la decodifica en una cadena
        imagenCodificada = base64.b64encode(output.getvalue()).decode('utf-8')
        # retorna la imagen
        return imagenCodificada

    # Metodo privado para generar un grafico de Torta con las 10 fiestas mas asistidas
    # listaOrdenada es una lista de diccionarios que contiene informacion sobre las fiestas
    # Cada diccionario contiene dos claves, 'c' para la cantidad de asistenes y 'f' para los nombres de las fiestas
    # Retorna la imagen codificada en str que representa la imagen del grafico codificado en base64
    def __graficoTortaMasAsistentes(self, listaOrdenada):
        # Crea una nueva figura
        plt.figure()
        # Extrae la cantidad de asistentes 
        asistentes = []
        nombreFiesta = []
        #listaOrdenada es una lista de diccionarios que alberga 'c'=cant de asistentes 'f'=nombre de la fiesta
        for nombreCant in listaOrdenada:
            asistentes.append(nombreCant['c'])
            nombreFiesta.append(nombreCant['f'])
        plt.pie(asistentes, labels=nombreFiesta, autopct="%0.1f %%")
        plt.title(f"Fiestas Con Más Asistentes")
        plt.legend()
        plt.axis("equal")
        # Se obtiene la figura actual
        fig = plt.gcf()

        output = io.BytesIO()
        # Guarda la figura en el objeto BytesIO
        fig.savefig(output, format='png')
        plt.close()
        # objeto de io.BytesIO que contiene los datos de la imagen
        imagenCodificada = base64.b64encode(output.getvalue()).decode('utf-8')
        return imagenCodificada

    # Este metodo privado obtiene los diccionarios con sus ids rescatados de lista de diccionarios Pyre
    def __obtenerDictConIds(self, listaDictPyre, clave):
        listaDict = []
        for dictPyre in listaDictPyre:
            dictNuevo = dictPyre.val()
            dictNuevo[clave] = dictPyre.key()
            listaDict.append(dictNuevo)
        return listaDict
    # Metodo privado para crear objetos de tipo Artista
    def __crearObjetosArtista(self, listaDict):
        listaArtista = []
        for diccio in listaDict:
            # instacia de cada artista por el diccionario que contiene los valores de sus atributos
            artistaNuevo = Artista(**diccio)
            listaArtista.append(artistaNuevo)
        return listaArtista
    # Metodo privado para crear objetos de tipo Banda
    def __crearObjetosBanda(self, listaDict):
        listaBanda = []
        for diccio in listaDict:
            # inicializa una lista vacia de artistas
            listaArtista = []
            for integrante in diccio['integrantes']:
                # realiza una instancia de cada artista por el dni de estos consiguiendo sus datos
                artista = Artista(**integrante)
                listaArtista.append(artista)
            # se guardan los objetos artista en una lista en la clave integrantes
            diccio['integrantes'] = listaArtista
            # se realiza una instancia de la clase Banda con los datos en el diccio
            bandaNueva = Banda(**diccio)
            listaBanda.append(bandaNueva)
        return listaBanda
    # metodo privado para crear objetos de tipo Fiesta
    def __crearObjetosFiesta(self, listaDict):
        listaFiesta = []
        for diccio in listaDict:
            if 'bandas' in diccio:
                # Se obtienen los diccionarios de tipo Banda
                bandas = self.firebase.obtenerListaDiccionarios('Bandas', diccio['bandas'])
                # En la lista de bandas utiliza el metodo crearObjetosBandas para crear las bandas y guardarlas en la lista
                listaBanda = self.__crearObjetosBanda(bandas)
                diccio['bandas'] = listaBanda
            fiestaNueva = Fiesta(**diccio)
            # en la listaFiesta agrega el objeto Fiesta creado
            listaFiesta.append(fiestaNueva)
        return listaFiesta
    # Metodo publico que se acciona al apretar alguno de los botones cuando se visualiza un Evento de tipo Fiesta
    def accionEvento(self):
        # obtiene la accion que puede ser asistir, noAsistir o editar
        accion = request.form.get('accion')
        # Transforma los datos a un diccionario
        datos = request.form.to_dict()
        # Obtiene el ID del evento y el DNI del usuario
        idFiesta = datos.get('idEvento')
        dni = datos.get('dni')
        # Obtiene la fiesta especifica por su idFiesta en formato diccionario Pyre
        listaFiestaDictPyre = self.firebase.obtenerListaDiccionarios("Fiestas", [idFiesta])
        listaFiestaDictPyre = listaFiestaDictPyre[0]
        fiestaDict = listaFiestaDictPyre.val()
        # Lo transforma a un diccionario normal con la clave id guardando el idFiesta
        fiestaDict['id'] = idFiesta
        # Crea el objeto fiesta
        fiestaObj = self.__crearObjetosFiesta([fiestaDict])
        fiestaObj = fiestaObj[0]
        if(accion=='asistir'):
            # Si apreto el boton de asistencia entonces marca la asistencia del usuario en la fiesta
            fiestaObj.setAsistente(dni, self.firebase)
            # Envia el mensaje al html por medio de flash
            flash(f"¡Ahora asiste a la fiesta '{fiestaDict['nombre']}'!", 'evento')
        elif(accion == "noAsistir"):
            # Si apreto el boton de eliminar asistentcia, entonces quita la asistencia de ese usuario de la fiesta
            fiestaObj.eliminarAsistente(dni, self.firebase)
            # Envia el mensaje al html por medio de flash
            flash(f"Ya no asiste a la fiesta '{fiestaDict['nombre']}'.", 'evento')
        elif(accion=='editar'):
            # Obtiene todos los datos y los cambia si estos son distintos al apretar el boton de editar
            nombre = datos.get('nombre')
            descripcion = datos.get('descripcion')
            fecha = datos.get('fecha')
            fechaFin = datos.get('fechaFin')
            # Descripcion de la ubicacion
            ubicacion = datos.get('ubicacionD')
            latitud = datos.get('latitud')
            longitud = datos.get('longitud')
            precio = datos.get('precio')
            capacidad = datos.get('capacidad')
            edadMin = datos.get('edadMin')
            edadMax = datos.get('edadMax')
            vestimenta = datos.get('vestimenta')
            categoria = datos.get('categoria')
            bar = datos.get('bar')
            conservadora = datos.get('conservadora')
            if(nombre!=fiestaObj.getNombre() and nombre!=""):
                fiestaObj.setNombre(nombre, self.firebase)
            if(descripcion!=fiestaObj.getDescripcion() and descripcion!=""):
                fiestaObj.setDescripcion(descripcion, self.firebase)
            if(fecha!=fiestaObj.getFecha()):
                fiestaObj.setFecha(fecha, self.firebase)
            if(fechaFin!=fiestaObj.getFechaFin()):
                fiestaObj.setFechaFin(fechaFin, self.firebase)
            
            fiestaObj.setUbicacion([latitud, longitud, ubicacion], self.firebase)

            if(precio!=fiestaObj.getPrecio() and precio!=""):
                fiestaObj.setPrecio(precio, self.firebase)
            if(capacidad!=fiestaObj.getCapacidad() and capacidad!=""):
                fiestaObj.setCapacidad(capacidad, self.firebase)
            if(edadMin<edadMax):
                fiestaObj.setRango([edadMin, edadMax], self.firebase)
            if(vestimenta!=fiestaObj.getVestimenta() and vestimenta!=""):
                fiestaObj.setVestimenta(vestimenta, self.firebase)
            if(categoria!=fiestaObj.getCategoria() and categoria!=""):
                fiestaObj.setCategoria(categoria, self.firebase)
            if(bar!=fiestaObj.getBar()):
                fiestaObj.setBar(bar, self.firebase)
            if(conservadora!=fiestaObj.getConservadora()):
                fiestaObj.setConservadora(conservadora, self.firebase)
            # Envia el mensaje al html por medio de flash
            flash("La fiesta ha sido modificada con los valores nuevos.", 'evento')
        elif(accion=='eliminar'):
            # Eliminar la fiesta al apretar el boton de eliminar
            self.firebase.eliminarDiccionario("Fiestas", idFiesta)
            # Envia el mensaje al html por medio de flash
            flash("La fiesta ha sido eliminada de la base de datos", 'evento')
        usuarioValido = self.firebase.obtenerListaDiccionarios("Usuarios", [dni])
        usuarioValido = usuarioValido[0]
        # usuarioValido seria el usuario de tipo diccionario
        usuarioValido = usuarioValido.val()
        # usuarioObjeto seria el usuario de tipo objeto
        # Pone al child como una clave valor mas para la creacion del objeto Usuario
        usuarioValido['dni'] = dni
        # Crea el usuario a partir del diccionario
        usuarioObjeto = Usuario(**usuarioValido)
        # Vuelve a la pantalla de inicio
        context = { 'server_time': self.__formatoServidorTiempo(), 'dni':dni, 'usuario': usuarioValido, 'usuarioObjeto': usuarioObjeto}
        return render_template('jodappInicio.html', context=context)

    def verFiesta(self):
        idFiesta = request.form.get('id')
        dni = request.form.get('dni')
        creador = request.form.get('creador')
        print("creador: ddd", creador)
        asistencia = "NO"
        #creador = "NO"
        if(creador=="SI"):
            listaFiestas = self.firebase.recuperarTodosDict("Fiestas", dni)
        elif(creador=="NO"):
            listaFiestas = self.firebase.recuperarTodosDict("Fiestas", dni, True)
            if(listaFiestas==[]):
                listaFiestas = self.firebase.obtenerTodosDictConKey('Fiestas')
        elif(creador=="NOOO"):
            listaFiestas = self.firebase.obtenerTodosDictConKey('Fiestas')
        listaObjFiestas = self.__crearObjetosFiesta(listaFiestas)
        fiestaObj = ""
        anfitrion = ""
        for fiesta in listaObjFiestas:
            if(fiesta.getID()==idFiesta):
                anfitrion = fiesta.getAnfitrion()
                #if(anfitrion == dni):
                #    creador = "SI"
                listaAsis = fiesta.getAsistentes()
                if dni in listaAsis:
                    asistencia = "SI"
                fiestaObj = fiesta
                break
        #fiestaPyre = self.firebase.obtenerListaDiccionarios("Fiestas", [idFiesta])
        
        dictFiesta = fiestaObj.objetoToDiccionario()
        dictFiesta['id'] = idFiesta
        #listaDatosFiestas = self.__listaDatosEventos(listaObjFiestas)
        context = { 'server_time': self.__formatoServidorTiempo(), 'fiesta':dictFiesta, 'evento':"Fiesta", 'dni':dni, 'dniCreador':anfitrion, 'asistencia':asistencia}
        return render_template('jodappVerEvento.html', context=context)

    def crearEvento(self):
        diccioDatos = request.form.to_dict()
        evento = diccioDatos.get('tipoEvento')
        ubicacionDescrip = diccioDatos.get('ubicacionD')
        ubicacionLatitud = diccioDatos.get('latitud')
        ubicacionLongitud = diccioDatos.get('longitud')
        nombre = diccioDatos.get('nombre')
        descripcion = diccioDatos.get('descripcion')
        fecha = diccioDatos.get('fecha')
        fechaFin = diccioDatos.get('fechaFin')
        precio = diccioDatos.get('precio')
        capacidad = diccioDatos.get('capacidad')
        edadMin = diccioDatos.get('edadMin')
        edadMax = diccioDatos.get('edadMax')
        dni = request.form.get('dni')
        if edadMin is None or edadMax is None:
            condiRango = False
        else:
            condiRango = edadMin>edadMax
        condiEvento = not ubicacionDescrip or not ubicacionLatitud or not ubicacionLongitud or not nombre or not descripcion or not fecha or not fechaFin or not precio or not capacidad or not edadMin or not edadMax or condiRango
        if(evento=='Fiesta'):
            vestimenta = diccioDatos.get('vestimenta')
            categoria = diccioDatos.get('categoria')
            #bar = diccioDatos.get('bar')
            #artistas = request.form.get('listaArtistaIds').split(',')
            # debo ver que error tiene las listaBandaIds diccioDatos.get('listaBandaIds').split(',')
            bandas = request.form.get('listaBandaIds').split(',')
            #flash(bandas, 'evento')
            condiEvento = condiEvento or not vestimenta or not categoria
        elif(evento=='Concierto'):
            print("Concierto")
            bandas = request.form.get('listaBandaIds').split(',')
            condiEvento= condiEvento or not vestimenta or not categoria or bandas==['']
        elif(evento=='Match'):
            equipos = request.form.get('listaEquipoIds')
            condiEvento = condiEvento or equipos==[]
            print("Match")
        
        if(condiEvento):
            # Se muestran los errores con flash
            if(not ubicacionDescrip):
                flash("La descripción de la ubicación no puede estar vacía.", 'evento')
            if(not ubicacionLatitud or not ubicacionLongitud):
                flash("Debe seleccionar una ubicación en el mapa.", 'evento')
            if(not nombre):
                flash("El nombre del evento no puede estar vacío.", 'evento')
            if(not descripcion):
                flash("La descripción del evento no puede estar vacía.", 'evento')
            if(not fecha):
                flash("Debe seleccionar una fecha de inicio.", 'evento')
            if(not fechaFin):
                flash("Debe seleccionar una fecha de finalización.", 'evento')
            if(not precio):
                flash("El precio debe ser 0 o mayor.", 'evento')
            if(not capacidad):
                flash("La capacidad no puede estar vacía.", 'evento')
            if(not edadMin):
                flash("La edad mínima no puede estar vacía", 'evento')
            if(not edadMax):
                flash("La edad máxima no puede estar vacía", 'evento')
            if(condiRango):
                flash("La edad mínima no puede ser mayor a la edad máxima", 'evento')
            if(evento=='Fiesta'):
                if(not vestimenta):
                    flash("La vestimenta no puede estar vacía.", 'evento')
                if(not categoria):
                    flash("La categoria no puede estar vacía.", 'evento')
            elif(evento=='Concierto'):
                print("errores concierto")
            elif(evento=='Match'):
                print("errores match")
        else:
            # Se puede crear el evento
            diccioDatos['rango'] = [edadMin, edadMax]
            del diccioDatos['edadMin']
            del diccioDatos['edadMax']
            
            diccioDatos['anfitrion'] = dni
            diccioDatos['ubicacion'] = [ubicacionLatitud, ubicacionLongitud, ubicacionDescrip]
            if(evento=='Fiesta'):

                if(bandas!=['']):
                    diccioDatos['bandas'] = diccioDatos['listaBandaIds']
                else:
                    diccioDatos['bandas'] = None
                diccioFiesta = diccioDatos
                del diccioFiesta['dni']
                del diccioFiesta['listaBandaIds']
                del diccioFiesta['tipoEvento']
                del diccioFiesta['ubicacionD']
                del diccioFiesta['usuario']
                del diccioFiesta['usuarioObjeto']
                # Se guarda en la bd firebase
                self.firebase.guardarDiccionario("Fiestas", diccioFiesta)
                flash(f"¡Felicidades, la fiesta {nombre} se creo exitosamente!", 'evento')
            elif(evento=='Concierto'):
                print("crear concierto")
                #conciertoNuevo = Concierto(**diccioDatos)
            elif(evento=='Match'):
                print("crear match")
                #matchNuevo = Match(**diccioDatos) 1234
        dictGrupo, dictPerso = self.listGrupoIntegrantes(evento)
        usuarioDict = diccioDatos.get('usuario')
        usuarioObj = diccioDatos.get('usuarioObj')
        context = { 'server_time': self.__formatoServidorTiempo(), 'usuario':usuarioDict, 'dni':dni, 'usuarioObjeto':usuarioObj, 'evento':evento, 'dictGrupo':dictGrupo, 'dictPerso': dictPerso }
        return render_template('jodappCrearEvento.html', context=context)


    def crearBanda(self):
        diccioDatos = request.form.to_dict()
        
        evento = diccioDatos.get('tipoEvento')
        # Recupera el nombre y el genero, sino se ingresaron devuelven None
        nombre = diccioDatos.get('nombreB')
        genero = diccioDatos.get('generoB')
        # Recupera la lista de artistas de la sesión
        # si listaArtistaIds no existe en el diccionario diccioDatos, devuelve una lista vacia
        print(request.form.get('listaArtistaIds'))
        artistas = request.form.get('listaArtistaIds').split(',')
        condi = not nombre or not genero or artistas==['']
        if(condi):
            if(not nombre):
                flash("El nombre de la banda no puede estar vacío", 'banda')
            if(not genero):
                flash("El género de la banda no puede estar vacío.", 'banda')
            if(artistas==['']):
                flash("La banda debe tener al menos un artista agregado.", 'banda')
        else:
            #print(f"ARTISTAS:: {artistas}")
            artistasDictPyre = self.firebase.obtenerListaDiccionarios("Artistas", artistas)
            artistasDict = self.__obtenerDictConIds(artistasDictPyre, "dni")
            artistasObj = self.__crearObjetosArtista(artistasDict)
            #print(lista[0].key())
            #print(lista[1].val())
            diccioBanda = {'nombre':nombre, 'genero':genero, 'integrantes':artistasObj}
            # Se crea un objeto de tipo Banda 
            bandaNueva = Banda(**diccioBanda)
            diccioBanda['integrantes'] = artistasDict
            self.firebase.guardarDiccionario("Bandas", diccioBanda)
            flash(f"¡Felicidades, la banda {nombre} se creo exitosamente!", 'banda')

        dictGrupo, dictPerso = self.listGrupoIntegrantes(evento)
        usuarioDict = diccioDatos.get('usuario')
        usuarioObj = diccioDatos.get('usuarioObj')
        context = { 'server_time': self.__formatoServidorTiempo(), 'usuario':usuarioDict, 'usuarioObjeto':usuarioObj, 'evento':evento, 'dictGrupo':dictGrupo, 'dictPerso': dictPerso }
        return render_template('jodappCrearEvento.html', context=context)



    def crearArtista(self):
        diccioDatos = request.form.to_dict()
        evento = diccioDatos.get('tipoEvento')
        dni = diccioDatos.get('dni')
        nombre = diccioDatos.get('nombre')
        apellido = diccioDatos.get('apellido')
        edad = diccioDatos.get('edad')
        talento = diccioDatos.get('talento')
        condi = not dni or not nombre or not apellido or not edad or not talento
        if(condi):
            if(not nombre):
                flash("El nombre del artista no puede estar vacío.", 'artista')
            if(not dni):
                flash("El DNI del artista no puede estar vacío.", 'artista')
            if(not apellido):
                flash("El apellido del artista no puede estar vacío.", 'artista')
            if(not edad):
                flash("La edad del artista no puede estar vacía.", 'artista')
            if(not talento):
                flash("El talento del artista no puede estar vacío.", 'artista')
        else:
            artistaNew = Artista(**diccioDatos)
            diccioArtista = artistaNew.objetoToDiccionario()
            self.firebase.guardarDiccionario("Artistas", diccioArtista, dni)
            flash(f"¡Felicidades, el artista {nombre} se creo exitosamente!", 'artista')

        dictGrupo, dictPerso = self.listGrupoIntegrantes(evento)
        usuarioDict = diccioDatos['usuario']
        usuarioObj = diccioDatos['usuarioObj']
        context = { 'server_time': self.__formatoServidorTiempo(), 'usuario':usuarioDict, 'usuarioObj':usuarioObj, 'evento':evento, 'dictGrupo':dictGrupo, 'dictPerso': dictPerso }
        return render_template('jodappCrearEvento.html', context=context)


    def crearJugador(self):
        evento = request.form['tipoEvento']
        diccioDatos = request.form.to_dict()
        self.creacionEvento(evento)

    def crearEquipo(self):
        evento = request.form['tipoEvento']
        self.creacionEvento(evento)

    # Serian los eventos creados y eventos asistidos del usuario
    def verListaDeSusEventos(self):
        dni = request.form['dni']

        listaFiestas = self.firebase.recuperarTodosDict("Fiestas", dni)
        listaObjFiestas = self.__crearObjetosFiesta(listaFiestas)
        listaDatosFiestas = self.__listaDatosEventos(listaObjFiestas)

        listaFiestasAsis = self.firebase.recuperarTodosDict("Fiestas", dni, True)
        listaObjFiestasAsis = self.__crearObjetosFiesta(listaFiestasAsis)
        listaDatosFiestasAsis = self.__listaDatosEventos(listaObjFiestasAsis)


        listaConciertos = self.firebase.recuperarTodosDict("Conciertos", dni)
        listaObjConciertos = self.__crearObjetosFiesta(listaConciertos)
        listaDatosConciertos = self.__listaDatosEventos(listaObjConciertos)

        listaConciertosAsis = self.firebase.recuperarTodosDict("Conciertos", dni, True)
        listaObjConciertosAsis = self.__crearObjetosFiesta(listaConciertosAsis)
        listaDatosConciertosAsis = self.__listaDatosEventos(listaObjConciertosAsis)


        listaMatchs = self.firebase.recuperarTodosDict("Matchs", dni)
        listaObjMatchs = self.__crearObjetosFiesta(listaMatchs)
        listaDatosMatchs = self.__listaDatosEventos(listaObjMatchs)
        
        listaMatchsAsis = self.firebase.recuperarTodosDict("Matchs", dni, True)
        listaObjMatchsAsis = self.__crearObjetosFiesta(listaMatchsAsis)
        listaDatosMatchsAsis = self.__listaDatosEventos(listaObjMatchsAsis)

        context = { 'server_time': self.__formatoServidorTiempo(), 'dni':dni, 'listasFiestas':listaDatosFiestas, 'listasFiestasAsis':listaDatosFiestasAsis}
        return render_template('jodappListaDeSusEventos.html', context=context)
    
    # Serian todos los eventos que existen
    def verListaEventos(self):
        usuarioDict = request.form['usuario']
        usuarioObj = request.form['usuarioObjeto']
        dni = request.form['dni']
        imagenCodificadaTorta = ""
        imagenCodificadaBarras = ""
        #listaConciertos = self.firebase.recuperarTodosDict("Conciertos")
        #listaMatchs = self.firebase.recuperarTodosDict("Matchs")

        listaFiestas = self.firebase.obtenerTodosDictConKey('Fiestas')
        listaObjFiestas = self.__crearObjetosFiesta(listaFiestas)
        listaDatosFiestas = self.__listaDatosEventos(listaObjFiestas)
        # Ordena la lista segun la cantidad de asistentes que esta guardado en el indice 7
        listaDatosFiestas  = sorted(listaDatosFiestas , key=lambda i: i[7])
        # Crea una nueva lista de diccionarios que se utiliza para los graficos de barra y torta
        listaOrdenada = []
        for fiesta in listaDatosFiestas:
            diccioAux = {'c':fiesta[7], 'f':fiesta[1]}
            listaOrdenada.append(diccioAux)
        listaDatosFiestas  = sorted(listaDatosFiestas , key=lambda i: i[7], reverse=True)
        # Solo el top 10 de las fiestas mas asistidas
        listaOrdenada = listaOrdenada[-10:]
        # Establecemos 'Agg' como el backend de matplotlib. 'Agg' es un backend basado en raster 
        # que no requiere una interfaz gráfica de usuario. 
        # Para evitarnos errores porque generamos graficos desde el servidor
        matplotlib.use('Agg')
        imagenCodificadaTorta = self.__graficoTortaMasAsistentes(listaOrdenada)
        imagenCodificadaBarras = self.__graficoBarrasMasAsistentes(listaOrdenada)
        context = { 'server_time': self.__formatoServidorTiempo(), 'dni':dni, 'listasFiestas':listaDatosFiestas, 'graficoTorta':imagenCodificadaTorta, 'graficoBarra': imagenCodificadaBarras}
        return render_template('jodappListaEventos.html', context=context)

    def listGrupoIntegrantes(self, eventoSeleccionado):
        if(eventoSeleccionado!="Match"):
            # Si es Fiesta o Concierto se guardan bandas y artistas
            dictGrupo = self.firebase.recuperarTodosDict("Bandas")
            dictPerso = self.firebase.recuperarTodosDict("Artistas")
        else:
            # Si es Match se guardan equipos y jugadores
            dictGrupo = self.firebase.recuperarTodosDict("Equipos")
            dictPerso = self.firebase.recuperarTodosDict("Jugadores")
        return [dictGrupo, dictPerso]

    def creacionEvento(self, actualizacion=False):

        if(actualizacion!=False):
            # En el caso de que sea distinta de falsa, quiere decir que tiene el evento seleccionado
            eventoSeleccionado = actualizacion
        else:
            # Obtenemos el tipo de evento que se selecciono para crear (Fiesta, Concierto, Match)
            # En el caso de que la actualizacion sea falsa
            eventoSeleccionado = request.form['tipoEvento']
        dictGrupo, dictPerso = self.listGrupoIntegrantes(eventoSeleccionado)
        usuario = request.form.get('usuario')
        usuarioObjeto = request.form.get('usuarioObjeto')
        dni = request.form.get('dni')
        context = { 'server_time': self.__formatoServidorTiempo(), 'dni':dni, 'usuario':usuario, 'usuarioObjeto':usuarioObjeto, 'evento':eventoSeleccionado, 'dictGrupo':dictGrupo, 'dictPerso': dictPerso }
        return render_template('jodappCrearEvento.html', context=context)
    
    def home(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('index.html', context=context)

    def login(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('login.html', context=context)

    def signup(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('signup.html', context=context)
    
    def reestablecerContrasenna(self):
        correo = request.form.get('correo')
        try:
            self.firebase.autenticacion.send_password_reset_email(correo)
            usuarios = self.firebase.baseDeDatosTR.child("Usuarios").get()
            for usuario in usuarios.each():
                if(usuario.val()['correo'] == correo):
                    nombreUsuario = usuario.val()['user']
                    break
            flash(f"Correo electrónico para reestablecer la contraseña enviado para el usuario: '{nombreUsuario}'.")
        except Exception as e:
            flash("El correo electrónico no existe en la base de datos.")
        # Vuelve a la pantalla de signup con el respectivo mensaje flash
        context = { 'server_time': self.__formatoServidorTiempo() }
        return redirect(url_for('login', context=context))

    def iniciarSesion(self):
        user = request.form.get('username')
        contra = request.form.get('password')
        if not user or not contra:
            if(not user):
                flash("El usuario no puede estar vacío.")
            if(not contra):
                flash("La contraseña no puede estar vacía.")
        else:
            usuarioValido = self.firebase.authIniciarSesionUser(user, contra)
            if(usuarioValido!=False):
                # Se obtiene el usuario en formato diccionario
                flash("¡Felicidades! Ingresaste con éxito")
                dni = usuarioValido
                usuarioValido = self.firebase.obtenerListaDiccionarios("Usuarios", [usuarioValido])
                usuarioValido = usuarioValido[0]
                # usuarioValido seria el usuario de tipo diccionario
                usuarioValido = usuarioValido.val()
                # usuarioObjeto seria el usuario de tipo objeto
                #print(usuarioValido)
                # Pone al child como una clave valor mas para la creacion del objeto Usuario
                usuarioValido['dni'] = dni
                #flash(usuarioValido)
                # Crea el usuario a partir del diccionario
                usuarioObjeto = Usuario(**usuarioValido)
                #flash(usuarioObjeto)
                #print(usuarioObjeto.getAsistencias())
                context = { 'server_time': self.__formatoServidorTiempo(), 'dni':dni, 'usuario': usuarioValido, 'usuarioObjeto': usuarioObjeto}
                return render_template('jodappInicio.html', context=context)
            
            flash("Usuario y/o contraseña incorrectos")
        # Vuelve a la pantalla de signup con el respectivo mensaje flash
        context = { 'server_time': self.__formatoServidorTiempo() }
        return redirect(url_for('login', context=context))
        
    def registrarte(self):
        dni = request.form.get('dni')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        edad = request.form.get('edad')
        correo = request.form.get('correo')
        user = request.form.get('username')
        contra = request.form.get('password')
        contra2 = request.form.get('password2')
        condi = not dni or not nombre or not apellido or not edad or not correo or not user or not contra or not contra2
        if condi:
        #Uno o mas entradas vacias
            if(not dni):
                flash("El DNI no puede estar vacío.")
            if(not nombre):
                flash("El nombre no puede estar vacío.")
            if(not apellido):
                flash("El apellido no puede estar vacío.")
            if(not edad):
                flash("La edad no puede estar vacía.")
            if(not correo):
                flash("El correo no puede estar vacío.")
            if(not user):
                flash("El usuario no puede estar vacío.")
            if(not contra or not contra2):
                flash("Las contraseñas no pueden estar vacías y deben ser iguales.")
        else:
        #Las entradas estan llenas
            bande=False
            if(contra==contra2):
                # Instancia de la clase Usuario
                diccioUsuario = {'dni':dni, 'nombre':nombre, 'apellido':apellido, 'edad':edad, 'correo':correo, 'user':user}
                usuarioObjeto = Usuario(**diccioUsuario)
                # Lo convierto en diccionario
                usuarioDiccio = usuarioObjeto.objetoToDiccionario()
                # Verifico si es un usuario valido con la base de datos
                usuarioValido = self.firebase.guardarDiccionario("Usuarios", usuarioDiccio, dni, 'user', 'correo')
                if(usuarioValido):
                    #("El usuario se guardo en la bd, por lo tanto es valido, para crear un usuarioAuth (que guarde su correo y contrasenna para autenticarse)")
                    usuarioAuth = self.firebase.authCrearUsuario(correo, contra)
                    if(usuarioAuth!=False):
                        # Deberia poner un mensaje de Felicidades, usuario creado
                        flash("¡Felicidades! Tu usuario ha sido registrado")
                        context = { 'server_time': self.__formatoServidorTiempo() }
                        return render_template('index.html', context=context)
                    bande=True
                else:
                    bande=True
            else:
                flash("Las contraseñas no coinciden.")
            if(bande):
                flash("Usuario y/o correo ya existentes.")

        # Vuelve a la pantalla de registro con el respectivo mensaje flasj
        context = { 'server_time': self.__formatoServidorTiempo() }
        return redirect(url_for('signup', context=context))

    def run(self):
        self.app.run(debug=True)
