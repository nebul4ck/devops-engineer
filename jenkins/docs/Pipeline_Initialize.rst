Pipeline Info
#############

Workflow
********


	**Commit (develop|master) => Github => Jenkins => Buanarepo (master|develop: main, restricted)**

Cada maintainer recibira información sobre el workflow en su canal privado de Slack. Los commits a la rama develop se publicarán en el canal #jenkins

Repository
**********

Master
======

Cuando se realiza un commit/merge a la rama **master**, el paquete será subido al repositorio **production**, tanto a la rama *main* como *restricted*:

.. code:: console

 $ cat /etc/apt/sources.list.d/master.buanarepo-main|restricted.nebul4ck.es.list
 deb https://master.buanarepo-main|restricted.nebul4ck.es:8080/ubuntu/master xenial main|restricted
..

Develop
=======

Los commits a la rama **develop** crearán paquetes tanto en código plano como encriptado en el repositorio **development**:

.. code:: console

 $ cat /etc/apt/sources.list.d/develop.buanarepo-main|restricted.nebul4ck.es.list
 deb https://develop.buanarepo-main|restricted.nebul4ck.es:8080/ubuntu/develop xenial main|restricted
..

Install package
***************

Una vez se ha compilado correctamente el nuevo paquete y los test han pasado sin errores, el paquete estará disponible en un repositorio u otro (develop o master)

Para instalar el paquete, clona la última version de `switch buanrepo <https://github.com/nebul4ck/switch-buanarepo>`_ y cambia a uno u otro repositorio (switch buanarepo gestiona los certificados, las URLs y la configuración del propio repositorio).

i.e: descargar el nuevo paquete desde el repositorio *development* y con el código encriptado:

.. code:: console

 - name: Add Buanarepo repository.
   include_tasks: buanarepo.yml
   vars:
     env_repo: 'development'
     type: 'restricted'
     add_repo: true
     remove_repo: true
   tags: buanarepo
..

i.e: descargar el nuevo paquete desde el repositorio de producción y con el código en plano:

.. code:: console

 - name: Add Buanarepo repository.
   include_tasks: buanarepo.yml
   vars:
     env_repo: 'production'
     type: 'main'
     add_repo: true
     remove_repo: true
   tags: buanarepo
..

Configurado el repositorio de nebul4ck:

.. code:: console

 $ sudo apt install <repo_name>
..

