= Introduction =

Example REST API provisioned with docker inside a virtual machine provisioned with ansible.
The used stack is: docker, mariadb, python, flask, flask-sqlalchemy, flask-cache.

= Requirements =

It is necesary to have ansible and vagrant installed on the host machine, as this tools will be used to provision the vagrant virtual machine.

= Usage =

Run "./main.sh start" to create the vm, provision everything and launch the app. Then point your browser to http://localhost:8080
 Port mappings may be modified within the Vagrantfile.

Run "./main.sh stop" to stop the vagrant vm.

Run "./main.sh restart" to restart the vm.

Run "./main.sh destroy" to delete the vm from disk.

= Procedure =

1) The virtual machine is created and managed by vagrant and provisioned by ansible.
2) Ansible runs a playbook with two roles: "docker" and "api". These roles setup docker within the vm and perform the deployment of the api application.
3) After docker has been successfully installed, using docker-compose, ansible is going to pull the required docker images, and startup them.
4) The MariaDB, Phpmyadmin and api instances are created and launched by docker-compose.
5) After the services are up, the api role will try to initialize the database and then restart the services.

= Other notes =

The flask-cache was implemented only in local mode, it should not be hard to setup redis, but I was running out of time.
Unit tests are missing, just a skeleton of them is provided.
