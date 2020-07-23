Info about integrations
#######################

Github
******

* Los repositorios de Github están configurados para que solo determinados usuarios (mantenedores) puedan hacer push a la rama master.
* Será necesaria la revisión por parte de los mantenedores (designados en CODEOWNERS) de los pull requests antes del merge.
* El usuario *Jenkins* (jenkins) (con la SSH-KEY del usuario 'sshjenkins' del repositorio de producción) será colaborador con permisos de escritura en todos los repositorios. Este usuario cuenta como un usuario mas en 'github/nebul4ck'.
* **IMPORTANTE** Todos los repositorios integrados con Jenkins deberán de contar con el archivo Jenkinsfile (https://github.com/nebul4ck/jenkins/blob/master/vars/Jenkinsfile) y el archivo make_package.sh (https://github.com/nebul4ck/repo-skeleton-python/blob/master/make_package.sh) en su directorio raiz.
* Existe un TOKEN en la cuenta administrador de GitHub con el que el usuario 'sshjenkins' realiza acciones en el repostiorio mediante Buanaserver (principalmente para mantener el código de los servicios de terceros).


Jenkins
*******

Servicio
========

* El servicio se inicia con algunos parámetros extras:

.. code:: console

  vi /etc/default/jenkins
  ...
  JAVA_ARGS="-Djava.awt.headless=true -Dpermissive-script-security.enabled=true ..."
  ...
..

* El usuario 'sshjenkins' administra Jenkins. Será necesario hacer owner al usuario buanarepo de todos los archivos/directorios que maneje Jenkins. El workspace (/var/lib/jenkins/workspace) mantiene un repositorio local de cada uno de los repositorios integrados (Jobs en Jenkins). Estos repositorios son administrados por el usuario 'sshjenkins' por lo que este cuenta con una SSH-RSA-KEY utilizada en GitHub (cuenta de Jenkins Github).

Panel
=====

* Aunque otros métodos de autenticación son posibles (i.e integración con LDAP) actualmente se accede con la única cuenta creada (admin).
* Configurar una cuenta SSH (mediante SSH-KEY) para que Jenkins pueda acceder a los repositorios remotos: Credentials > Jenkins > Domains > Github > ID (SSH Username with private key)
* Integrado con Slack por lo que existe una cuenta configurada (Credentials > Jenkins > Domains > Slack > ID) para cada uno de los canales/usuarios a los que se enviará información del workflow. Cada cuenta es configurada con su respectivo TOKEN (Slack integration).
* Configurar un canal/usuario por defecto de Slack: Jenkins > Manage Jenkins > Configure System > Global Slack Notifier Settings > Base URL (https://nebul4ck.slack.com/services/hooks/jenkins-ci/) > Integration Token Credential ID > <Utilizar la cuenta creada anteriormente>

Pipeline
========

* Se han utilizado ambos tipos de Pipeline (Declarative y Scripted) en uno solo para contar con mayor flexibilidad, esto hay que tenerlo en cuenta ya que es necesario aplicar permisos sobre aquellas clases de Java que Jenkins considera de "riesgo". Esto se realiza instalando el pluging correspondiente e iniciando Jenkins con un parámetro adicional (permiso para todo, uso de groovy "sin limitaciones") o bien aceptando aquellos que sean necesarios en Jenkins > Manage Jenkins > In-process Script Approval.
* El pipeline está enfocado a modularizar cada una de las Stages en archivos independientes bajo la carpeta Jenkins/

Build Stage
===========

**Sistemas**

* El directorio */srv/buanarepo-build/<repo>* contiene un repositorio local para las app de terceros. Desde aquí se realizan pull/push cuando una aplicación de terceros respalda su configuración (buanaclient backup). Los cambios en los archivos DEBIAN se realizan desde nuestro repositorio local. Tanto el comando 'buanaclient backup' (para las config) como el commit de los archivos DEBIAN desde nuestro repositorio local desencadenan la misma acción en Jenkins -> construir el paquete (buanarepo mpkg) y testearlo a partir de su workspace en Jenkins.

**Desarrollo**

* El código es compilado con el último commit de la rama (master|develop) a partir de la fuente jenkins/workspace/<repo>. El comando que empaqueta es 'buanaclient mpkg' (ejecutado desde el Builder.groovy). CentralKB utiliza este repositorio para consultar la doc.
* Una vez integrado todo, el desarrollador solo tendrá que realizar commits/merge desde la rama 'develop' o 'master' (si es el mantenedor). Se irá informando del proceso por Slack.


Slack
*****

* Es necesario crear tantos TOKEN como usuarios/canales queramos integrar con Jenkins.

Otras notas
***********

* Cuando configuramos un webhooks es posible suscribirse a determinados eventos para recibir su payload. Por defecto los webhooks están únicamente suscritos al evento 'push': https://developer.github.com/webhooks/#service-hooks
* Integrar el estado del build en GitHub: https://stackoverflow.com/questions/14274293/show-current-state-of-jenkins-build-on-github-repo/26910986#26910986
* Firewall: The Hook URL is http://jenkins-server.nebul4ck.es:8080/github-webhook/ , and it needs to be accessible from the internet. If you have a firewall and such between GitHub and Jenkins, you can set up a reverse proxy and override the hook URL that Jenkins registers to GitHub, by checking "override hook URL" in the advanced configuration and specify to which URL GitHub should POST.
