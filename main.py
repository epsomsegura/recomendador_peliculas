# DEPENDENCIES
from flask import Flask, render_template, request, redirect, url_for, session
from models.database import db
import json

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'@movies_2019$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# CONTROLLERS
from controllers.usersController import usersController as uC

# ROUTES
# LOGIN
@app.route("/", methods=['GET','POST'])
def index():
    if(request.method=='POST'):
        login = uC.login(app,request.form.to_dict())
        if(login['response'] == 'OK'):
            session['user'] = login['session_data']
            return redirect(url_for('.dashboard'))
        elif(login['response'] == 'PASSWORD'):
            return redirect(url_for('.index', alert="La contraseña es incorrecta"))
        elif(login['response'] == 'NOUSER'):
            return redirect(url_for('.index', alert="El usuario no existe"))
        else:
            return redirect(url_for('.index', alert="Error desconocido"))
    elif(request.method == 'GET'):
        alert = request.args.get('alert')
        return render_template("index.html",alert=alert)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/recuperar_password',methods=['POST','GET'])
def recuperar_password():
    if(request.method == 'POST'):
        return 'HOLA'
    elif(request.method == 'GET'):
        return render_template('users/password_recovery.html')



@app.route("/registro", methods=['GET','POST'])
def registro():
    if(request.method == 'POST'):
        registration = uC.registration(app,request.form.to_dict())
        if(registration['response']=='OK'):
            return redirect(url_for('.index',message="Usuario creado con éxito"))
        else:
            return redirect(url_for('.registro', alert=registration['message']))
        return uC.registration(app,request.form.to_dict())
    elif(request.method == 'GET'):
        alert = request.args.get('alert')
        return render_template("users/register.html",alert=alert)




# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if(session.get('user') != None):
        return render_template("dashboard/dashboard.html")
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)