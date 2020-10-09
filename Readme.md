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
````


## Manejador de base de datos
- MySQL/MariaDB


## Estructura del proyecto
- `controllers`: Almacena los controladores de funcionalidad, estan creados de forma semántica para alojar la funcionalidad de las distintas entidades que intervienen en la operación de este proyecto:
    - `categoriesController.py`: Controlador relacionado con el tratamiento de los datos y el retorno de las recomendaciones basadas en `categorías` (géneros) seleccionados por el usuario. La recomendación se lleva a cabo mediante el cálculo del `score` con la fórmula de IMDb para calificar películas.
    - `genresController.py`: Controlador relacionado con la funcionalidad de los géneros. Se encarga de retornar desde la base de datos la lista de los géneros utilizados en el recomendador por `categorías`. La funcionalidad de este controlador es el retorno del catálogo de categorías para el módulo `recomendador por categorías`.
    - `moviesController`.py: Controlador relacionado con el tratamiento de los datos y el retorno del catálogo de películas para el módulo de `recomendación por calificaciones`. La funcionalidad de este controlador es el retorno del catálogo de películas a la vista correspondiente.
    - `ratingsController.py`: Controlador relacionado con el tratamiento de los datos y el retorno de las recomendaciones basadas en `calificación` de películas selecconadas y calificadas por el usuario. La recomendación se lleva a cabo mediante el `coeficiente de correlación de Pearson` haciendo uso de los datos recibidos por el usuario y las calificaciones de otros usuarios.
    - `userController.py`: Controlador relacionado con la funcionalidad de los usuarios. Se encarga de realizar las tareas de inicio/cierre de sesión, registro de nuevos usuarios, actualización de los datos del usuario activo y recuperación de contraseña de un usuario. Todas las tareas interactuan con los registros en la base de datos.
- `models`: Almacena los modelos de las entidades utilizadas en base de datos, mismos que representan a las entidades que intervienen en la operación de este proyecto
    - `database.py`: Lanzador de la conexión a la base de datos mediante el ORM `SQLAlchemy`.
    - `genres.py`: Modelo que representa a la entidad `categorías` (géneros).
    - `users`: Modelo que representa a la entidad `usuarios`.
- `src`: 
    - `categories`: 
        - `categories_metadata.csv`: Archivo con los datos después del tratamiento de datos para ejecutar `recomendaciones por categorías`. Se genera a partir del tratamiento de datos del archivo [src/categories/movies_metadata.csv](/src/categories/movies_metadata.csv).
        - `movies_metadata.csv`: DataSet de las películas utilizadas para el tratamiento de datos del `recomendador por categorías`.
    - `ratings`: Directorio que almacena los archivos para la construcción del dataFrame para las `recomendaciones por calificaciones`.
        - `movies_dataset.csv`: Archivo con los datos después del tratamiendo de datos para ejecutar `recomendaciones por calificaciones`. Se genera a partir del tratamiendo de los datos del archivo [src/ratings/movies.csv](/src/ratings/movies.csv), [categories/categories_metadata.csv](/categories/categories_metadata.csv) y el cálculo de los `scores` mediante la fórmula de IMDb.
        - `movies.csv`: Catálogo de películas con datos básicos sin tratamiento.
        - `ratings.csv`: DataSet de la relación entre diversos usuarios, id de las películas del catálogo contenido en `movies.csv` y las calificaciones a estas.
    - `movies.sql`: Script para la creación de la base de datos con las tablas `users`y `genres` junto con el volcado de datos preestablecidos.
- `static`: Almacena los recursos estáticos correspondientes a la parte visual del proyecto, como lo son imagenes, fuentes, hojas de estilo y javascript
    - `assets/bootstrap`: Almacena el CSS y JS del <i>framework</i> para <i>FrontEnd Bootstrap</i>
    - `assets/css`: Almacena el CSS de las vistas creadas para este proyecto 
    - `assets/fonts`: Almacena las fuentes utilizadas para este proyecto, incluyendo las fuentes especiales <i>FontAwesome</i>
    - `assets/img`: Almacena las imágenes utilizadas para dar vista a distintas secciones de este proyecto
    - `assets/js`:  Almacena los archivos JS utilizados para la funcionalidad de este proyecto
- `templates`: Almacena los archivos correspondientes a la construcción de la vista que se presenta al usuario, se almacenan los distintos <i>layouts</i> y <i>ventanas</i> utilizados en este proyecto
    - `dashboard`: Almacena los archivos de las vistas de la aplicación.
        - `categories.html`: Vista parcial del `catálogo de categorías` obtenido desde el controlador `categoriesController`. Se encarga de ejecutar la petición de las `recomendaciones por categoría`.
        - `dashboard.html`: Vista parcial de la ventana de bienvenida a la aplicación.
        - `rates.html`: Vista parcial del `catálogo de películas` obtenido dede el controlador `moviesController`. Se encarga de ejecutar la petición a las `recomendaciones por calificaciones`.
        - `recommendations.html`: Vista parcial que retorna el resultado de las `recomendaciones`. Esta vista es el resultado de la ejecución de alguna de las dos opciones con las que cuenta esta aplicación.
    - `layouts`: Almacena los archivos de plantillas mediante los cuales se despliegan los otros ficheros de visualización contenidos en el directorio `templates`.
        - `dashboard_layout.html`: Plantilla para desplegar las vistas parciales de la aplicación.
        - `login_layout.html`: Plantilla para desplegar las vistas parciales del inicio de sesión, registro de nuevos usuarios y la recuperación de la contraseña
    - `users`: Almacena los archivos de vista relacionados con los usuarios de este proyecto
        - `password_recovery.html`: Vista parcial para la reasignación de contraseña de un usaurio.
        - `profile.html`: Vista parcial para la edición de datos del usuario activo.
        - `register.html`: Vista parcial para el registro de nuevos usuarios.
    - `index.html`: Archivo de la vista de inicio de sesión
- `main.py`: Archivo principal para la ejecución de la aplicación.

## Notas
- El archivo CSV `movies_metadata.csv` fue modificado en la columna `release_date` desde Microsoft Excel para asignar el año a cuatro dígitos en lugar de dos dígitos para su posterior tratamiento.

## Despliegue
Una vez instaladas las dependencias es posible ejecutar este proyecto mediante el comando:

```terminal 
python main.py
```

## Autor
Epsom Enrique Segura Jaramillo

segurajaramilloepsom@gmail.com