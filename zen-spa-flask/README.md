# Zen Spa

Aplicación web en Flask para gestionar los masajes de un spa y sus usuarios, con una API REST documentada. Es el proyecto de la asignatura Tecnologías Web, hecho a lo largo de cinco entregas en marzo de 2026.

## Qué hace
- CRUD de masajes (nombre, duración, precio, si es individual y una imagen opcional) con validaciones de los datos.
- CRUD de usuarios.
- Registro, inicio y cierre de sesión. Las contraseñas se guardan con hash.
- Dos roles: cada usuario ve y gestiona sus propios masajes, y el administrador ve todos.
- Filtros de búsqueda de masajes por nombre y por rango de precio (ver `docs/rutas.md`).
- API REST en `/api/v1/masajes` (GET, POST, PUT y DELETE) con validación de datos mediante Pydantic y documentación Swagger en `/apidocs/`.
- Cada masaje consultado por la API se enriquece con datos de una API externa (`dummyjson.com`), de forma asíncrona y con caché de 10 minutos.
- Cliente de prueba de la API en `client/client.py`.

## Tecnologías
Flask, Jinja2, SQLAlchemy y Flask-Migrate (Alembic) con MySQL 8.0, Pydantic, Flasgger (Swagger/OpenAPI), `httpx` y `aiocache`. Las dependencias están en `requirements.txt`.

## Cómo ejecutarlo
1. Crea un entorno virtual e instala las dependencias:

       python -m venv venv
       source venv/bin/activate        # en Windows: venv\Scripts\activate
       pip install -r requirements.txt

2. Define la conexión a tu MySQL y una clave secreta (ver `.env.example`):

       export DATABASE_URL="mysql+mysqlconnector://USUARIO:CONTRASENA@localhost/zen_spa"
       export SECRET_KEY="una-clave-propia"

   La aplicación crea la base de datos `zen_spa` si no existe.
3. Desde esta carpeta, carga los datos de ejemplo (borra las tablas y las recrea) y arranca la app:

       python -m app.seed
       flask --app app run

   También se puede arrancar con `python -m app.app`. La web está en http://127.0.0.1:5000 y la documentación de la API en http://127.0.0.1:5000/apidocs/.

La migración de Alembic que crea las tablas está en `app/migrations/`. Como alternativa a `python -m app.seed`, se puede aplicar con `flask --app app db upgrade -d app/migrations`.

Los usuarios de ejemplo son solo para desarrollo: `admin` / `admin123`, `marta` / `marta123` y `pablo` / `pablo123`.

## Evolución del proyecto
1. **Entrega 1:** páginas estáticas en HTML y CSS (Flexbox, Grid, formularios y etiquetas semánticas).
2. **Entrega 2:** CRUD de masajes y usuarios con los datos en memoria, filtros de búsqueda y documentación de las rutas RESTful. Para generar ids busqué el mayor y le sumé 1, porque usar el tamaño de la lista daba ids repetidos.
3. **Entrega 3:** subida de imágenes, validaciones con mensajes de error, estilos CSS propios y fuentes.
4. **Entrega 4:** los datos pasan a una base de datos MySQL con migraciones, y se añaden registro, inicio de sesión, roles y contraseñas con hash.
5. **Entrega 5 (esta versión):** API REST con validación, documentación Swagger, consulta asíncrona a una API externa con caché, logging y cliente de prueba.

## Imágenes
Solo se incluye `logo.png`, que es propio. Las fotos de la web (portada, "sobre nosotros" y fondo de cabecera) no se incluyen. Para verlas, añade tus imágenes en `app/public/images/` con estos nombres: `spa-header1.jpg`, `spa1.jpg`, `spa2.jpg`, `spa3.jpg`, `masaje1.jpg`, `masaje2.jpg`, `masaje3.jpg` y `relajacion1.jpg`.

## Autoría
Helena Montejo.
