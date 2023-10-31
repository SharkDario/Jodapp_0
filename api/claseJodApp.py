#from flask import Flask, render_template, make_response
#import time
#from firebaseConfig import config
#from pyrebase import pyrebase

#firebase=pyrebase.initialize_app(config)
#autenticacion = firebase.auth()
#bd = firebase.database()


#app = Flask(__name__)

#def format_server_time():
#  server_time = time.localtime()
#  return time.strftime("%I:%M:%S %p", server_time)

#@app.route('/')
#def home():
#    context = { 'server_time': format_server_time() }
#    return render_template('index.html', context=context)

#@app.route('/login')
#def login():
#    return render_template('login.html')

#@app.route('/signup')
#def signup():
#    return render_template('signup.html')

#if __name__ == '__main__':
#    app.run()


from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from claseFirebase import Firebase
from claseUsuario import Usuario
import time

class JodApp:
    def __init__(self):
        self.firebase = Firebase()
        self.context = { 'server_time': self.__formatoServidorTiempo() }
        self.app = Flask(__name__)
        self.app.secret_key = "holaMundo"
        self.app.route('/')(self.home)
        self.app.route('/login')(self.login)
        self.app.route('/signup')(self.signup)
        self.app.route('/registrarte', methods=['POST'])(self.registrarte)

    def __formatoServidorTiempo(self):
        servidorTiempo = time.localtime()
        return time.strftime("%I:%M:%S %p", servidorTiempo)
    
    def home(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('index.html', context=context)

    def login(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('login.html', context=context)

    def signup(self):
        context = { 'server_time': self.__formatoServidorTiempo() }
        return render_template('signup.html', context=context)
    
    def registrarte(self):
        entradas = ['dni', 'nombre', 'apellido', 'edad', 'correo', 'user', 'contra', 'contra2']
        
        if not all(request.form.get(entrada) for entrada in entradas):
        #Uno o mas entradas vacias
            flash("Una o más entradas están vacías.")
        else:
        #Los campos estan llenos
            dni = request.form.get('dni')
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            edad = request.form.get('edad')
            correo = request.form.get('correo')
            user = request.form.get('username')
            contra = request.form.get('password')
            contra2 = request.form.get('password2')
            if(contra==contra2):
                # Instancia de la clase Usuario
                usuarioObjeto = Usuario(dni, nombre, apellido, edad, correo, user)
                # Lo convierto en diccionario
                usuarioDiccio = usuarioObjeto.objetoToDiccionario()
                # Verifico si es un usuario valido con la base de datos
                usuarioValido = self.firebase.guardarDiccionario("Usuarios", usuarioDiccio, dni, 'user', 'correo')
                if(usuarioValido):
                    #("El usuario se guardo en la bd, por lo tanto es valido, para crear un usuarioAuth (que guarde su correo y contrasenna para autenticarse)")
                    usuarioAuth = self.firebase.authCrearUsuario(correo, contra)
                    if(usuarioAuth!=False):
                        # Deberia poner un mensaje de Felicidades, usuario creado
                        context = { 'server_time': self.__formatoServidorTiempo() }
                        return render_template('index.html', context=context)
                else:
                    flash("Usuario y/o correo ya existentes.")
            else:
                flash("Las contraseñas no coinciden.")

        # Vuelve a la pantalla de registro con el respectivo mensaje flasj
        context = { 'server_time': self.__formatoServidorTiempo() }
        return redirect(url_for('signup', context=context))

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    JodApp().run()
