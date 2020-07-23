Create job from scratch
#######################

Development
***********

Configurar el repositorio remoto (Github)
=========================================

	i.e.: https://github.com/nebul4ck/hdfscleaner

* Añadir el archivo **CODEOWNERS** en la raiz de nuestro repositorio local

.. code:: console

    $ subl CODEOWNERS
    * nebul4ck
..
    
* Configura las restrinciones de la rama master:

 Settings > Branches > Branch protection rules > Add rule

 * Require pull request reviews before merging
 * Require review from Code Owners
 * Restrict who can dismiss pull request reviews
 * Restrict who can push to matching branches
                
* Añadir como colaborador del repositorio con premisos de escritura al usuario 'jenkins':

 Settings > Collaborators & Team > Add collaborator > jenkins


Configura el Job en Jenkins
===========================

* New Job

 Jenkins > Nueva tarea > Enter an item name: hdfscleaner >  Pipeline > Ok

 *El item name debe de coincidir con el nombre del repositorio*

  * Descripción: HDFSCleaner's pipeline.
  * GitHub project (check)
   - Project url: https://github.com/nebul4ck/hdfscleaner/
   - GitHub hook trigger for GITScm polling (check)
  * Pipeline:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repositories: 
    - Repository URL: git@github.com:nebul4ck/hdfscleaner.git
    - Credentials: sshjenkins (SSH jenkins Account on jenkins master server)
   - Avanzado:
    - Name: <empty>
    - Refspec: +refs/heads/master:refs/remotes/origin/master +refs/heads/develop:refs/remotes/origin/develop
   - Branches to build:
    - Branch Specifier (blank for 'any'): */master
   - Add Branch
    - Branch Specifier (blank for 'any'): */develop
        
  * Script Path: Jenkins/Jenkinsfile
  * Lightweight checkout: (check)
            
 Apply Guardar

* Ejecutar de forma manual el pipeline: esto es necesario hacerlo para que Jenkins cree de forma automática un webhook en GitHub

 Jenkins > hdfscleaner > Schedule a Build for hdfscleaner
    
* Deshabilitar la verificación SSL en el repositorio de Github:
 Settings > Webhooks > Edit > SSL Verification > Disable (not recommended) (check)

* Lanzar *commit* desde la rama develop o master del repositorio local.


Sistemas        
********
                
Inicializar el repositorio
==========================

Crear el repositorio a partir del *src* del servicio de terceros.
    
1. Descargar el .tar.gz o .deb (ej, hdfscleaner from https://github.com/nebul4ck/hdfscleaner)
2. Iniciar un nuevo repositorio de Github con el nombre del nuevo servicio (hdfscleaner)
3. Clonar el nuevo repositorio
4. Descomprimir el paquete y crear la estructura de paquete DEBIAN:

.. code:: console

	$ pwd
	git-projects/hdfscleaner/

	$ tree
	.
	├── CODEOWNERS
	├── Jenkins
	│   ├── Builder.groovy
	|	├── checkup.groovy
	|	├── deployer.groovy
	|	├── discoveryRelease.groovy
	|	├── masterPipeline.groovy
	|	├── taggerRelease.groovy
	|	├── testing.groovy
	│   └── Jenkinsfile
	├── hdfscleaner
	│   ├── DEBIAN
	│   │   ├── control
	│   │   ├── postinst
	│   │   ├── postrm
	│   ├── etc
	│   │   └── logrotate.d
	│   │       └── hdfscleaner
	│   ├── opt
	│   │   └── hdfscleaner
	│   │       ├── bin
	│   │       ├── config
	│   │       ├── libs
	│   │       ├── LICENSE
	│   │       ├── NOTICE
	│   │       └── version
	│   └── usr
	│       └── bin
	│           └── hdfscleaner
	└── README.md
..

5. Add&push