# DEPENDENCIAS
import json, datetime
from flask import Flask, render_template, request, Response, redirect, url_for, session, jsonify
from ast import literal_eval

# DEPENDENCIAS PARA EL MANEJO DE MODELOS
from models.database import db

# CONFIGURACIONES PARA EL MANEJO DE LOS TEMPLATES (VISTAS)
app = Flask(__name__, static_url_path='/static')
# CONFIGURACIONES PARA EL MANEJO DE LAS SESIONES
app.permanent_session_lifetime = datetime.timedelta(hours=1)
# CONFIGURACIONES PARA LA CONEXIÓN A LA BASE DE DATOS
app.secret_key = b'@movies_2019$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# IMPORTACIÓN DE LOS CONTROLADORES
from controllers.usersController import usersController as uC
from controllers.genresController import genresController as gC
from controllers.moviesController import moviesController as mC
from controllers.categoriesController import categoriesController as catC
from controllers.ratingsController import ratingsController as ratC




# INSTANCIAS A CONTROLADORES ESPECIALES
catC=catC()     #   CONTROLADOR DE RECOMENDACIONES POR CATEGORÍAS
ratC=ratC()     #   CONTROLADOR DE RECOMENDACIONES POR CALIFICACIONES




# RUTAS PARA LA APLICACIÓN WEB
# RUTA PARA INICIAR SESIÓN
@app.route("/", methods=['GET','POST'])
def index():
    # RETORNA LA VISTA DE INICIO DE SESIÓN
    if(request.method == 'GET'):
        alert = request.args.get('alert')
        return render_template("index.html",alert=alert)
    # RECIBE LA PETICIÓN PARA INICIO DE SESIÓN
    elif(request.method=='POST'):
        # EJECUTA LA FUNCIÓN DE INICIO DE SESIÓN DESDE EL CONTROLADOR 'USUARIOS'
        login = uC.login(app,request.form.to_dict())
        # SI LA AUTENTICACIÓN ES CORRECTA RETORNA LA RESPUESTA 'OK' y LOS DATOS DEL USUARIO PARA CREAR UNA COOKIE DE SESIÓN, POSTERIORMENTE REDIRECCIONA A LA VISTA PRINCIPAL DE LA APLICACIÓN
        if(login['response'] == 'OK'):
            session['user'] = login['session_data']
            return redirect(url_for('.dashboard'))
        # SI LA AUTENTICACIÓN RESPONDE CON EL MENSAJE 'PASSWORD' INDICA QUE LA CONTRASEÑA INGRESADA ES INCORRECTA Y NOTIFICA AL USUARIO
        elif(login['response'] == 'PASSWORD'):
            return redirect(url_for('.index', alert="La contraseña es incorrecta"))
        # SI LA AUTENTICACIÓN RESPONDE CON EL MENSAJE 'NOUSER' INDICA QUE EL USUARIO INGRESADO NO EXISTE Y NOTIFICA AL USUARIO
        elif(login['response'] == 'NOUSER'):
            return redirect(url_for('.index', alert="El usuario no existe"))
        # CUALQUIER OTRA RESPUESTA NOTIFICA AL USUARIO CON EL MENSAJE 'Error desconocido'
        else:
            return redirect(url_for('.index', alert="Error desconocido"))

# RUTA PARA CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# RUTA PARA RECUPERAR LA CONTRASEÑA EN CASO DE QUE EL USUARIO LA OLVIDE, SE CREA UNA CONTRASEÑA ALEATORIA PARA INICIAR SESIÓN Y SE SOLICITA QUE SE CAMBIE AL INGRESAR A LA APLICACIÓN
@app.route('/recuperar_password',methods=['POST','GET'])
def recuperar_password():
    # RETORNA LA VISTA DE RECUPERAR CONTRASEÑA
    if(request.method == 'GET'):
        return render_template('users/password_recovery.html')
    # RECIBE LA PETICIÓN PARA CAMBIAR LA CONTRASEÑA
    elif(request.method == 'POST'):
        pass_recovery = uC.pass_recovery(app,request.form.to_dict())
        return jsonify(pass_recovery)

# RUTA PARA REGISTRAR UN NUEVO USUARIO PARA INTERACTUAR CON EL SISTEMA
@app.route("/registro", methods=['GET','POST'])
def registro():
    # RETORNA LA VISTA DE REGISTRO DE NUEVO USUARIO
    if(request.method == 'GET'):
        alert = request.args.get('alert')
        return render_template("users/register.html",alert=alert)
    # RECIBE LA PETICIÓN PARA REGISTRAR UN NUEVO USUARIO
    elif(request.method == 'POST'):
        registration = uC.registration(app,request.form.to_dict())
        if(registration['response']=='OK'):
            return redirect(url_for('.index',message="Usuario creado con éxito"))
        else:
            return redirect(url_for('.registro', alert=registration['message']))

# RUTA PARA EDITAR LOS DATOS DEL PERFIL ACTIVO
@app.route('/perfil',methods=['GET','POST'])
def perfil():
    # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA PRINCIPAL
    if(session.get('user') != None):
        # RETORNA LA VISTA DEL PERFIL DEL USUARIO
        if(request.method=='GET'):
            user_data = session.get('user')
            return render_template("users/profile.html",user_data=user_data)
        # RECIBE LA PETICIÓN PARA ACTUALIZAR LOS DATOS DEL USUARIO ACTIVO
        elif(request.method=='POST'):
            update_user = uC.update_user(app,request.form.to_dict())
            if(update_user['response']=='PASSWORD'):
                return redirect(url_for('perfil', alert="La contraseña es incorrecta"))
            elif(update_user['response']=='OK'):
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('perfil', alert="Error desconocido"))
    # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA DE INICIO DE SESIÓN
    else:
        return redirect(url_for('index'))




# RUTA PARA REDIRECCIONAR A LA VENTANA PRINCIPAL DE LA APLICACIÓN
@app.route("/dashboard", methods=["get"])
def dashboard():
    # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA PRINCIPAL
    if(session.get('user') != None):
        return render_template("dashboard/dashboard.html")
    # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA DE INICIO DE SESIÓN
    else:
        return redirect(url_for('index'))




# RUTA PARA REDIRECCIONAR A LA VENTANA DE CATEGORÍAS
@app.route("/categorias", methods=['GET'])
def categorias():
    if request.method=='GET':
        # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA CATEGORÍAS
        if(session.get('user') != None):
            genres = gC.getAll(app)
            return render_template("dashboard/categories.html",genres = genres['genres'])
        # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA DE INICIO DE SESIÓN
        else:
            return redirect(url_for('index'))




# RUTA PARA REDIRECCIONAR A LA VENTANA CALIFICACIONES
@app.route("/calificaciones", methods=["GET"])
def calificaciones():
    if request.method=='GET':
        # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA CALIFICACIONES
        if(session.get('user') != None):
            movies = mC.getAll(app)
            return render_template("dashboard/rates.html", result=movies)
        # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA DE INICIO DE SESIÓN
        else:
            return redirect(url_for('index'))
      



# RUTA QUE REDIRECCIONA A LA VENTANA RECOMENDACIONES, SE ESPERA EL PARÁMETRO 'tipo' PARA PINTAR LA VENTANA CORRESPONDIENTE
@app.route("/recomendaciones/<tipo>",methods=['POST'])
def recomendaciones(tipo):
    if request.method=='POST':
        # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA RECOMENDACIONES Y ESPERA A LEER EL PARÁMETRO 'tipo'
        if(session.get('user') != None):
            # SE LEE EL PARÁMETRO 'tipo'
            # SI EL PARÁMETRO 'tipo' ES 'categorias' EJECUTA EL ALGORITMO RECOMENDADOR POR CATEGORIAS Y RECIBE UNA RESPUESTA QUE SERÁ PINTADA EN LA VISTA DE RECOMENDACIONES
            if tipo == 'categorias':
                # Se obtienen los parámetros del cuerpo de la petición y se mandan al algoritmo
                data = catC.obtener_recomendaciones('genre',request.form.getlist('categoria'))
                return render_template('dashboard/recommendations.html',result=data, categories=request.form.getlist('categoria'))
            # SI EL PARÁMETRO 'tipo' ES 'calificaciones' EJECUTA EL ALGORITMO RECOMENDADOR POR CALIFICACIONES Y RECIBE UNA RESPUESTA QUE SERÁ PINTADA EN LA VISTA DE RECOMENDACIONES
            elif tipo == 'calificaciones':
                # Se obtienen los parámetros del cuerpo de la petición y se mandan al algoritmo
                titles = request.form.getlist('title')
                rates = request.form.getlist('rating')
                # Se prepara una variable de tipo lista para almacenar los diccionarios de cada 'title' y 'rating' calificados en la vista de calificaciones de películas vistas
                userInput = []
                data = zip(titles,rates)

                for t, r in data:
                    movie = {
                        'title': t,
                        'rating' : r
                    }
                    userInput.append(movie)
                # Se envía la lista al algoritmo
                data = ratC.obtener_recomendaciones(userInput)
                return render_template('dashboard/recommendations.html',result=data, movies=userInput)
            # SI EL PARÁMETRO 'tipo' NO ESTÁ DENTRO DE LOS PERMITIDOS, LA APLICACIÓN RETORNA AL USUARIO A LA VISTA ANTERIOR
            else:
                return redirect(redirect_url())
        else:
            # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA PRINCIPAL
            return redirect(url_for('index'))
    else:
        if(session.get('user') != None):
            # SI LA APLICACIÓN TIENE SESIÓN REDIRECCIONA A LA VENTANA PRINCIPAL
            return redirect(url_for('dashboard'))
        # SI LA APLICACIÓN NO TIENE SESIÓN REDIRECCIONA A LA VENTANA PRINCIPAL
        else:
            return redirect(url_for('index'))




# SE INICIALIZA LA APLICACIÓN
if __name__ == "__main__":
    app.run(debug=True)