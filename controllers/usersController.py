# DEPENDENCIAS
import bcrypt, json,logging
from datetime import date, datetime, timedelta
from sqlalchemy import exc, inspect
import random, string

# MODELOS
from models.database import db
from models.users import Users as U

class usersController:
    # Verificar el inicio de sesión
    def login(self,data):
        try:
            # Ejecuta el query mediante el ORM SQLAlchemy
            user_login = U.query.filter_by(email=data['email']).all()
            # Si el usuario está duplicado
            if(len(user_login)>1):
                return {'response':'DUPLICADOS'}
            # Si el usuario no existe
            elif(len(user_login)==0):
                return {'response':'NOUSER'}
            # Si el usuario existe
            elif(len(user_login)==1):
                user_data = user_login[0]
                # Si la contraseña es correcta
                if bcrypt.checkpw(str.encode(data['password']), str.encode(user_data.password)):
                    return {
                        'response': "OK",
                        'session_data' : user_data.as_dict()
                    }
                # Si la contraseña es incorrecta
                else:
                    return {'response':'PASSWORD'}

        except Exception as e:
            return 'NO'

    # Registro de un nuevo usuario
    def registration(self, data):
        # Variables para registro del nuevo usuario
        password = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
        terms = True if data['terms']==1 else False
        created_at = datetime.now()
        # Si las contraseñas son incorrectas retorna error
        if(data['password']!=data['password2']):
            return {'response':'Error','message':'Las contraseñas no coinciden'}
        # Si las contraseñas son correctas continua el proceso
        else:
            # Ejecuta una transacción para registrar al nuevo usuario y hace el commit
            try:
                new_user = U(None,data['username'],data['email'],password,data['city'],terms,created_at,None)

                db.session.add(new_user)
                db.session.commit()

                return {'response':'OK','new_id':new_user.id}
            # Retorna los posibles errores en caso de que la transacción falle y hace el rollback
            except exc.SQLAlchemyError as e:
                msg = ""
                error_code = int((e.args[0].split(') (')[1]).split(', "')[0])
                if(error_code == 1062):
                    msg = "Correo electrónico duplicado, por favor intente con otro"
                else:
                    msg = (((e.args[0]).split(') (')[1]).split(', "')[1]).replace(')','')
                db.session.rollback()
                return {'response':'Error','message':msg}

    # Actualizar usuario
    def update_user(self,data):
        # Variables para la edición de un usuario
        user_data = U.query.filter_by(email=data['email']).first()
        user_data.email = data['email']
        user_data.username = data['username']
        user_data.city = data['city']
        user_data.updated_at = datetime.now()
        try:
            # Se verifica cambio en las contraseñas
            if(data['chk_pass']=='1'):
                # Si las contraseñas coinciden ejecuta las operaciones necesarias
                if(data['password']==data['password2']):
                    new_pass = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
                    user_data.password = new_pass
                    db.session.commit()
                    return {
                        'response': 'OK'
                    }
                # De lo contrario, retorna un error en la respuesta
                else:
                    db.session.rollback()
                    return {
                        'response': 'PASSWORD'
                    }
            # Si no hay cambios en las contraseñas actualiza los datos recibidos
            else:
                db.session.commit()
                return {
                        'response': 'OK'
                    }
        # Retorna los posibles errores en caso de que la transacción falle y hace el rollback
        except Exception as e:
            db.session.rollback()
            return 'NO'

    # Recuperar contraseña
    def pass_recovery(self, data):
        try:
            # Ejecuta el query mediante el ORM SQLAlchemy
            user_login = U.query.filter_by(email=data['email']).all()
            # Si el usuario está duplicado
            if(len(user_login)>1):
                return {'response':'DUPLICADOS'}
            # Si el usuario no existe
            elif(len(user_login)==0):
                return {'response':'NOUSER'}
            # Si el usuario existe
            elif(len(user_login)==1):
                user_data = user_login[0]
                new_pass = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
                password = bcrypt.hashpw(str.encode(new_pass), bcrypt.gensalt())

                user_data.password = password
                db.session.commit()
                return {
                    'response': 'OK',
                    'password': new_pass,
                }
        except Exception as e:
            db.session.rollback()
            return 'NO'
        
