# DEPENDENCIA DE INICIO DE ORM
from models.database import db

# MODELO 'Genres'
class Genres(db.Model):
    __tablename__ = 'genres'

    id = db.Column('id',db.Integer,primary_key=True)
    genre = db.Column('genre',db.String(250),unique=True)

    def __init__ (self,id,genre):
        self.id = id
        self.genre = genre

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}