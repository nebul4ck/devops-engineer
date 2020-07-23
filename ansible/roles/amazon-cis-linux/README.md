
Introduction
------------

This ansible role applies v2.0.0 of the CIS Amazon Linux Benchmark. <https://benchmarks.cisecurity.org/tools2/linux/CIS_Amazon_Linux_Benchmark_v2.0.0.pdf>

This role was developed and tested against Amazon Linux 2016.03. It has been tested against Amazon Linux 2016.09 with equal success.

Amazon Linux and SE Linux
----------------
By default SElinux is disabled via grub in amazon linux.

To enable edit ;

```/boot/grub/menu.lst```

Modifiy ```selinux=0  to  selinux=1```

```touch /etc/selinux/config```

Also install the following package to allow the ansible SElinux module to function on the host.

```yum install libselinux-python```

A reboot will be neccessary for the changes to take effect.

Example Playbook
----------------

An example playbook which uses this role is as follows:

```
---

- hosts: localhost
  connection: local
  gather_facts: true
  become: yes

  roles:
    - cis-amazon-linux
```

A more advanced example, which includes modifications to the default values used, as well as the exclusion of some items in the benchmark which are considered unnecessary for a fictional environment, is as follows:

```
---

- hosts: localhost
  connection: local
  gather_facts: true
  become: yes

  vars:
    cis_level_1_exclusions:
      - 5.4.4
      - 3.4.2
      - 3.4.3
      - 6.2.13
    cis_pass_max_days: 45
    cis_umask_default: 002

  roles:
    - cis-amazon-linux

```

Note that the use of ```become: yes``` is required as 99% of tasks require privileged access to execute.

Role Variables
--------------

See ```defaults/main.yml``` for variables which can be overriden according to preference.

Options
-------

Tags (and combinations thereof) can be used to run a particular level of the CIS standard, a section, or an individual recommendation. For example:

* Run only Level 1 tasks

```
ansible-playbook playbook.yml -t level-1
```

* Run only Section 3 tasks

```
ansible-playbook playbook.yml -t section-3
```

* Run tasks 1.3.1 and 2.2.10 only

```
ansible-playbook playbook.yml -t 1.3.1,2.2.10
```

* Run scored tasks only

```
ansible-playbook playbook.yml -t scored
```

Limitations
-----------

At present, only the Level 1 items of the benchmark are implemented. Level 2 items will be added as time permits.

The following checks have not been implemented:

* 3.6.2. Firewall rulesets are environment specific.
* 3.6.3. Firewall rulesets are environment specific.
* 3.6.4. Firewall rulesets are environment specific.
* 3.6.5. Firewall rulesets are environment specific.
* 4.2.1.2. The determination of what should be logged and the destination of messages is environment specific.
* 4.2.2.2. The determination of what should be logged and the destination of messages is environment specific.
* 4.2.2.3. Inline editing of syslog-ng configuration file is considered too imprecise and is best solved by a supplied configuration file which addresses this and other related requirements.
* 4.2.2.4. Inline editing of syslog-ng configuration file is considered too imprecise and is best solved by a supplied configuration file which addresses this and other related requirements.
* 4.2.2.5. Inline editing of syslog-ng configuration file is considered too imprecise and is best solved by a supplied configuration file which addresses this and other related requirements.
* 4.3. The configuration of logrotate is site-specific.
* 5.3.2. Multi-line editing of pam configuration files is considered too imprecise and dangerous, and is best solved by a supplied configuration file which addresses this and other related requirements.
* 5.3.3. Multi-line editing of pam configuration files is considered too imprecise and dangerous, and is best solved by a supplied configuration file which addresses this and other related requirements.

Compatibility
-------------

This role is compatible with the following versions of ansible:

* 2.3
* 2.4
* 2.5
* 2.6
* 2.7

This role has not been tested against any other versions of ansible.

License
-------

MIT.

Author Information
------------------

This role was developed by [Anth Courtney](https://au.linkedin.com/in/anthcourtney).

All feedback, issues and PRs are encouraged and appreciated.
