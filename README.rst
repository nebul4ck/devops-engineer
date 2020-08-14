
Index
#####

Ansible
=======

Roles
-----

* **buanarepo**
* **cerebro**
* **configure_os_kernel**
* **curator**
* **dnsmasq**
* **druid**
* **elasticsearch**
* **haproxy**
* **hdfs**
* **influxdb**
* **kafka**
* **kibana**
* **logstash**
* **mongodb**
* **mosquitto**
* **postgresql**
* **redis**
* **spark**
* **vernemq**
* **zookeeper**
* **utils**
* **amazon-cis-linux**

AWS
===

CloudFormation Templates
------------------------

* **Example template**
* **ALB**
* **EC2**
* **ROLE**
* **S3**
* **multi-aws-cli.sh**: shell script which you can use to test, get info, delete and deploy cloudformation stack from CLI.

Jenkins
=======

Jenkins pipeline is an own self illustration how jenkins groovy shared library works. For a full work, it needs a third party software like buanarepo. Jenkins is integrated with github, buanarepo (build debian packages, backups and encrypted ownself tool write in python) and slack.

During the stages, **Jenkins clone the code from github repository** (develop or master branch, it is depend of the commit that the developer did), after that, a **test cycle is launched into development environment** and if all work fine, **jenkins up the software version**, **auto-merge master and development branches**, **tags the new version** on github and finally, clone the master branch and **deploy the code on production environment**.

**Note** much more info into jenkins > docs folder

**Shared libary**

* Use this shared library to build, test, deploy in staging and production environments. This shared library can be use to create multiple projects/pipeline with a unique pipeline code. The main function is parametrizable and called by Jenkinsfile.

Scripting/SysAdmin
==================

**Useful scripts to automated tasks**

* scripts/ubuntu-kde/shortcuts -> Creating Kubuntu/ubuntu shortcuts with Vagrant
* scripts/ubuntu-kde/plasma-widget-save-restore -> save & restore KDE Desktop widgets and shortcuts design
* scripts/sysadmin/create-swap.sh -> create swap from comand line using /swap_file
* scripts/vagrant/create_vm.sh -> Create and orchestrate one or more virtual machine in few seconds.
* debian_packages/psmen -> view processes using advanced ps command options in tree+forks and used memory by each of them by easy way.
* prog/mongostats -> useful tool for view and monit mongo database

debian_packages/psmen
---------------------

1. Clone this repository
2. go to debian_package folder
3. create debian package
   
.. code:: console

    $ dpkg -b psmem/ psmem.deb
..

4. Install psmem

.. code:: console

    $ sudo apt install ./psmem.deb

5. use psmem
   
.. code:: console

    $ psmem agonzalez
    agonzalez             1,7M      \_ /bin/sh /usr/bin/startkde
    agonzalez             320K          \_ /usr/bin/ssh-agent /usr/bin/im-launch /usr/bin/startkde
    agonzalez             7,0M          \_ kwrapper5 /usr/bin/ksmserver
    agonzalez             7,8M /lib/systemd/systemd --user
    agonzalez             2,6M  \_ (sd-pam)
    agonzalez             4,8M  \_ /usr/bin/dbus-daemon --session --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
    agonzalez              35M  \_ /usr/bin/kglobalaccel5
    agonzalez             4,9M  \_ /usr/lib/dconf/dconf-service
    agonzalez              27M  \_ /usr/bin/kactivitymanagerd start-daemon
    ...
..

**note**: psmem let us to see all processes of agonzalez user. You can get all process of concrete service. ($ psmem httpd) 

prog/mongostats
---------------

1. Launch a python virtualenv
2. run mongostats.py

.. code:: console

    $ . bin/activate
    $ python mongostats.py
..
