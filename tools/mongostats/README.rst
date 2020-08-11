MONGOSTATS
##########

Entorno virtual para cliente mongo con el que se accede a un MongoDB standAlone o ReplicaSet para:

- Listar BBDD
- Tamaño del workingset + indexsize de cada base de datos
- Tamaño total utilizado por todas las bases de datos
- Listar colecciones dentro de cada base de datos
- Calcular el número de documentos existentes en cada colección


Lanzar el script:

.. code:: console

	$ . bin/activate
	$ python mongostats.py
..