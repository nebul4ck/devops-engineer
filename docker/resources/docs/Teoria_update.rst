******
Docker
******

Index
=====

1. ¿Que es Docker?

     1)  Life Cycle
     2)  Docker

2. Partes y elementos de los que se compone Docker

     1)  Docker Engine
     2)  Docker images
     3)  Docker image index
     4)  Docker containers

          2.4.1)  Image vs container

     5)  Dockerfile
     6)  Docker host  

3. What happen when run a container

4. Comandos básicos de docker

     1)  Listar comandos
     2)  Buscando imágenes
     3)  Descargando nuevas imágenes
     4)  Listar imágenes descargadas (caché)
     5)  Correr un contenedor
     6)  Correr un contenedor con parámetros
     7)  Listar estado de contenedores
     8)  Iniciar y parar un contenedor
     9)  Conectar con contenedores a través de tty
     10) Comprobando los procesos internos y estádisticas de un container
     11) Eliminar contenedor, imágenes y volúmenes
     12) Prune: limpiar contenedores, imágenes, volúmenes y caché

5. Contenedores vs Virtual Machines

    1) What's happening inside the container
    2) No SSH Needed

6. Networking

    1) Docker Network
    2) Principales comandos de red
    3) Puertos
    4) DNS
       
        4.1) Round Robin test

7. Images vs Containers

    1) Layers: imáganes por capas
    2) Crear imágenes
    3) Taguear y subir imágenes
    4) Iniciar un contenedor a partir de una imagen
    5) Extender imágenes oficiales
    6) Comandos para imágenes

        6.1) Listar imágenes
        6.2) Descargar una imagen por su nombre y por su nombre y tag respectivamente
        6.3) Ver el historial de cambios para una imagen
        6.4) Ver detalles de una imagen
        6.5) Taguear una imagen
        6.6) Loguear en dockerhub (u otro si indicamos el enlace)
        6.7) Compilar una imagen
        6.8) Subir una imagen a docker hub (u otro si indicamos un repositorio diferente)
        6.9) Contruir una imagen

8. Persistencia de datos

    1) Data volumes
    2) Bind mounting

        2.1) Ejercicio

9. Componentes docker engine: How it is possible

    1) Namespaces
    2) Cgroups
    3) LXC

10. Algunas conclusiones

11. Best practices

    1) Performance

        1.1) Storage
        1.2) Imágenes y contenedores

    2) Logging
    3) Networking
    
        3.1) Seguridad por defecto

12. Tips

13. Docker Compose

  1) Docker-compose.yml: archivo de despliegue
  2) Principales comandos de docker-compose.

    2.1) Inicia todos los containers del compose.yml en segundo plano
    2.2) Visualiza los logs de los containers lanzados por compose
    2.3) Visualiza los containers en ejecución pertenecientes al compose.yml
    2.4) Visualiza los servicios que corren dentro de cada container
    2.5) Parada de servicios
    2.6) Lanza un compose que crea una imagen a partir de un dockerfile en runtime

15. Docker Swarm: service

  1) Inicia un cluster docker swarm
  2) Visualiza los nodos del cluster
  3) Crea un servicio con un solo nodo
  4) Visualiza los containers del cluster
  5) Mira información sobre un container/servicio concreto
  6) Añade nuevos nodos al cluster
  7) Actualiza un servicio a 3 nodos
  8) Elimina un nodo del cluster
  9) Crea un servicio con 3 nodos directamente
  10) Crear una red para el cluster de nodos
  11) Crear dos servicio en la red creada anteriormente
  12) Scale in and rollbacks
  13) Actualiza la imagen de un servicio en ejecución
  15) Añadir/Eliminar variables de entorno en caliente
  16) Publicar puerto en caliente

16. Docker Swarm en producción

    1) Docker Swarm Stacks
    2) Secrets en Swarm

        2.1) Crear un secret a partir de un archivo de texto
        2.2) Crear un secret a partir de la CLI
        2.3) Listar los secrets en la base de datos
        2.4) Comprobar el contenido de un secret
        2.5) Usar secrets en Swarm compose
        2.6) Añadir o eliminar un secret en caliente
        2.7) Usar secret en Swarm stack
        


1. Introducción: ¿Que es Docker?

1.1 Lifecycle

Version Life cycle

    - Edge = Beta : soporte durante 1 mes. Cada mes sale una beta.
    - Stable : soporte durante 4 meses.

    Como cada 3 meses sale una versión nueva, siempre habrá un mes para pasar de la versión actual a la nueva versión. (foto stable vs edge)


1.2 Docker

Docker es una herramienta que puede empaquetar una o mas aplicaciones y sus dependencias en un contenedor virtual, ejecutable en cualquier servidor Linux, ya sea instalación física, nube, etc...
Implementa una API de alto nivel para proporcionar contenedores que ejecutan uno o mas procesos de manera aislada dentro del OS Linux.
A diferencia de la virtualización convencional, Docker virtualiza a nivel de OS anfitrión, es decir, no necesita instalar un sistema operativo independiente (Guest) para cada "maquina virtual", evitando así la sobrecarga por iniciar y mantener máquinas virtuales, si no que crea contenedores independientes donde procesos (samba, http, ftp, apps...) son ejecutados de forma aislada (uno o mas por contenedor) a nivel del OS anfitrión. Por tanto, múltiples contenedores comparten el mismo nucleo y hardware, pero cada uno de ello puede tener ciertas limitaciones o restrinciones de acceso a recursos como CPU, RAM, Red, E/S... Para tal aislamiento docker utiliza características del kernel de linux tales como cgroups y espacios de nombres (namespaces).

Docker accede a las facilidades de virtualización del kernel de Linux directa o indirectamente. Desde la v.0.9 incluye la libreria libcontainer la cual proporciona acceso directo, mientras que con libvirt, LXC y Systemd-spawn lo puede hacer de forma indirecta. LXC era utilizado como entorno de ejecución por defecto hasta que se incluyo libcontainer en la v0.9 (escrita en Go).

Docker permite la automatización del despliegue de aplicaciones dentro de cada uno de los contenedores de software y que el despliegue de nodos se realice a medida que se dispone de recursos o cuando se necesiten mas nodos, lo que permite crear una plataforma como servicio (PaaS).

Docker se puede integrar con diferentes herramientras de infraestructura como AWS, Ansible, Chef, Cfengine, Google Cloud Plataform, OpenStack, Puppet, Salt y Vagrant.


2. Partes y elementos de los que se compone Docker

    2.1 Docker Engine

    Proporciona el core de docker en si, de manera que podamos hacer uso de imágenes y contenedores, administrados mediante su CLI. Docker engine está formado por:

        + Demonio: utilizado para administrar los contenedores (LXC) en el host anfitrión (Docker-Host).

        + CLI: linea de comandos para comunicarnos con el demonio de docker. Para que el shell de linux sepa que la orden ejecutada es interna de docker, necesitamos anteponer el comando "docker" a la orden (lo que puede ser para Linux un comando con parámetros)

            # comando subcomando [opciones]
            # docker run --help

        La sintaxis para el comando docker es la siguiente:

            # docker [opciones] [comandos] [argumentos]

    2.2 Docker images

    Una imagen es un sistema de archivos independiente y parámetros utilizados en tiempo de ejecución. Una imagen puede ser un snapshot de un contenedor o imágenes base (un OS) muy similares a los livecds. Una imagen no tiene estados ni modificaciones. Podemos buscar imágenes docker navegando por Docker Hub, por tanto y si no lo has hecho ya, deberás de crearte una cuenta. (https://hub.docker.com/). Si tenemos cuenta o la acabamos de crear, accederemos mediante "Log In". Desde la lupa buscaremos aquello que estemos buscando, por ejemplo una imagen de Ubuntu. Existe imágenes creadas por empresas o usuarios normales. La descarga de imágenes también se puede hacer mucho mejor desde CLI, algo que veremos mas adelante. La diferencia entre una imagen y un contenedor es una capa que se crea en el "top" del resto de capas de la imagen a la que se le denomina "Thin R/W layer" o "Container Layer" y es en la que se producen todas las escrituras y lecturas efímeras del container. Una vez el contenedor es eliminado, esta capa se elimina y el resto permanece intacta (capas de imagen).

    Nota: si acabamos de registrarnos, quizás estaría bien crear un repositorio personal. Esto lo haremos una vez hemos confirmado el registro a través del email, en la pestaña "Create Repository". Es bueno hacerlo público. En este tutorial llamaremos al nuevo repositorio mi_repo, aparecerá mas adelante, asi que nos acordaremos que es nuestro repo recien creado.


    2.3 Docker containers

    Es una instancia de una imagen. Los contenedores son creados al instanciar imágenes mediante Dockerfiles. En definitiva son directorio en el sistema de archivos local (donde tenemos instalado docker) que contiene todo lo relacionado con la aplicación/es. Estos directorios tienen un cierto formato reconocido por docker. Es posible empaquetar este directorio como otro cualquiera para poder migrar a otra máquina. La única dependencia es tener configurado el host al que se migra para que sea capaz de levantar contenedores docker.
    Cuando se instancia un container se le pasa un comando que será ejecutado dentro del container, cuando ese comando finalice el container se detendrá.

    2.4 Dockerfile

    Script para la automatización del proceso de creación de imagenes. Contienen una serie de comandos que al ser ejecutados generarán una nueva imagen docker. Los Dockerfiles comienzan con la definición de una imagen base utilizando el comando FROM. Existen otros comandos empleados en un Dockerfile, como por ejemplo:
            + ADD: añadir un archivo local a un contenedor
            + CMD: configura los comandos por defecto
            + COPY: Copia contenido del "current directory" directorio local o $(PWD) a un directorio dentro del container
            + ENTRYPOINT: define en el contenedor el punto de entrada de la aplicación
            + ENV: inicializa variables de entorno
            + EXPOSE: expone un puerto al exterior
            + FROM: configura la imagen base a usar
            + MAINTAINER: define el autor del archivo Dockerfile
            + RUN: ejecuta un comando y realiza un commit
            + USER: define el usuario que ejecutará contenedores para una imagen determinada
            + VOLUMEN: monta un directorio local en un contenedor
            + WORKDIR: establece el directorio de trabajo donde los comandos definidos por CMD serán ejecutados         


    2.6 Docker host

    Dentro de la terminología docker, debemos de saber que un docker host, es el host que contiene los container, es decir nuestra máquina local, llamada anfitrión en el resto de sistemas de virtualización.

3. What happens in the background when we run the docker

    - El commando 'container' espera que el último parámetro sea el nombre de la imagen desde la que desplegar el container. Lo primero que hace es buscar esta imagen en la cache local de esa imagen, si no existe, se irá a Docker Hub, el cual es el repositorio de imagenes por defecto.
    - Si no se elige una versión especifica, siempre intentará descargar la última.
    - No se hará una copia de la imagen cada vez que se levante un container, sino que iniciará una nueva capa con los cambios diferenciadores desde la última capa (imagen/snapshot) realizada la primera vez que se descargó y almacenó.
    - A continuación, asignará una IP virtual dentro de la red privada de Docker y abrirá los puertos especificados con la opción --publish (80:80, reenviará todo el tráfico del puerto 80 del docker host, al puerto 80 del container.
    - Se iniciará el container utilizando el CMD especificado en el Dockerfile


4. Introducción a comandos básicos docker

    4.1 Listar todos los comandos disponibles

        Si ejecutamos el comando docker sin mas, obtendremos una lista de todos los comandos docker disponibles:

        $ docker

        Quizás de entrada sea interesante ver que versión de docker se ha instalado y algo de información extra:

        $ docker version
        $ docker info

        A parte de los comandos build (construye una imagen), cp, diff, history, info, kill (mata un contenedor en ejecución), start, stop, restart, top (busca los procesos en ejecución de un contenedor) y versión, similares o idénticos a los propios de Linux, podemos utilizar:

            + attach: adjuntar un "objecto" a un contenedor en ejecución
            + commit: crea una nueva imagen con los cambios realizados en el contenedor
            + events: obtiene eventos en tiempo real desde el servidor
            + export: exporta el contenido de un contenedor a un archivo tar
            + import: crea una nueva imagen del sistema de archivos (carpeta contenedor) a partir de un archivo tar
            + images: listar las imágenes disponibles
            + insert: inserta un archivo en una imagen
            + inspect: muestra información de bajo nivel de un contenedor
            + load: cargar una imagen a partir de un archivo tar
            + login: iniciar sesión en el index de docker
            + logs: mostrar información (loggin) de un contenedor
            + port: hacer NAT del puerto público
            + ps: lista los contenedores activos
            + pull: descagar una imagen desde el index de docker
            + push: subir una imagen al index de docker
            + rm: elimina uno o mas contenedores
            + rmi: elimina una o mas imagenes
            + run: ejecutar un comando en un contenedor
            + save: guardar una imagen en un archivo tar
            + search: buscar imágenen en los repositorios (index) de docker
            + tag: etiqueta una imagen en un repositorio de docker

    4.2 Localizando una imagen en los repositorios de docker

        ## Para buscar por ejemplo imágenes docker de Ubuntu
        # docker search Ubuntu

    4.3 Descargando la imagen

        # docker pull ubuntu[:tag]

    4.4 Listar las imágenes disponible

        # docker image ls

        Nota: con este comando veremos entre otra información el ID de la imagen útil para arrancarla, pararla, eliminarla, etc...

    4.5 Iniciando un contenedor básico a partir de la imagen descargada

        # docker container run ubuntu[:tag]

        Nota: Si no hemos realizado previamente la descarga de la imagen, docker engine, comprobará si está en nuestro sistema local, si no lo está la descargará "on fly" y finalmente la instanciará en un container.

        Es posible que existan una gran variedad de versiones de Ubuntu en el repositorio, para concretar una podemos hacer uso de los tags:

        # docker run ubuntu:16.04

        Esto descargará e iniciará un container con la imagen de Ubuntu v16.04 LTS

    4.6 Instanciar un contenedor con parámetros

        # docker run --name <nombre_contenedor> [-d] [-it] [-p 8080:80] [-e PATH=:/usr/bin] <user_docker_hub>/<nombre_imagen> <comando_a_ejecutar>

        # docker run --name my_container -p 6000:5000 -link db:cassandra miuser/mi_imagen python apps/mipython1.py

        Con -name estamos nombrando a un container para poder identificarlo por su nombre en vez de por su ID, aunque es cierto que de no dar ningun nombre, docker asigna uno aleatorio.

        Por ejemplo podemos parar ahora el contaner con: docker stop my_container

        Con la opción -p hemos indicado que el puerto 6000 (expuesto en el container) se mapee al puerto 6000 de nuestro host local.
 
        Existe también el parámetro -P el cual indica que se mapeen los puertos necesarios (expuestos por defecto) del container a nuestro docker host (host local). Por ejemplo si una APP utiliza el 80, lo expondrá y lo mapeará a un puerto del rango 32768 to 61000 en nuestro localhost (puertos sin privilegios de root).

        La idea de poder mapear los puertos y no utilizar los puertos por defecto de una aplicación, por ejemplo 80:80 es evidente, no podríamos desplegar varias instancias de por ejemplo Apache en nuestro host local, es decir cada container levantaría un apache en el 80, pero solo uno podria ser mapeado en nuestro host local.

        Nota: al iniciar un container es posible pasarle un comando para que sea ejecutado dentro del container, en este caso el comando que se ejecutará dentro del container una vez iniciado es "python apps/mipython1.py"

        Importante: Un container se mantendrá activo mientras el comando que se ha ejecutado se encuentre activo, en este caso en cuanto el script mipython1.py realice su trabajo y finalice, el container se detendrá.


    4.7 Ver contenedores iniciados, iniciados y parados o los últimos contenedores creados (respectivamente).

        # docker container ls

        # docker container ls -a

        # docker container ll -ls

        nota: usa -s para ver el tamaño del container + imagen (total container size)

        Otra forma de ver el espacio total usado es con:

        $ docker system df

    4.8 Detener un contenedor

        # docker container stop <container_id>
        # docker container start [-at] <container_id> <command>

    4.9 Conectarse a la terminal de un container:

        4.9.1 Si el container es nuevo:
            $ docker container run --name webserver -it -p 8080:80 -d httpd bash|sh

        4.9.2 Si el container estaba parado y queremos iniciarlo accendiendo directamente a la terminal
            $ docker container start webserver -at webserver bash|sh

        4.9.3 Si el contenedor ya está en ejecución y lo único que queremos hacer es abrir un nuevo proceso de terminal para ejecutar algo desde dentro del container:
            $ docker container exec -it webserver bach|sh

        Nota: con imágenes como las de "ubuntu" no es necesario especificar el último argumento (en este caso el shell que queremos iniciar) debido a que el Dockerfile de la imagen ya tiene como CMD bash

    4.10 Comprobando los procesos internos y estádisticas de un container

        $ docker container top <container_name>
        $ docker container stats <container_name>
        $ docker container inspect <container_name>

    4.11 Eliminar un container, imagen o un volumen

        $ docker container rm <container_id>
        $ docker container run --name <name> --rm nginx  (será eliminado al ser parado, exit) 

        $ docker image rm <sha>
        $ docker volume rm <volume_name>

    4.12 Eliminando todos los contenedores, imágenes, volúmenes o cache

        $ docker container|image [-a]|volume|system prune

        Nota: la opción "-a" de image es para eliminar solo las que no se están utilizando.

    4.13 Find new images

        $ docker search --filter "is-official=true" --filter "is-automated=true" --filter stars=50 --no-trunc node

5. CONTAINERS vs VIRTUAL MACHINES

    Container aren't Mini-VM's

        - They are just processes
        - Limited to what resources they can access
        - Exist when process stops
    
    
Arrancar containers con variables de entorno: -e (--environment)

Para poner una password a Mysql se arranca el container con -e MYSQL_RANDOM_ROOT_PASSWORD=yes y luego se miran los logs del container durante el arranque 

5.1 What's happening inside the container 

    - Listar los procesos en ejecución dentro de un container : docker container top <container-name>
    - Detalles de la configuración de un container : docker container inspect <container-name>
    - Estadísiticas de rendimiento de todos los containers : docker container stats [-a,--all, --format string, --help, --no-stream]

5.2 No SSH Needed

    - Iniciar un contenedor con shell interactiva (el contenedor parará cuando salgamos de la shell): docker container run -it --name proxy nginx bash

        -i = interactive 
        -t = new pseudo tty

    Nota: cuando se inicia un container por defecto se le asigna un comando que hace que esté no se cierre, por lo general el comando que mantiene al servicio instalado dentro del container ejecutarse. Si añadimos nosotros un comando, este sustituirá al comando propio del container. Por ejemplo cuando descargamos una imagen de Ubuntu y ejecutamos el container, por defecto el comando a ejecutar es bash.  
  
    - Acceder a la shell de un container ya iniciado: docker container exec -it <nombre-container> bash 

    Nota: cuando hacemos exit de esta sesión interactiva, el container continuará corriendo ya que el comando exec lo que hace es abrir un nuevo proceso dentro del container.
   

6. NETWORKING

6.1 Docker Network

Docker incluye soporte para redes de containers. Por defecto docker proporciona dos drivers de red: bridge (puente de red) o overlay. El tipo de red bridge está limitado a un solo docker host, mientras que una red overlay puede incluir varios docker host y otros recuros.

Toda instalación de docker automáticamente incluye tres redes por defecto que podemos ver con el siguiente comando:

        # docker network ls
        NETWORK ID          NAME                DRIVER
        18a2866682b8        none                null                
        c288470c46f6        host                host                
        7b369448dccb        bridge              bridge

Por defecto docker lanza los container bajo la red bridge.

Notas:

    - Por defecto docker crea una red privada virtual (Docker0/Bridge) en el docker host, la cual realiza NAT contra la interfaz física del sistema para poder hacer un I/O de paquetes hacía o desde la red externa (a la que está conectada nuestro Docker Host)
    - También crea por defecto la red 'host' a cual se salta la funcionalidad de la red Bridge y utiliza la IP del docker host como gateway para salir al exterior. Es posible que se pierdan funcionalidades avanzadas de la containerización.
    - Utilizar esta segunda red (host), hará que el contenedor se enganche directamente a la interfaz física del docker host lo que mejorará el rendimiento (mayor throughput) al saltarnos la red virtual pero sacrificaremos la seguridad del container.
    - Existirá una tercera red llamada 'none' (--network none) a la que conectar container. Tiene la particularidad de que eliminará la interfaz 'fisica' del container, típicamente eht0, dejnado solo la interfaz localhost.
    - Cada container es conectado a una red virtual privada, creada en modo bridge
    - Cada red virtual privada se comunica entre ellas o hacia el exterior a través de NAT en el DockerHost
    - Todos los container iniciados dentro de la misma red privada virtual pueden comunicarse sin necesidad de exponer el puerto con -p
    - Buenas prácticas es crear una red virtual para cada conjunto de aplicaciones. Es decir si va a ver un container con php y otro con mysql, pueden estar dentro de la misma red, luego otra red para por ejemplo el Frontend.
    
Research: https://docs.docker.com/network/macvlan/#create-a-macvlan-network

6.2 Principales comandos:
    - Ver los puertos (ruteo) abiertos en un container:
        $ docker container port <containername>
    - Ver la IP asignada a un container: 
        $ docker container inspect --format '{{ .NetworkSettings.IPAddress }}' <containername>
    NOTA: el parámetro --format nos permite formatear el texto de salida y mediante expresiones JSON conseguir aquellos campos que nos interese o bien utilizar el comando grep.
    - Listar las redes disponibles: 
        $ docker network ls
    - Mostrar detalles de una red: 
        $ docker network inspect <network-name>|<network-id>|<container-id>
        Nota: Podemos ver tanto los detalles de una red entera, como los detalles de red de un container. ES posible que un container tenga ninguna, una o mas redes simultáneas, lo que equivaldría a tener varias interfaces de red.
    - Crear una red virtual nueva:
        $ docker network create <network-name> --driver <bridge por defecto>

        Esta red tendrá algunas características que no tiene la red por defecto docker, como por ejemplo la resolución DNS para todos los containers pertenecientes a esa red. Podemos hacer que containers se resuelvan mutuamente dentr de esta red, si utilizamos la opción --link al arrancar el container.
    - Añadir container a una red virtual:
        $ docker network connect <network-id> <container-name>
        Nota: una nueva NIC virtual será creada en el container
    - Iniciar un container en una determinada red:
        $ docker run -d --network lan1 --name micontainer1 nebul4ck/Ubuntu-apache2
    - Quitar container de una red virtual:
        $ docker network disconnect <network-id> <container-name>
    - Ver los containers que están dentro de una determinada red:
        $ docker network inspect <network-id> --format '{{ .Containers }}'

6.3 PORTS
    Cuando un container levanta una aplicación que requiere de un puerto, el docker container mapeará el puerto por defecto de la aplicación levantada con un puerto de rango superior de la máquina local. Lo anterior se consigue pasando el parámetro -P al comando run. También sabemos que si no queremos un mapeo por defecto, si no que queremos exponer un puerto determinado en el container y mapearlo con un puerto específico de la maqúina local, lo podíamos hacer con -p <puerto_container>:<puerto_máquina_local>.

    Si no sabemos a que puerto se ha mapeado un determinado puerto expuesto en un container, podemos utilizar el siguiente comando:

        $ docker port <container> <puerto_expuesto>

        $ docker port mi-container 5000
        49155

    Ahora por ejemplo vamos a ver que IP local es la que está expuesta para un container:
    
        $ docker-machine ip <container>

6.4 DNS
    - Olvida el utilizar IP's estáticas en los contenedores. Docker es demasiado dinámico como para depender de IP estáticas. 
    - Docker host, ya trae en su propio demonio un DNS server. Los nombres de los container son utilizados por el DNS como si de un hostname se trataran por lo que se utilizará los nombres de los container para la comunicación entre unos y otros.
    - Teniendo dos containers dentro de la misma red, podemos hacer: docker container exec -it container1 ping container2  , y veremos como resuelve el nombre correctamente. (en las nuevas imágenes nginx, el ping está desactivado por defecto, o bien entramos dentro e instalamos ping o utilizamos la imagen nginx:alpine
    - No obstante es posible crear alias para el hostname. Los alias nos permiten llamar de distintas formas a un mismo container. Es muy útil para realizar DNS round robin, por ejemplo poniendo el mismo nombre de alias a diferentes containers y luego haciendo peticiones curl a ese nombre, DNS daemon hará una especie de round robin entre los disitintos containers.

    Comandos para testear el DNS name:

    1. Crea la red
        $ docker network create my_app_net
    2. Crea dos containers dentro
        $ docker container run -d --name new_nginx --network my_app_net nginx
        $ docker container run -d --name new_apache --network my_app_net apache

    Nota: si no tienen el comando ping, entrar dentro con exec -it e instalar

    3. Hacer ping de uno a otro
        $ docker container exec -it my_nginx ping new_nginx

6.4.1 Round Robin test

    - Create a new virtual network (default bridge driver): docker network create dude
    - Create two containers from elasticsearch:2 image: docker container run -d --net dude --net-alias search elasticsearch:2 (x2)
    - Use --net-alias <nombre> when creating them to give them an additional DNS name to respond to: --net-alias search
    - Use alpine image to do an nslookup: docker container run --rm --net dude alpine nslookup search
    - Check DNS round robin: docker container run --rm --net dude centos curl -s search:9200

    Ejemplo:

    1. Crear red:
        $ docker network create dude
    2. Crear dos containers de elasticsearch y añadirlos en un alias:
        $ docker container run -d --net dude --net-alias search elasticsearch:2
        $ docker container run -d --net dude --net-alias search elasticsearch:2

    Nota: al no darles un nombre, lo cogerán por defecto
    3. Crear un contenedor efimero para hacer una busqueda al alias "search"
        $ docker container run --rm -- net dude alpine nslookup search
    4. Usar curl de forma efimera para ver que servidor nos responde
        $ docker container run --rm --net dude centos curl -s search:9200
        $ docker container run --rm --net dude centos curl -s search:9200
        $ docker container run --rm --net dude centos curl -s search:9200
    Nota: por cada comando veremos como cambia el nombre del contenedor que nos responde

7. IMAGES vs CONTAINERS

    7.1 Cada capa de la imagen tiene su propio SHA que ayuda al sistema a identificarla.

    Ejemplo de imagen con 3 capas:

    La primera capa de nuestra imagen será la capa "Ubuntu" lo que emula al OS y contendra los servicios a dockerizar (FROM)
    Acto seguido y mediante el Dockerfile (o el comando COMMIT) se añaden algunos otros archivos (por ejemplo con APT) o con COPY si pasamos archivos del host al docker, lo que escribirá otra capa por encima de esta.
    Otra capa por encima de esta última puede ser añadir variables de entorno a través del Dockerfile.

    Ejemplo de 2 imágenes que comparten capas

    Ambas imágenes van a compartir la capa de OS utilizada (FROM), en este caso un Debian Jessie. Esta capa se encuentra en la caché y como cada capa está identificada por un SHA único, el propio Docker host, sabrá que al usar el mismo OS/version se podrá utilizar la capa ya cacheada que contiene ese OS/version. Este 'match' entre lo que tenemos en la cache de Docker y lo que existe en la imagen que vamos a descargar de Docker hub, lo hace solo el Docker host.
    Por un lado una de las imagenes tiene 3 capas mas (mysql con RUN, algunos archivos copiados con COPY y un puerto abierto EXPOSE)
    Por otro lado, la otra imagen tiene la capa COPY y RUN idéntica a la de la primera imagen.
    La ventaja es que en nuestro sistema de archivos solo tendrémos una copia de cada capa. Por lo que las dos imágenes anteriores sumarán 4 capas (os+apt+copy+port).

    El tamaño de un contenedor podemos verlo con ps -s. El tamaño size es el tamaño de la capa Thin W/R Docker Layer (capa de escritura de un container) + el tamaño de las capas de lecturas (capas estáticas que forman la imagen). Si 4 container comparten imagen, el tamaño de capas estáticas se reduce en una cuarta parte y solo habría que sumar a este valor el valor de cada una de las capas de escritura de cada container. El valor de la capa estática + el de la de escritura es Virtual-Size.

    Un claro ejemplo es cuando queremos tener dos imágenes de Apache prácticamente idénticas a diferencia del virtual host/Website. Existe la capa OS (FROM), la capa apt apache (RUN), la capa port 80 (EXPOSE) y por encima cada imagen una pequeña capa que es la carga del website conf (Thin W/R Container Layer).

    ¿Como funciona a nivel de container?

     Docker para cada container que levantemos a partir de cualquiera de las dos imagenes creadas anteriormente, creará una nueva capa de lectura/escritura encima de esta imagen. 
    
     Cuando examinamos los archivos del sistema una vez el container iniciado, veremos que en principio se trata de un archivo regular en el sistema de archivos pero por debajo de esto el driver de almacenamiento que ha sido utilizado por Docker (overlay2) ha creado una especie de archivo de cambios (con las distintas modificaciones que se han realizado desde el container y que no pertenecen a la imagen). Este archivo es de lectura y escritura, sin embargo el archivo de la imagen es read-only. Por lo tanto cuando arrancamos container a partir de una imagen se crea un archivo Cow en el que se copian los cambios/diferencias que existen entre el container en ejecución y la imagen estática. Por lo que al final el container es un proceso del sistema que utiliza este archivo como una especie de imagen/archivo cow de intercambio para minimizar el I/O.

    TIP: Un container no es mas que una capa de lectura/escritura en el top de la imagen.

    7.2 About images tags and how to upload them to Docker hub

    Las imágenes no tienen un nombre específico: $ docker image ls , por lo que algo común es asociar un tag o etiqueta a un image_id. Existen otras formas de referirnos a una imagen (con el comando anterior solo vemos 2, el tag y el image id. Otra forma es mediante el USER/REPO:TAG (tag = version, 1.0 ej.). Esto no es válido para las imagenes oficiales, ya que están en el "root namespace" de registry y no necesitan un nombre de usuario y cuando hacemos pull de estas images, en la columna repository, solo aparece el nombre de la imagen pero no el usuario. Si por el contrario descargamos una imagen no oficial y volvemos a repetir el comando, veremos que ahora si se añade el nombre de usuario o nombre de organización al repositorio, por lo cual se identifica inequivocamente.
  
    Tags needs to actually be in a specific format in order to work with a registry, para mas info: $ docker image tag --help
    

    ¿Cuando crear un tag?

        - cuando tenemos diferentes versiones de una image
        - cuando dentro de una misma versión queremos referirnos a la misma versión de imagen con diferente tag: 1.0.0 , 1.0, 1 y latest ; cuatro tags que apuntan a una misma image
    
    Nota: si no damos un tag a la image destino, por defecto será latest

    Para descargar una imagen según su tag: $ docker pull nginx:latest

    Si intentamos descargar una imagen con dos tags diferentes pero que apuntan a la misma imagen, Docker no volverá a descargarla debido a que ya se encuentra en cache, y nos avisará de ello. Diferente es que podamos crear un nuevo tag a una imagen previamente descargada, sin importar si es propia, oficial o de terceros. Esta imagen a la que hemos añadido por ejemplo el nombre de nuestro repo:

    $ docker image tag mysql nebul4ck/mysql:mainimage

    Recordar que si no añadimos tag se creará por defecto latest. No obstante podemos modificarlo a posteriori con:

    $ docker image tag nebul4ck/mysql:mainimage nebul4ck/mysql:1.0.0

    Todos estos tags compartirán el mismo image_id

    TIP: El tag "latest" se utiliza para marcar una imagen como estable.

   No existirá aun en nuestro repositorio pero podemos subirla de la siguiente forma:

    $ docker login
        username: nebul4ck
        password: ********

    Por defecto nos autenticará contra Docker Hub pero cabe la posibilidad de pasar una URL personalizada. La configuración y metadatos se almacenan bajo ~/.docker/

    $ docker image push nebul4ck/mysql

    Tras realzar los cambios, es buena practica realizar un logout si la máquina es compartida

    Al igual que no podíamos descargar una imagen mas de una vez mediante diferentes tags, tampoco se podrá subir a Docker Hub mas de una vez la misma imagen con diferente tag, a menos que modifiquemos ciertas capas (layers) de la imagen, lo que vendría a ser ya otra imagen diferente. No obstante, aunque la imagen sea la misma y no permita hacer el push, si que se creará la nueva etiqueta para esta image en Docker Hub.

7.3 Create images with Docker files.

    Dockerfile es una receta para crear una imagen personalizada. Aunque tenga un aspecto parecido a batch o shell script, no es ninguno de ellos ya que tiene un formato propio y exclusivo de Docker.

Un ejemplo de Docker file:

<ejemplo>

# NOTE: this example is taken from the default Dockerfile for the official nginx Docker Hub Repo
# https://hub.docker.com/_/nginx/
# NOTE: This file is slightly different then the video, because nginx versions have been updated 
#       to match the latest standards from docker hub... but it's doing the same thing as the video
#       describes
FROM debian:stretch-slim
# all images must have a FROM
# usually from a minimal Linux distribution like debain or (even better) alpine
# if you truly want to start with an empty container, use FROM scratch

ENV NGINX_VERSION 1.13.6-1~stretch
ENV NJS_VERSION   1.13.6.0.1.14-1~stretch
# optional environment variable that's used in later lines and set as envvar when container is running

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y gnupg1 \
    && \
    NGINX_GPGKEY=573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62; \
    found=''; \
    for server in \
        ha.pool.sks-keyservers.net \
        hkp://keyserver.ubuntu.com:80 \
        hkp://p80.pool.sks-keyservers.net:80 \
        pgp.mit.edu \
    ; do \
        echo "Fetching GPG key $NGINX_GPGKEY from $server"; \
        apt-key adv --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$NGINX_GPGKEY" && found=yes && break; \
    done; \
    test -z "$found" && echo >&2 "error: failed to fetch GPG key $NGINX_GPGKEY" && exit 1; \
    apt-get remove --purge -y gnupg1 && apt-get -y --purge autoremove && rm -rf /var/lib/apt/lists/* \
    && echo "deb http://nginx.org/packages/mainline/debian/ stretch nginx" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
                        nginx=${NGINX_VERSION} \
                        nginx-module-xslt=${NGINX_VERSION} \
                        nginx-module-geoip=${NGINX_VERSION} \
                        nginx-module-image-filter=${NGINX_VERSION} \
                        nginx-module-njs=${NJS_VERSION} \
                        gettext-base \
    && rm -rf /var/lib/apt/lists/*
# optional commands to run at shell inside container at build time
# this one adds package repo for nginx from nginx.org and installs it

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
# forward request and error logs to docker log collector

EXPOSE 80 443
# expose these ports on the docker virtual network
# you still need to use -p or -P to open/forward these ports on host

CMD ["nginx", "-g", "daemon off;"]
# required: run this command when container is launched
# only one CMD allowed, so if there are mulitple, last one wins


<fin ejemplo>

FROM : Existe en todos los Dockerfiles (es un requisito). La mayoría de las veces veremos que se utiliza Alpine por estar bastante optimizada (minimal distribution) para Docker. Sin embargo para entornos mas estables se utilizan distribuciones con administradores de paquetes mas comunes como APT o YUM (Ubuntu, Debian, Fedora o CentOS). Estas distribuciones cuentan con los últimos parches de seguridad por lo que crea entornos mas seguro. También es posible utilizar una imagen, por lo que la nueva imagen dependerá de aquella que carguemos con FROM (lo veremos en la próxima sección)

ENV : Estas instancias permiten crear variables de entorno, en nuestro ejemplo contamos con dos. Es muy importante contrar con ellas ya que permiten setear dentro del container o durante su creación clave:valor para que el container obtenga está información.

Importante: cada una de estas instancias/líneas forman una capa (layer) de nuestra imagen, por lo que el orden en el que se establezcan es realmente importante.

RUN : Esta instancia nos permite ejecutar comandos shell o scripts que hayamos creado y copiado dentro del container antes de llegar a esta instancia dentro del container durante su creación. Se utiliza "&&" dentro del comand RUN cuando queremos ejecutar varios comandos y que pertenezcan todos a la misma capa de la imagen. La sgunda instancia RUN es muy importante, ya que permite enlazar la salida estandar del container con el docker host, de manera que podamos leer los logs del container. AUNQUE LUEGO VEREMOS LA FORMA CORRECTA DE HACER ESTO (existen Drivers propios de docker engine que hará esto por nosotros)

EXPOSE : nos permite exponer puertos tcp/udp, que no se exponen por defecto. Esto no garantiza que cuando iniciemos el container, se abran los puertos automáticamente, si no que tendremos que usar el parámetro -p para iniciar el container.

CMD : Esta instancia es igual de obligatoria que FROM y debe de ir al final del Dockerfile. Este comando será lanzado siempre que se cree un nuevo container a partir de esta imagen, se inicie o se detenga el container ya creado. 

mas instancias de Dockerfile:

    + ADD: añadir un archivo local a un contenedor
    + COPY: Copia contenido del "current directory" directorio local o $(PWD) a un directorio dentro del container
    + ENTRYPOINT: define en el contenedor el punto de entrada de la aplicación
    + MAINTAINER: define el autor del archivo Dockerfile
    + USER: define el usuario que ejecutará contenedores para una imagen determinada
    + VOLUMEN: monta un directorio local en un contenedor
    + WORKDIR: establece el directorio de trabajo donde los comandos definidos por CMD serán ejecutados

7.4 Running Docker builds: Building images.

    Lo primero, al ejecutar el Dockerfile, docker hará un pull de la imagen/distro que hayamos elegido en la instancia FROM y la almacenará en cache local, a continuación ejecutará dentro de docker engine línea a línea las siguientes instancias del archivo Dockerfile en su correspondiente cache layer. 

    A continuación construiremos una imagen a partir del Dockerfile (miDockerfileApp). Podemos usar Docher Hub o bien trabajar en local:

    En local:

        $ docker image build -t nebul4ck/newApp:1.0 -f miDockerfileApp .

        Donde:
            nebul4ck/newApp:1.0 es el nombre completo de la imagen (usuario/app:version). Es necesario indicar el último "." para hacer referencia al directorio de trabajo donde tenemos el Dockerfile.

        Durante la ejecución, existirá un hash que se corresponderá con la instancia ejecutada. Está quedará en cache, si no existen cambios en las construcciones posteriores, estas líneas (las que no hayan sufrido cambios) no serán ejecutadas porque ya están almacenadas (sus resultados) en su correspondiente cache layer. Esto acelera la construcción y despliegue.

    IMPORTANTE: el orden de las instancias es MUY importante debido a que en el momento que se encuentre una línea distinta a la cacheada (los hash no coinciden) todas aquellas instancias que sean posteriores a la que ha cambiado, tendrán que ser ejecutadas nuevamente aunque no haya cambiado. Se recomienda entonces que aquellas instancias mas propensas a cambios se ejecuten en último lugar, por ejemplo si estamos ejecutando un programa cuyo código fuente hemos modificado. Por lo tanto, lo mejor es que las primeras líneas construyan una buena base, que prácticamente nunca cambie y sea estable, sobre la que ejecutar nuevas instancias, esto nos llevará menos tiempo.


7.5 Extendiendo imágenes oficiales

Lo que haremos a continuación será extender una imagen oficial, es decir crear una imagen personalizada basada en una imagen ya existente, en este caso de un nginx oficial. Luego le añadiremos un tag y la subiremos a Docker Hub. Por último las conclusiones.

    $ docker image pull nginx:latest

    Ahora ya tenemos la imagen oficial y cada una de sus capas cacheadas en local.

    $ mkdir ~/docker/nginx-proof    
    $ cd ~/docker/nginx-proof
    $ vi index.html
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">

      <title>Proof Hello World!</title>

    </head>

    <body>
      <h1>Hello World!</h1>
    </body>
    </html>

    $ vi Dockerfile
    # Extenderemos la imagen oficial nginx. En otras palabras, la usaremos de base.

    FROM nginx:latest
    # Es recomendable usar el tag/versión para asegurarnos de que la base es estable

    WORKDIR /usr/share/nginx/html
    # La instancia WORKDIR seteará como directorio raíz de nginx al indicado. Es similar a "RUN cd /usr/share/nginx/html", solo que es preferible utilizar WORKDIR. Se puede utilizar en diferentes líneas, cada vez que queramos cambiar de directorio para acometer una acción.

    COPY index.html index.html
    # La instancia COPY copiará el archivo index.html que hemos creado previamente (si no estamos en la ruta, deberemos de indicar el path completo al archivo a copiar) en el directorio WORKDIR indicado.

    # IMPORTANTE: No hemos utilizado la instancia CMD ya que está dentro de la imagen de la que heredamos (nginx:latest en este caso).


    Nota: Esta práctica se utiliza mucho para contruir imágenes heredando de otras imágenes. Las variables de entornos (aquellas marcadas por la instancia ENV, no será heredadas).


    $ docker image build -t nebul4ck/hello-world-nginx:0.1.0 -f Dockerfile .

    Podemos probar que todo va OK:

    $ docker container run -p 80:80 --rm nebul4ck/hello-world-nginx:0.1.0 -d

    Nota: recordar que con --rm eliminaremos todo al parar el container. Esto es útil cuando se realizan pruebas o queremos volatilidad del container.

    Si todo hay ido bien, podremos subir nuestra nueva imagen a Docker Hub. Para ello deberemos antes renombrar y opcionalmente ponerle un tag, de lo contrario se utilizara "latest"

    $ docker image tag nebul4ck/hello-world-nginx:0.1.0 nebul4ck/hello-world-nginx:stable
    $ docker image push nebul4ck/hello-world-nginx:stable

    Conclusiones:

    Una buena práctica es tener una imagen o varias imagenes que conforman una muy estable y con la mayoría de software y configuraciones que utilizarán otros docker, para posteriormente crear aquella imagen específica que usaremos para levantar container. Por ejemplo podemos tener una primera imagen con un ubuntu actualizado, python2.7 y la última JDK. Esta imagen servirá de base para otras imagenes, por ejemplo de webservers que heredarán de esta para construirse. Luego en función de las ultimas configuraciones (páginas web, puertos de escucha, etc..) podremos crear otra imagen que compacte la de ubuntu y el webserver, para definitivamente añadir algunas capas como las páginas web y los puertos. Finalmente levantaremos varios container con diferentes páginas webs y puertos de escucha sin a penas esfuerzos y muy rápido.

7.6 Comandos para imágenes

7.6.1 Listar imágenes

    $ docker image ls

7.6.2 Descargar una imagen por su nombre y por su nombre y tag respectivamente

    $ docker pull nginx

    $ docker pull nginx:1.11.9

7.6.3 Ver el historial de cambios para una imagen

    $ docker history nginx:latest

7.6.4 Ver detalles de una imagen

    $ docker image inspect nginx

7.6.5 Taguear una imagen

    $ docker image tag nginx bretfisher/nginx
    $ docker image tag nginx-with-html:latest bretfisher/nginx-with-html:latest

7.6.6 Loguear en dockerhub (u otro si indicamos el enlace)

    $ docker login
    $ cat .docker/config.json

7.6.7 Compilar una imagen
    $ docker image build -t nebul4ck/hello-world-nginx:0.1.0 -f Dockerfile .

7.6.8 Subir una imagen a docker hub (u otro si indicamos un repositorio diferente)

    $ docker image push bretfisher/nginx
    $ docker image push bretfisher/nginx bretfisher/nginx:testing

7.6.9 Contruir una imagen

    $ cd dockerfile-sample-1
    $ vim Dockerfilel
    $ docker image build -t customnginx .

8. Persisten data

    8.1 Data volumes

        Los data volumes se pueden crear directamente desde el Dockerfile mediante la instancia VOLUME. Por ejemplo en un Dockerfile de Mysql podemos encontrar la línea "VOLUME /var/lib/mysql" lo que creará un almacen persistente que durará hasta que manualmente sea eliminado. No se podrá eliminar tan solo eliminando el container. Este directorio será mapeado a un directorio concreto del Docker Host "/var/lib/docker/volumes/31293812738r3r3rh23012/_data" (por ejemplo).

          Podemos conocer la localización de los datos en el Docker host tal que así:

              $ docker container ls
              $ docker container inspect <name>
            {
                   "Mounts"...
                      "Source" : "/var/lib/docker/...."
              }

             $ docker volume ls
             $ docker volume inspect <volume name>

            Es posible crear un volumen al container en tiempo de ejeción al cual además le pasamos un nombre concreto:

               $ docker container run -d --name mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=True -v mysql-data:/var/lib/mysql mysql

            Donde "mysql-data" es el nombre que tomará el volumen (será creado y almacenará los archivos que el contenedor almacene en /var/lib/mysql, en el directorio /var/lib/docker/overlay2/... del docker host.)

            La nueva forma de hacer esto es sustituyento -v|--volume por --mount:

                $ docker container run -d --name mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=True \
                --mount type=volume,source=mysql-data,target=/var/lib/mysql mysql

           Nota: es posible reutilizar este volume en otro container, dejándo la línea exactamente igual pero cambiando el --name <nombre>

            Tambien es posible crear primero el volumen y luego asignarselo a un docker durante la ejecución del container (docker run...) de esta manera podemos utiliar drivers y labels personalizadas:

                $ docker volume create --help

            Nota: esta manera se utiliza en entornos de producción donde se requiere una configuración mas personalizada.

    Los volumemens nos facilitan mucho la vida a la hora de actualizar la version de una aplicación por ejemplo con bbdd. Si tenemos una version de posgresql y un volumen para los datos y queremos actualizar la version de postgresql, solo tendremos que crear un nuevo Dockerfile con la nueva postgresql y utilizando el mismo directorio para la instancia VOLUME para el container que está ejecutando la antigua versión, e iniciar el nuevo. Las bbdd, tablas, usuarios etc.. se mantendrán gracias al volumen.

    8.2 Bind Mounting

        Archivos o directorios del docker host mapeados en el container para poder hacer uso de ellos desde dentro del container. En este caso no se pueden mapear desde el Dockerfile, el mapeo se hace una vez el container a iniciado:

            $ docker container run -d --name nginx -p 80:80 -v $(pwd):/usr/share/nginx/html nginx

       Ahora todo lo que agregremos en $(pwd) estará en tiempo real en el directorio /usr/share/nginx/html del container. Si eliminamos archivos desde el container, estos permanecerán en el docker host. En realidad con este método no tenemos que entrar al container, por lo que para labores de desarrollo es muy práctico, ya que modificaríamos código en el docker hosts y sería interpretado en tiempo real por el container. La diferencia con el VOLUME  es que en este caso no creamos un almacen persistente en el container, si no que es un simple mapeo.

    8.2.1 Ejercicio con bind mounting

        La idea es ver en tiempo real como cambia el contenido web editando archivos que se encuentran en un directorio del docker hosts, el cual se encuentra mapeando con bind mounting en el container lanzado. Este uso de docker hace el desarrollo web (en este caso) mucho mas eficiente, ya que no es encesario disponer de un host en el que tengamos que descargar determinadas herramientas de desarrollo, desplegar y configurar un servidor web en un determinado OS, etc... bastará con levantar un container y desde nuestro PC (docker host) trabajar sobre el código y ver modificaciones en tiempo real.

        Nos encontramos en un directorio de trabajo en el que tenemos una serie de archivos de configuración y una carpeta con archivos web (_posts), en este caso tan solo un archivo .md (Markdown) que se mostrará como archivo principal de la web. El servidor web a utilizar será jekyll, un generador de de sitios estáticos (SSG por sus siglas en inglés, Static Site Generator) utilizado especialmente en las "GitHub pages" (https://pages.github.com/)

        **Puedo reutilizar el contenido del repo udemy-docker-mastery/bindmount-sample-1

        cd udemy-docker-mastery/bindmount-sample-1
        login: docker login
        username:
        password:
        Iniciar el container con: docker container run --name myjekyll -p 80:4000 -v $(pwd):/site bretfisher/jekyll-serve

        Una vez iniciado el container, abrir el navegador y ver la página principal que tenemos en jekyll.
        Luego, modificar el archivo que hay dentro de _posts y veremos como cambia en tiempo real en el navegador.

Ref
---

* https://docs.docker.com/storage/volumes/
* https://docs.docker.com/engine/reference/commandline/volume_create/


9. How Docker is possible

9.1 NAMESPACE
Según las páginas man de linux un namespace es una capa de abstracción que hace que parezca que los procesos dentro de un determinado namespace tengan sus propios recursos hardware aislados. Los cambios en los recursos globales son visibles para procesos miembros del mismo namespace, pero no para procesos en distinto namespaces. El uso principal de de los espacios de nombres es la implementación de contenedores.

Cuando se necesita aislar un recurso hardware a un grupo de proceso (container), este dependerá del tipo de namespace. Todos los procesos son asociados con un namespace y solo podrán utilizar los recursos asociados a ese namespace.

Desde la versión 3.8 del kernel de linux existen 6 tipos de namespaces:

    - mnt: controla el aislamiento de los distintos puntos de montaje.
    - pid: encargado de asignar un nuevo PID a cada proceso.
    - net: proporciona el aislamiento de los recursos asociados con el networking (devices, IPv4, IPv6, IP routing table, etc...)
    - ipc: identificadores IPC de SysV
    - uts: nombres de hosts y dominios
    - user: identificadores de usuarios y grupos.

Podemos ver estos grupos bajo el directorio /proc/[PID]/ns/

En definitiva los namespace se utilizan para agrupar procesos incluyendo árboles de procesos, red, ID de usuario y sistemas de archivos montados, para posteriormente aislarlos a nivel de recursos, del resto de procesos pertenecientes a otros namespaces.

Docker crea una serie de namespaces para cada uno de los containers que inicia.

9.2. GRUPOS DE CONTROL (CGROUPS)

Debido a que los permisos tradicionales linux, ACLs, MAC (SELinux), los limites (/etc/security/limits.conf) que acotan la máxima asignación de recursos y el planificador de recursos (nice, renice o ionice) son insuficientes si lo que desea un administrador de sistemas es especificar con detalle como se deben asignar los recursos entre las diferentes tareas en ejecución, se integró en el kernel de Linux la herramienta cgroups.

El fin de utilizar cgroups, es poseer a nivel de sistema la capacidad de aislar el consumo de recursos (CPU, memoria, E/S, ancho de banda, etc...) de forma independiente a cada grupo de procesos. Por tanto cgroups es una herramieta util para controlar la asignación de los recursos a los procesos, la cual se integro en el núcleo de Linux a partir de la versión 2.6.29.

Nota: existe la versión cgroups-v2 integrada en Marzo del 2016 en el kernel 4.5

Los grupos de control (cgroups) permiten definir una jerarquía de grupos de procesos de manera que un administrador pueda definir al detalle la asignación de sus recursos (tiempo de CPU, I/O, RAM, Ancho de banda...).

Una forma sencilla de ver la potencia de cgroups es con el siguiente ejemplo:
    "Supongamos que tenemos una CPU y dos procesos en ejecución, y que con el comando nice le hemos dado la misma prioridad de tiempo de CPU a cada uno de ellos. El problema surge cuando uno de los dos procesos es por ejemplo un software como Apache HTTP, el cual crea procesos hijos 
    haciendo uso de fork. Estos subprocesos heredan la prioridad del proceso padre (la cual es la misma que para el otro proceso), de modo que si apache a creado 98 subprocesos (+ el proceso padre) al otro proceso no Apache, le queda tan solo un 1% de uso de CPU, haciendose Apache con el 99% de tiempo de CPU.
    Con los grupos de control se podría entonces crear dos grupos independientes, uno para apache y otro para la otra aplicación, y asignar por ejemplo un 50% de tiempo de CPU para cada uno de ellos. La suma de todos los subprocesos apache no consumirá nunca mas del 50% de tiempo de     CPU."

Nota: en las distribuciones que están implementando systemd como controlador de procesos, cgroups se integra directamente con este. En las que no, cabe la posibilidad de manipular cgroups a partir del sistema de archivos virtual /sys. Concretamente los cgroups mantienen su punto de montaje bajo /sys/fs/cgroup

Nota2: no es muy extraño que navegadores como chrome o firefox consuman recursos del sistema en exceso, concretamente memoria ram. Es posible con cgroup aislar en un grupo a los navegadores, de manera que nunca nuestra estación de trabajo se llegue a congelar como consecuencia de un "mal funcionamiento" del navegador.

Podemos aprender mas sobre los cgroups:

    - http://elpuig.xeill.net/Members/vcarceler/articulos/introduccion-a-los-grupos-de-control-cgroups-de-linux
    - https://www.digitalocean.com/community/tutorials/how-to-limit-resources-using-cgroups-on-centos-6

9.3 LXC

LinuX Containers es una tecnologia de virtualización a nivel de OS para Linux, similar a OpenVZ o Linux-VServer. LXC permite que un servidor físico ejecute múltiples instancias de OS aislados conocidos como Servidores Privados Virtuales o VPS. A diferencia de una máquina virtual convencional, LXC provee de un espacio de usuario (container) que posee su propio espacio de procesos y redes.

Al igual que Docker, LXC utiliza cgroups y namespaces para contabilizar, limitar y aislar los recursos, y una API de alto nivel para la administración de los contenedores.

Es posible utilizar una distribución de Linux diferente en cada contenedor, siempre y cuando hagan uso de la misma versión de kernel que posee la máquina física (en concreto el OS anfitrión).

Un contenedor LXC contiene los mismos servicios que una máquina con un OS Linux (cron, logs, comandos..), de hecho es posible entrar a la consola del contenedor e instalar el paquete deseado mediante el gestor de paquetes correspondiente.

A nivel de red es posible conectar el contenedor con el host anfitrión y con el resto de contenedores, creando una "LAN" a nivel de host.

Cada contenedor LXC tiene su propio sistema de ficheros (en definitiva un directorio de la máquina anfitriona). Esto ofrece la ventaja que con un rsync podemos copiar un contenedor a otra máquina.

LXC tiene grandes similitudes con chroot solo que con muchas mas funcionalidades.

Algunos enlaces de interes:

    - https://www.stgraber.org/2013/12/20/lxc-1-0-blog-post-series/  -> desarrollador de LXC
    - https://help.ubuntu.com/lts/serverguide/lxc.html  -> LXC sobre Ubuntu
    - https://rootsudo.wordpress.com/2014/09/20/lxc-linux-containers-linux-dentro-de-linux/

10. CONCLUSIONES

Ya sea utilizando Docker o LXC, la administración de un contenedor (iniciarlo, detenerlo, destruirlo, etc...) es mucho mas eficaz e impacta menos en el rendimiento de la máquina anfitriona que una virtualización convencional donde se despliega y administra una máquina completa.


12 Best practices
#################

12.1 Performance
****************

12.1.1 Storage
==============

* Use overlay2 storage driver by default as much as possible (by default in newer linux version).
* Storage drivers allow you to create data in the writable layer of your container.
* If you need multiple images to have shared access to the exact same data, store this data in a Docker volume and mount it into your containers.
* Volumes are the preferred mechanism for persisting data generated by and used by Docker containers (volumes are completely managed by Docker) => No use "bind mounts" (dependent on the directory structure of the host machine).
* volumes are often a better choice than persisting data in a container’s writable layer, because a volume does not increase the size of the containers using it, and the volume’s contents exist outside the lifecycle of a given container.
* If your container generates non-persistent state data, consider using a tmpfs mount to avoid storing the data anywhere permanently, and to increase the container’s performance by avoiding writing into the container’s writable layer.
* Bind mounts are very performant, but they rely on the host machine’s filesystem having a specific directory structure available. If you are developing new Docker applications, consider using named volumes instead.
* Use -v, --volume or --mount in order to bind or mount volumes storages. The biggest difference is that the -v syntax combines all the options together in one field, while the --mount syntax separates them. New users should use the --mount syntax. Experienced users may be more familiar with the -v or --volume syntax, but are encouraged to use --mount, because research has shown it to be easier to use.
  * If you use -v or --volume to bind-mount a file or directory that does not yet exist on the Docker host, -v creates the endpoint for you. It is always created as a directory.
  * If you use --mount to bind-mount a file or directory that does not yet exist on the Docker host, Docker does not automatically create it for you, but generates an error.
  * When using volumes with services, only --mount is supported.
* As opposed to volumes and bind mounts, a tmpfs mount is temporary, and only persisted in the host memory. When the container stops, the tmpfs mount is removed, and files written there won’t be persisted.
    * You can’t share tmpfs mounts between containers.
    * This functionality is only available if you’re running Docker on Linux.
    * Choose the --tmpfs or --mount flag

Ref
---
* https://docs.docker.com/storage/volumes/
* https://docs.docker.com/storage/bind-mounts/
* https://docs.docker.com/storage/tmpfs/

12.1.2 Images and containers
=====================
* Create a common image (os, config, directories, volumes) for shared services and then re-create new images based on the first one. From this way, the second images contains all the layers from the first image (sharing data on disk)
* For write-heavy applications, you should not store the data in the container. Instead, use Docker volumes, which are independent of the running container and are designed to be efficient for I/O. In addition, volumes can be shared among containers and do not increase the size of your container’s writable layer.

Ref
---
* https://docs.docker.com/storage/storagedriver/

12.2 Logging
============
* Configure logging driver and log rotation.
* Use environment variables or labels with logging drivers. "$ docker run -dit --label production_status=testing -e os=ubuntu alpine sh" => The following output is generated by the json-file logging driver: "attrs":{"production_status":"testing","os":"ubuntu"}.
* Usa el comando docker logs para visualizar los logs cuando configures el log driver a "local", "json-file" o "journald".
* Una buena opción si queremos almacenar los logs en el sistema, como el resto de servicios, es usar journald o syslog y añadir etiquetas o variables de entorno "--label or -e".
* Reading log information requires decompressing rotated log files, which causes a temporary increase in disk usage (until the log entries from the rotated files are read) and an increased CPU usage while decompressing.
* The capacity of the host storage where the Docker data directory resides determines the maximum size of the log file information.

Ref
---

* https://docs.docker.com/config/containers/logging/json-file/
* https://docs.docker.com/config/containers/logging/syslog/
* https://docs.docker.com/config/containers/logging/journald/

12.3 Networking
===============

12.3.1 Default security

* Create as applications as you can at the same network so their inter-communication never leaves host, for example: lamp_network contains mysql, php and apache. We only need open 8080 port in our host while the mysql and apache connections will be possible one each other.



13. Tips
========
* Una imagen está formada por capas (cada uno de los comandos utilizados en un Dockerfile menos el último).
* Todas estas capas son de solo lectura.
* La diferencia entre una capa y un contendor es que el contenedor crea una nueva capa (Container Layer o Thin R/W Layer) donde almacena todas las escrituras y lecturas efímeras.
* Los datos almacenados en la container layer son destruídos al eliminar el contenedor.
* Dos contenedores que comparten la misma imagen comparten el 100% de los datos en disco.
* Dos contenedores que usan diferentes imagenes pero existen capas identicas en las diferentes imagenes, comparten esos datos en disco.
* "copy_up" es el proceso de copiar un archivo de solo lectura que va a ser modificado y que se encuentra en alguna de las capas de la imagen a partir de la cual fue construido el contenedor, a la capa thin writable top layer del contenedor, es modificado el archivo y almacenado en esta capa (capa efimera). A copy_up operation can incur a noticeable performance overhead. This overhead is different depending on which storage driver is in use. Large files, lots of layers, and deep directory trees can make the impact more noticeable.
* Cabe destacar que el uso de Docker Compose está estrechamente relacionado con entornos de desarrollo y testing sobre un mismo servidor (docker-host). Para despliegues en producción es altamente aconsejable el uso de Docker Swarm sobre el que podremos desplegar contenedores en diferentes docker-host (nodos) haciendo uso de herramientas como docker service o docker stack, las cuales veremos más adelante u otras herramientas de orquestación como Kubernetes.
* Utiliza varios archivos docker-compose.yml así como docker-compose.override.yml para tener un repositorio de código único que te permita trabajar en varios entornos a la misma vez. Un ejemplo podría ser un archivo docker-compose.yml en el que indicamos exclusivamente los servicios finales a desplegar (servicio -> imagen -> versión), un archivo docker-compose.override.yml que nos permita recrear un entorno parecido al de producción, es decir creando volúmenes, usando secrets, etc... pero exponiendo puertos locales, hacer uso de bind-mounts de nuestros datos en desarrollo y llamando al comando build para compilar nuestra propia imagen y por último un docker-compose.testing.yml que usaremos en el servidor de CI para compilar la imagen (una vez probada en el paso de override y subida a nuestro repositorio de código) y un docker-compose.prod.yml que será el que finalmente exponga los puertos en producción, cree todos los volúmenes, haga uso de secrets y descargue la imagen de nuestro repositorio de imágenes en docker-hub.


11. Docker compose

    Docker compose será la herramienta que nos permita desplegar entornos completos formados por un importante número de containers (frontends, backends workers, SQL or Key Value databases, etc..) los cuales guardan relaciones entre ellos, como por ejemplo la ejecución en una misma red, puertos de comunicación, etc..

    Con Docker compose podremos mantener el despliegue de una infraestructura en un simple archivo YAML, sobre el que podremos definir la ejecución de diferentes containers, creación de Volumes o redes. El formato de este archivo es básico y además estandarizado, no obstante compose marca su propio formato que varia según la versión que estemos utilizando.

    Además Docker compose cuenta con una herramienta de línea de comandos "docker-compose" (CLI) usada normalmente para entornos de desarrollo o testing. A partir de la versión 1.13 de "docker-compose YAML file" es posible utilizarlo en entornos de produción junto con Swarm. 

   El archivo de configuración de docker compose por defecto es docker-compose.yml, no obstante podemos utilizar la opción -f de docker-compose para indicar que queremos iniciar con otro archivo.

   Ejemplo del archivo:

    version: '3.1'  # if no version is specificed then v1 is assumed. Recommend v2 minimum

    services:  # containers. same as docker run
      servicename: # a friendly name. this is also DNS name inside network
        image: # Optional if you use build:
        command: # Optional, replace the default CMD specified by the image
        environment: # Optional, same as -e in docker run
        volumes: # Optional, same as -v in docker run
      servicename2:

    volumes: # Optional, same as docker volume create

    networks: # Optional, same as docker network create


   En definitiva si quisieramos ejecutar un número determinado de "docker container run ..." podriamos crear un shell script línea a línea en el que cada una de ellas fuera el despliegue de un container, pero la forma mas profesional y siguiendo las buenas practicas de docker, es crear un archivo YAML para envitar tener que recordar por ejemplo cada una de las opciones del comando docker container run, además de simplificarse enormemente la forma de estructurar y desarrollar el despliegue.

   Un ejemplo básico en el que se pasa a YAML el comando con el que en la sección anterior desplegábamos Jekyll:

    version: '2'

    # same as 
    # docker run -p 80:4000 -v $(pwd):/site bretfisher/jekyll-serve

    services:
      jekyll:
        image: bretfisher/jekyll-serve
        volumes:
          - .:/site
        ports:
          - '80:4000'


   A continuación un ejemplo de un despliegue real en el que se integra un wordpress con su respectiva base de datos mysql y además se crea un volumen para la persistencia de datos de MySQL

    version: '2'

    services:

      wordpress:
        image: wordpress
        ports:
          - '8080:80'
        environment:
          WORDPRESS_DB_HOST: mysql
          WORDPRESS_DB_NAME: wordpress
          WORDPRESS_DB_USER: example
          WORDPRESS_DB_PASSWORD: examplePW
        volumes:
          - ./wordpress-data:/var/www/html

      mysql:
        image: mariadb
        environment:
          MYSQL_ROOT_PASSWORD: examplerootPW
          MYSQL_DATABASE: wordpress
          MYSQL_USER: example
          MYSQL_PASSWORD: examplePW
        volumes:
          - mysql-data:/var/lib/mysql

    volumes:
      mysql-data:

   Nota: te habrás fijado que hemos utilizado strings para especificar los puertos (ej. '8080:80' , HOST:CONTAINER, aunque también podría especificarse solo el del container y docker utilizará un puerto aleatorio en el host), esto se debe a que YAML parsea los puertos en el formato xx:yy como sexagesimal (base 60) por lo que es posible que obtengamos un comportamiento erróneo si utilizamos puertos en el container que se encuentran por debajo del 60. 

   Nota 2: compose acepta "./" como ruta relativa, en este caso indicaría el directorio donde nos encontramos al instante de lanzar el compose o mejor dicho (ver esto) el directorio en el que se encuentra el YAML. 

   Nota 3: cuando se utiliza el "-" al inicio de la clave valor, es porque estamos utilizando listas de valores.

        Diferencias:

            environment: {
                            WORDPRESS_DB_HOST: mysql,
                            WORDPRESS_DB_NAME: wordpress,
                            WORDPRESS_DB_USER: example,
                            WORDPRESS_DB_PASSWORD: examplePW
                        },
            volumes: [./wordpress-data:/var/www/html],
            ...

        En el primer caso utilizamos un diccionario clave valor, como valor de la clave environment, mientras que para la clave volumes estamos utilizando una lista de valores como valor de clave.

   Un comando interesante a utilizar dentro del docker-compose.yml es el "depens_on" este comando ayuda a compose a comprender la relación entre varios servicios, por ejemplo si tenemos un cluster de 2 mysql, en el segundo mysql quizás tengamos que indicar que depende del primer mysql. Veremos esto en secciones posteriores y como siempre para una información mas extendida podemos acceder a http://docs.docker.com/compose    

Docker compose CLI (command line)

Docker compose está mas orientado a entornos de desarrollo y test. Como ejemplo, imaginad levantar una máquina/entorno que cuente con todo lo necesario para comenzar a desarrollar y poder pararlo y volver a levantarlo si algo no ha ido bien durante el desarrollo. 

Referencias:

       https://docs.docker.com/compose/

14.1 Create a docker-compose.yml file filling all services (container) as you would like deploying.

    version: '3'

    services:
      ghost:
        image: ghost
        ports:
          - "80:2368"
        environment:
          - URL=http://localhost
          - NODE_ENV=production
          - MYSQL_HOST=mysql-primary
          - MYSQL_PASSWORD=mypass
          - MYSQL_DATABASE=ghost
        volumes:
          - ./config.js:/var/lib/ghost/config.js
        depends_on:
          - mysql-primary
          - mysql-secondary
      proxysql:
        image: percona/proxysql
        environment: 
          - CLUSTER_NAME=mycluster
          - CLUSTER_JOIN=mysql-primary,mysql-secondary
          - MYSQL_ROOT_PASSWORD=mypass
       
          - MYSQL_PROXY_USER=proxyuser
          - MYSQL_PROXY_PASSWORD=s3cret
      mysql-primary:
        image: percona/percona-xtradb-cluster:5.7
        environment: 
          - CLUSTER_NAME=mycluster
          - MYSQL_ROOT_PASSWORD=mypass
          - MYSQL_DATABASE=ghost
          - MYSQL_PROXY_USER=proxyuser
          - MYSQL_PROXY_PASSWORD=s3cret
        volumes:
            - mysql-primary-vol:/var/lib/mysql
      mysql-secondary:
        image: percona/percona-xtradb-cluster:5.7
        environment: 
          - CLUSTER_NAME=mycluster
          - MYSQL_ROOT_PASSWORD=mypass
       
          - CLUSTER_JOIN=mysql-primary
          - MYSQL_PROXY_USER=proxyuser
          - MYSQL_PROXY_PASSWORD=s3cret
        volumes:
            - mysql-primary-vol:/var/lib/mysql
        depends_on:
          - mysql-primary

    volumes:
        - mysql-primary-vol:

14.2 Principales comandos de docker-compose.

    14.2.1 Inicia todos los containers del compose.yml en segundo plano
    $ docker-compose up -d [-f compose-custom-name-file.yml]

    14.2.2 Visualiza los logs de los containers lanzados por compose
    $ docker-compose logs

    14.2.3 Visualiza los containers en ejecución pertenecientes al compose.yml
    $ docker-compose ps

    14.2.4 Visualiza los servicios que corren dentro de cada container
    $ docker-compose top

    14.2.5 Para los servicios y opcionalmente elimina todos los volúmenes creados y todas las imagenes (en general o solo las locales).
    $ docker-compose down [-v] [--rmi all|local]

    14.2.6 Lanza un compose que crea una imagen a partir de un dockerfile en runtime

        version: '2'

        services:
          proxy:
            build:
              context: .
              dockerfile: nginx.Dockerfile
            ports:
              - '80:80'
          web:
            image: httpd
            volumes:
              - ./html:/usr/local/apache2/htdocs/


    $ docker-compose up --build

15. Docker Swarm: service

15.1 Inicia un cluster docker swarm

    $ docker swarm init

    Nota: si fuese necesario, publicar la IP a través de la cual el resto de nodos podrán comunicarse con el Manager:

    $ docker swarm init --advertise-addr <IP>

15.2 Visualiza los nodos del cluster

    $ docker node ls

15.3 Crea un servicio con un solo nodo

    $ docker service create alpine ping 8.8.8.8
    $ docker service create --name drupal --detach=true --network backend -p 80:80 drupal

15.4 Visualiza los containers del cluster

    $ docker service ls

15.5 Mira información sobre un container/servicio concreto

    $ docker service ps <service-name>

15.6 Añade nuevos nodos al cluster

    $ docker swarm join-token manager
    $ docker swam join \
        <hash> \
        <ip>

15.6 Actualiza un servicio a 3 nodos
    
    $ docker service update <servicio> --replicas 3

15.7 Elimina un nodo del cluster

    $ docker container rm -f <node-name>

15.8 Crea un servicio con 3 nodos directamente

    $ docker service create --replicas 3 alpine ping 8.8.8.8

15.9 Crear una red para el cluster de nodos

    $ docker network create --driver overlay <nombre-de-red>

    Nota: es el mismo comando que en docker engine. El fin es el mismo, crear la red

15.10 Crear dos servicio en la red creada anteriormente

    $ docker service create --name psql --netowrk <nombre-de-red> -e POSTGRES_PASSWORD=mypass --mount type=volume,source=db-data,target=/var/lib/postgresql/data postgres:9.4

    $ docker service create --name drupal --network <nombre-de-red> -p 80:80 drupal

15.11 Scale in and rollbacks

    $ docker service scale web=4
    $ docker service rollback web

15.12 Update the image used to a newer version

    $ docker service update --image myapp:1.2.1 <service-name>

15.13 Añadir/Eliminar variables de entorno "on-fly"

    $ docker service update --env-add NODE_ENV=production <service_name>

15.14 Publicar puerto "on-fly"

    $ docker service update --publis-rm 8080 <service_name>

    NOTA: si hemos realizado cambios importantes y de "gran envergadura", es decir aumentado el número de nodos, eliminado variables de entorno y publicado nuevos puertos, podemos forzar la actualización de los servicios del cluster de Swarm:

        $ docker service update --force <service_name>

16. Docker Swarm: Production Grade Compose
    16.1 Docker Swarm Stacks

        Los stacks se diferencian de los servicios de swarm en que esto está mas orientado a producción y añaden el comando "deploy" con muchas opciones y agumentos para poder desplegar de forma segura los containers en un cluster de swarm en producción. Se escriben las recetas en compose-file también pero se ignora la directiva build (de existir dentro) ya que no se permite compilar imágenes en producción al igual que si desplegamos con "service" se omitira el comando deploy pero no el de build.

        16.1.1 desplegar un stack en producción

            $ docker stack deploy -c example-voting-app-stack.yml voteapp

        16.1.2 comprobar los stacks que tenemos desplegados

            $ docker stack ls

        16.1.3 Dentro de un stack, comprobar los servicios que forman el stack y están iniciados

            $ docker stack ps voteapp

    16.2 Secrets en Swarm

        Con secrets podemos administrar SSH-KEY, user/password, API Key, TLS Certificates, etc... de manera fiable. Existen dos formas de crear secres en docker swarm, bien através de la consola o desde un archivo y podremos añadirlos a la base de datos RAFTS de Swarm (que por defecto ya viene encriptada) con tan solo un comando.

        Si usamos secrest con compose en desarrollo (service) funcionará de una forma distinta si lo usamos en producción con "stacks".

        Se considera a los secrets entidades KEY:VALUE donde la KEY es el nombre que toma el archivo o el secret en si (cuando lo hacemos desde CLI con comando secret) y el valor es el valor que existe dentro del archivo o el que le hemos pasado por línea de comando.

        16.2.1 Crear un secret a partir de un archivo de texto

            $ docker secret create psql_usr psql_usr.txt

        16.2.2 Crear un secret a partir de la CLI

            $ echo "myDBpassWORD" | docker secret create psql_pass -
            $ openssl rand -base64 20 | docker secret create psql_pass - 

        16.2.3 Listar los secrets en la base de datos

            $ docker secret ls

        16.2.4 Comprobar el contenido de un secret

            $ docker secret inspect psql_usr

        16.2.5 Usar secrets en Swarm compose (desarrollo y local) a partir de los secrets generados anteriormente

            $ docker service create --name psql --secret psql_user --secret psql_pass -e POSTGRES_PASSWORD_FILE=/run/secrets/psql_pass -e POSTGRES_USER_FILE=/run/secrets/psql_user postgres

            Nota: si accedemos al container a los archivos /run/secrets podremos ver el contenido en plano de los secrets lo cual no es seguro

                $ docker exec -it psql.1.CONTAINER NAME bash

        16.2.6 Añadir o eliminar un secret "on-fly"

            $ docker service update --secret-rm | --secret-add

            nota: docker, re-creará de nuevo el servicio (containers afectados) por lo cual no es una buena técnica en base de datos

        16.2.7 Usar secret en Swarm stack

            $ vi docker-compose.yml
            version: "3.1"

            services:
              psql:
                image: postgres
                secrets:
                  - psql_user
                  - psql_password
                environment:
                  POSTGRES_PASSWORD_FILE: /run/secrets/psql_password
                  POSTGRES_USER_FILE: /run/secrets/psql_user

            secrets:
              psql_user:
                file: ./psql_user.txt
              psql_password:
                file: ./psql_password.txt


            Donde:
                $ cat psql_user.txt
                dbuser
                $ cat psql_password.txt
                QpqQcgD7dxVG

            $ docker stack deploy -c docker-compose.yml mydb

            Al eliminar un stack, también se eliminan los secrets que se crearon para el stack. Es decir son eliminados de la base de datos RAFT.

            $ docker stack rm mydb

        IMPORTANTE: otra forma de haberlo hecho es creando primero los secrets a través de la CLI usando el comando secret y a continuación utilizar el tomando "external:" dentro del compose indicando el nombre de los secrets a los que referenciamos.


17. Docker Heatlhchecks

* Soportado en Dockerfile, Compose YAML, docker run y Swarm services.
* Docker ejecuta los comandos desde dentro del container por lo que no es necesario ni exponer puertos, simplemente comprobará a modo local si el servicio está ok, por ejemplo usando curl en servidores webs
* El comando ejecutado espera un 0 o 1. Si el código es distinto de 0 la salida será definida como unhealthy.
* Los tres estados posibles para un container son: starting, healthy, unhealthy

    17.1 Stages
        1. Healthcheck status shows up in "docker container ls"
        2. Check last 5 healthckeck with "docker container inspect"
        3. Docker run does nothing with healtchecks. This action will be take by docker services/stacks
        4. Services will replaces tasks if they fail heatlhcheck, replacing that container with a new task on a new host possibly
        5. Services updates wait for them (new containers) before continuing

        Example

        docker run \
          --heatlh-cmd="curl -f localhost:9200/_cluster/health || false" \
          --health-interval=5s \
          --health-retries=3 \
          --heatlh-timeout=2s \
          --health-start-period=15s \
          --health-start-period=30 \
          elasticsearch:2

        Nota: de las opciones mas importante cabe destacar "start-period" la cual define un periodo de tiempo que se concede al servicio antes de que se lance una señal de "bad healthcheck result".



    
    
    



Sysdig Falco



