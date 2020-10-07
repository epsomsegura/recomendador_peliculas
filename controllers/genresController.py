# DEPENDENCIAS
from datetime import date, datetime, timedelta
from sqlalchemy import exc, inspect

# Modelos
from models.database import db
from models.genres import Genres as G

# CLASE CONTROLADOR DE GÉNEROS
class genresController:
    # Obtener todos los géneros desde la base de datos
    def getAll(self):
        data = G.query.all()

        return {
            'response': "OK",
            'genres' : data
        }