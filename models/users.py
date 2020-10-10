# DEPENDENCIA DE INICIO DE ORM
from models.database import db

# Modelo 'Users'
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(150))
    username = db.Column('username',db.String(250),unique=True)
    email = db.Column('email',db.String(100),unique=True)
    password = db.Column('password',db.Text)
    terms = db.Column('terms',db.Boolean)
    created_at = db.Column('created_at',db.DateTime)
    updated_at = db.Column('updated_at',db.DateTime)

    def __init__ (self,id,name,username,email,password,terms,created_at,updated_at):
        self.name = name
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.terms = terms
        self.created_at = created_at
        self.updated_at = updated_at

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}