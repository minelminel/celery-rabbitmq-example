# Ansible Notes

- Ansible is a Configuration Management, Deployment & Orchestration tool
- It is a "Push-based" configuration tool
- Agentless, requires only a network connection, usually SSH

#### Features
- Simple to install and setup
- No need for any agent or client software to manage the nodes (remote machines)
- Capabilities to model complex IT workflows and orchestrate your entire IT workflow
- Extensible with modules written in any programming language

#### Ansible Architecture

- Inventory: List of IP addresses of all host machines
- Playbook: Describes the entire workflow of your systems
  - Modules: Part which is executed on each machine
  - APIs: Only there to support the command line tools
  - Plugins: Special kind of module which allows execution of Ansible task as a job build step
    - examples include Connection plugins for connecting to Docker environments, and Action plugins which perform steps within a GUI
- CMDB: Configuration Management Database, stores repository artifacts
- Hosts: Remote locations upon which provisioning and monitoring is performed

#### Playbook
Each playbook starts with three dashes across the top `---`

`Hosts` - list of all host machines (remote addresses)

`Variables` - gathering facts produces variables

`Tasks` - steps to be performed on the host machine, these tasks are always executed in the same order which they are written

`Handlers` - tasks that require a trigger from a normal task (uses Notify)

# Use Cases
#### Orchestration
Allows simple execution of commands across many remote hosts

#### Provisioning
For installing various necessary software in order to develop an application

#### Deployment
Configures placement of artifacts, modules, and packages

#### Security & Compliance
Lock down firewalls, user credentials, network rules

# Hands-On Example
```bash
ansible --version

# host inventory file, each with an IP and a host group
vim /etc/ansible/hosts
# here, our host group is 'test-servers'

# test ssh connection using ansible
ansible -m ping 'test-servers'
```

## Provisioning
`lampstack.yml`
```yml
---
name: install apache, php, mysql
hosts: test-servers
become: true
become_user: root
gather_facts: true
tasks:
  - name: "Install apache2"
    package: name=apache2 state=present

  - name: "Install apache2-php5"
    package: name=libapache2-mod-php state=present

  - name: "Install php-cli"
    package: name=php-cli state=present

  - name: "Install php-mcrypt"
    package: name=php-mcrypt state=present

  - name: "Install php-gd"
    package: name=php-gd state=present

  - name: "Install php-mysql"
    package: name=php-mysql state=present

  - name: "Install mysqlserver"
    package: name=mysql-server state=present
```
(the opposite of `present` is `absent`)

NOTE: always be careful with the indentation to avoid unnecessary errors! Lines which have the same indentation are referred to as `siblings`

Run the playbook
```bash
ansible-playbook lampstack.yml
```

## Orchestration
`mysqlmodule.yml`
```yml
---
hosts: all
remote_user: root

tasks:
  -name: Install PIP
   apt: name=python-pip state=present

  -name: Install libmysqlclient-dev
   apt: name=libmysqlclient-dev state=present

  -name: Install the Python MySQL module
   pip: name=MySQL-python

  -name: Create database user edureka
   sql_user: name=edureka password=edureka priv=*.*:ALL state=present

  -name: Create the database edu
   mysql_db: db=edu state=present

  -name: Create a Table reg
   command: mysql -u edureka -pedureka -e 'CREATE TABLE reg (name varchar(30), email varchar(30));' edu
```

Run the playbook
```bash
ansible-playbook mysqlmodule
```

## Deployment
`deploywebsite.yml`
```yml
---
name: Copy
hosts: test-servers
become: true
become_user: root
gather_facts: true
tasks:
  - name: "Copy file"
    copy: src=/home/edureka/Documents/index.html dest=/var/www/html/index.html

  - name: "Copy file"
    copy: src=/home/edureka/Documents/process.php dest=/var/www/html/process.php

  - name: "Copy file"
    copy: src=/home/edureka/Documents/result.php dest=/var/www/html/result.php
```

Run the playbook
```bash
ansible-playbook deploywebsite
```
