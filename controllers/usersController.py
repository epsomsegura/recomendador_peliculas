import bcrypt, json,logging
from datetime import date, datetime, timedelta
from sqlalchemy import exc, inspect

# Modelos
from models.database import db
from models.users import Users as U

class usersController:
    def login(self,data):
        try:
            user_login = U.query.filter_by(email=data['email']).all()
            if(len(user_login)>1):
                return {'response':'DUPLICADOS'}
            elif(len(user_login)==0):
                return {'response':'NOUSER'}
            elif(len(user_login)==1):
                user_data = user_login[0]
                if bcrypt.checkpw(str.encode(data['password']), str.encode(user_data.password)):
                    return {
                        'response': "OK",
                        'session_data' : user_data.as_dict()
                    }
                else:
                    return {'response':'PASSWORD'}

        except Exception as e:
            return 'NO'

    
    def registration(self, data):
        password = bcrypt.hashpw(str.encode(data['password']), bcrypt.gensalt())
        terms = True if data['terms']==1 else False
        created_at = datetime.now()

        if(data['password']!=data['password2']):
            return {'response':'Error','message':'Las contraseñas no coinciden'}
        else:
            try:
                new_user = U(None,data['username'],data['email'],password,data['city'],terms,created_at,None)

                db.session.add(new_user)
                db.session.commit()

                return {'response':'OK','new_id':new_user.id}
            except exc.SQLAlchemyError as e:
                msg = ""
                error_code = int((e.args[0].split(') (')[1]).split(', "')[0])
                if(error_code == 1062):
                    msg = "Correo electrónico duplicado, por favor intente con otro"
                else:
                    msg = (((e.args[0]).split(') (')[1]).split(', "')[1]).replace(')','')
                db.session.rollback()
                return {'response':'Error','message':msg}