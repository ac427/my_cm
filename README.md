### You can use the Vagrantfile to build the ansible admin node and run play book compute.yml to install and configure dhcp and dns
Steps:

```
vagrant up;vagrant ssh
```
### run below commands in terminal

```
[vagrant@admin ~]$ eval $(ssh-agent )
[vagrant@admin ~]$ ssh-add .ssh/root 
[vagrant@admin ~]$ git clone https://bitbucket.org/memoverflow/my_cm.git
[vagrant@admin ~]$ cd my_cm/ansible/
[vagrant@admin ansible]$ ansible-playbook -i hosts -u root cobbler.yml 
```
### one you import iso to cobbler you can start adding nodes using playbooks/add_node

### To import iso to cobbler
```
wget http://mirror.cs.vt.edu/pub/CentOS/7/isos/x86_64/CentOS-7-x86_64-Minimal-1511.iso -P /tmp
sudo mkdir -p /mnt/centos7
sudo mount -o loop /tmp/CentOS-7-x86_64-Minimal-1511.iso /mnt/centos7/
sudo cobbler import --path=/mnt/centos7/ --name=centos7-x86_64 --available-as=http://admin.home/centos7
``` 

### To add compute node, you can run below. Read playboks/add_node file for more info

```
#create a host_vars/<hostname> file FIRST!
ansible-playbook -i hosts -u root  --extra-vars "target=compute1 profile=centos7-x86_64" playbooks/add_node
```

