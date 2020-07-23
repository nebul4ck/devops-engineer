Setting up Jenkins CI/CD
########################

1. Instalar JDK 8
2. Instalar desde el repositorio oficial de Jenkins
3. Acceder a http://jenkins-server.nebul4ck.es:8080
4. Setear la password de admin (cuenta por defecto)
5. Instalar los plugins recomendados
6. Crear un nuevo admin user (nebul4ck)
7. Instalar plugins alternativos: **Build Timestamp**, **Permissive Script Security** y **Slack Notification**
8. Habilitar *SPDY* and *HTTP/2* :

.. code:: console

 cd /usr/share/jenkins
 wget https://repo.maven.apache.org/maven2/org/mortbay/jetty/alpn/alpn-boot/8.1.13.v20181017/alpn-boot-8.1.13.v20181017.jar
 vi /etc/default/jenkins
 ...
 JAVA_ARGS="-Djava.awt.headless=true -Xbootclasspath/p:/usr/share/jenkins/alpn-boot-8.1.13.v20181017.jar"
 ...        

9. Crear Token en Slack para setear por defecto un canal al que enviar el workflow (#jenkins-nebul4ck). Se crearán tantos TOKEN como canales/usuarios vayan a recibir el workflow (https://my.slack.com/services/new/jenkins-ci).
10. Crear las cuentas de slack:

  Jenkins > Administrar Jenkins > Credentials > Jenkins > Add domain > Slack > Add new credentials

  * Kind: Secret text
  * Scope: Global
  * Secret: <TOKEN>
  * ID: Jenkins-titan
  * Description: Token for '#jenkins-nebul4ck' channel
11. Crear una cuenta para administrar los Webhooks de Github:
12. Generar un token en la cuenta de jenkins (Github) para posteriormente utilizarlo como 'Secret text' en la cuenta que crearemos a continuación en Jenkins
13. Crear la cuenta en Jenkins para administrar los webhooks de GitHub:

  Credentials > Jenkins > Add domain > GitHub > Domain for GitHub projects.

  * Add Credentials
  * Kind: Secret text
  * Secret: <el token de github>
  * id: identificación de la cuenta
  * Descripción
14. Configurar Jenkins System

  Manage Jenkins > Configure system

  * Mensaje del sistema
  * Nro. ejecutores
  * Github (utilizar la cuenta token de github creada anteriormente)
  * Añadir canal de Slack predeterminado para recibir el workflow (utilizar la cuenta creada en la sección 7)
15. Parar Jenkins

.. code:: console

 systemctl stop jenkins
..
16. Cambiar todos los ficheros/carpetas con propietario jenkins a buanarepo: 

.. code:: console

 find / -user jenkins -exec chown -R buanarepo:buanarepo {} \;
..
17. Habilitar el plugin Permissive Script:

.. code:: console

 # vi /etc/default/jenkins
 ...
 JAVA_ARGS="-Djava.awt.headless=true -Dpermissive-script-security.enabled=true"
 JENKINS_USER=buanarepo
 JENKINS_GROUP=buanarepo
 JENKINS_LOG=/var/log/$NAME/$NAME.log
 ...
..
18. Iniciar de nuevo Jenkins

.. code:: console

 systemctl start jenkins
..
19. Desde el panel de jenkins (http://jenkins-server.nebul4ck.es:8080/log/levels) modificar el nivel de logs para la clase "*org.jenkinsci.plugins.permissivescriptsecurity.PermissiveWhitelist*"

.. code:: console

 org.jenkinsci.plugins.permissivescriptsecurity.PermissiveWhitelist, warning
..

20. Configurar la cuenta que controlará el repositorio local (Github):

* **Cuenta del sistema** (administrar el repositorio local/workspace):
        
.. code:: console

 $ su - buanarepo
 >>Si no tiene SSH-KEY: ssh-keygen -q -t rsa -C '' -N ''
 $ cat ~/.ssh/id_rsa (copiar la PRIVATE KEY)
..

 Jenkins > Credentials > Add domain > Github > Adding some credentials

 * Kind: SSH Username with private key
 * Scope: Global
 * Username: buanarepo
 * Private Key (Enter directly)
 * Passphrase: <empty>
 * ID: SSH buanarepo Account

* **Cuenta de GitHub**

.. code:: console

 $ su - buanarepo
 $ cat ~/.ssh/id_rsa.pub (copiar la clave Pública)
..

  Github: https://github.com/settings/profile

  SSH and GPG keys > New SSH key > Title (buanarepo user), Key (paste rsa.pub)