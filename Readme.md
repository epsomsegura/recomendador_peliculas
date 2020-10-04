# Recomendador de películas
## Dependencias Python
- Pandas

```terminal 
pip install pandas
```

- Numpy

```terminal 
pip install numpy
```

- Flask

```terminal 
pip install flask
```
- SQLAlchemy

```terminal
pip install sqlalchemy
```
- Flask-SQLAlchemy

```terminal
pip install flask-sqlalchemy
````
```terminal
pip install pymysql
```

- Bcrypt
````
pip install bcrypt
```


## Manejador de base de datos
- MySQL/MariaDB

## Estructura del proyecto
- `controllers`: Almacena los controladores de funcionalidad, estan creados de forma semántica para alojar la funcionalidad de las distintas entidades que intervienen en la operación de este proyecto
    - `userController`: Controlador relacionado con la funcionalidad de los usuarios
- `models`: Almacena los modelos de las entidades utilizadas en base de datos, mismos que representan a las entidades que intervienen en la operación de este proyecto
    `- users`: Modelo que representa a la entidad usuarios
- `static`: Almacena los recursos estáticos correspondientes a la parte visual del proyecto, como lo son imagenes, fuentes, hojas de estilo y javascript
    - `assets`: Directorio principal
    - `assets/bootstrap`: Almacena el CSS y JS del <i>framework</i> para <i>FrontEnd Bootstrap</i>
    - `assets/css`: Almacena el CSS de las vistas creadas para este proyecto 
    - `assets/fonts`: Almacena las fuentes utilizadas para este proyecto, incluyendo las fuentes especiales <i>FontAwesome</i>
    - `assets/img`: Almacena las imágenes utilizadas para dar vista a distintas secciones de este proyecto
    - `assets/js`:  Almacena los archivos JS utilizados para la funcionalidad de este proyecto
- `templates`: Almacena los archivos correspondientes a la construcción de la vista que se presenta al usuario, se almacenan los distintos <i>layouts</i> y <i>ventanas</i> utilizados en este proyecto
    - `index.html`: Archivo de la vista principal
    - `dashboard`: Almacena los archivos del dashboard, calificaciones y recomendaciones, mismos que son presentados al usuario accediendo a la ruta asignada a cada vista
    - `layouts`: Almacena los archivos de plantillas mediante los cuales se despliegan los otros ficheros de visualización contenidos en el directorio `templates`
    - `users`: Almacena los archivos de vista relacionados con los usuarios de este proyecto

## Notas
- Los ficheros CSV fueron modificados en las columnas `release_date` desde Microsoft Excel para asignar el año a cuatro dígitos en lugar de dos dígitos

## Despliegue
Una vez instaladas las dependencias es posible ejecutar este proyecto mediante el comando:

```terminal 
python main.py
```

## Autor
Epsom Enrique Segura Jaramillo

segurajaramilloepsom@gmail.com