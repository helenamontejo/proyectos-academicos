# Rutas y filtros (documentación de la entrega 2)

GESTIÓN DE USUARIOS (Segundo recurso RESTful)

GET /usuarios/
Acción CRUD: READ (Listar)
Descripción: Lista todos los usuarios. Renderiza usuarios/list.html

GET /usuarios/new
Acción CRUD: CREATE (Formulario)
Descripción: Formulario nuevo usuario

POST /usuarios/
Acción CRUD: CREATE
Descripción: Invocado por el formulario anterior para crear un usuario. Redirige a /usuarios

GET /usuarios/<id>
Acción CRUD: READ (Detalle)
Descripción: Muestra un usuario. Renderiza usuarios/show.html

GET /usuarios/<id>/edit
Acción CRUD: UPDATE (Formulario)
Descripción: Formulario editar usuario. Renderiza usuarios/edit.html

PUT /usuarios/<id>
Acción CRUD: UPDATE
Descripción: Invocado por el formulario anterior para editar un usuario. Redirige a /usuarios

DELETE /usuarios/<id>/
Acción CRUD: DELETE
Descripción: Invocado por el botón “Delete” presente en list.html. Elimina usuario

==================================================
FILTROS DE BÚSQUEDA IMPLEMENTADOS

Se han implementado filtros en la ruta:

GET /masajes/

Filtros disponibles:

Filtro por nombre
Permite buscar masajes cuyo nombre contenga el texto introducido (no distingue mayúsculas).

Filtro por rango de precio
Selector con opciones:

Menor de 100€

Entre 100€ y 120€

Mayor de 120€

Los filtros se envían mediante método GET y el servidor devuelve la lista ya filtrada renderizada con Jinja2.

==================================================
OBSERVACIONES TÉCNICAS

Para generar ids al crear masajes y usuarios, en vez de sumar 1 al tamaño del array, he buscado el mayor id y le he sumado 1, ya que usando únicamente el tamaño del array he tenido problemas como asignar el mismo id a dos objetos distintos.