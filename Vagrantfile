Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.network "private_network", ip: "172.16.1.10", virtualbox__intnet: "home_network" 
  config.vm.hostname = "admin.home"
  config.vm.provider "virtualbox" do |v|
   	v.memory = 1024
     	v.cpus = 2
        v.gui = true
  end
  config.vm.provision "shell", inline: <<-SHELL
         yum -y update
         yum install  -y vim wget git epel-release  bind-utils screen libselinux-python
	 yum -y update
         yum -y install ansible
         sed -i.bak "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
	 bash -c "cat << EOF > /etc/resolv.conf
search home
nameserver 172.16.1.10
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF"
	 sed -i.bak_$(date +%s) "s/^NM_CONTROLLED/#NM_CONTROLLED/g" /etc/sysconfig/network-scripts/ifcfg-eth0
	 sed -i.bak_$(date +%s) "s/^NM_CONTROLLED/#NM_CONTROLLED/g" /etc/sysconfig/network-scripts/ifcfg-eth1
	 sed -i.bak_$(date +%s) "s/^PEERDNS/#PEERDNS/g" /etc/sysconfig/network-scripts/ifcfg-eth0
	 sed -i.bak_$(date +%s) "s/^PEERDNS/#PEERDNS/g" /etc/sysconfig/network-scripts/ifcfg-eth1
	 echo "NM_CONTROLLED=no" >> /etc/sysconfig/network-scripts/ifcfg-eth0
	 echo "NM_CONTROLLED=no" >> /etc/sysconfig/network-scripts/ifcfg-eth1
	 echo "PEERDNS=no" >> /etc/sysconfig/network-scripts/ifcfg-eth0
	 echo "PEERDNS=no" >> /etc/sysconfig/network-scripts/ifcfg-eth1
###### Copy root keys to vagrant user 
	yes |  bash -c "ssh-keygen -f ~/.ssh/id_rsa -t rsa  -N '' "
	mkdir -p /home/vagrant/.ssh
###### Doing to run commands as root via ssh-agent , Kow what you are doing while using this file
	cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
	chmod 0600 /root/.ssh/authorized_keys
	cp /root/.ssh/id_rsa /home/vagrant/.ssh/root
	chmod 0600 /home/vagrant/.ssh/root	
	chown -R vagrant:vagrant /home/vagrant/.ssh/ 
	ssh-keyscan localhost >> /home/vagrant/.ssh/known_hosts
#	init 6
  SHELL
end
