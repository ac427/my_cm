# Configure Jenkis

- all screenshots are in my_cm/ansible/roles/ansible_jenkins_role/images directory ( don't run jenkins.yml like in screenshot, it will make your jenkins crash as the playbook tries to restart jenkins service) 
- configure jenkins host by running jenkins.yml
- Manually copy the admin host root ssh key(id_rsa) as /var/lib/jenkins/root on jenkins host 
- Reset password for user jenkins on jenkins host to whatever you want


# Login  & Initial setup

- ssh -p 2002 -X vagrant@localhost 
- launch firefox and open http://localhost:8080
- Navigate to, Manage Jenkins - Configure Systems -  add SSH remote hosts ( check screenshot) 
 
#  Project setup 

- New item -- > give some name --> Freestyle project --> ok
- Source Code Management --> Git--> give github url 
- check Poll SCM and give how fequently you want to run / or when to run, self explanatory 
- check Build Environment - > Execute shell script on remote host using ssh	
- You can run ansible-playbook in Pre build script /Post build script
```
      $ ansible-playbook -i /home/vagrant/my_cm/ansible/hosts --tags=plugin -u root  /home/vagrant/my_cm/ansible/base.yml
```
- check SSH Agent -> it shoud auto select the account we added before 

