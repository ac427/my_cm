# -*- mode: ruby -*-

# vi: set ft=ruby :

puppetboxes = [
    {
        :name => "puppetca",
        :mem => "512",
        :cpu => "1" ,
        :mac => "08:00:27:dd:da:b8"
    },
    {
        :name => "puppetdb",
        :mem => "512",
        :cpu => "1" ,
        :mac => "08:00:27:66:df:f4"
    }
#   {
#        :name => "foreman",
#        :mem => "512",
#        :cpu => "1"
#    }
]

Vagrant.configure("2") do |config|
  config.vm.define "admin" do |admin|
 	admin.vm.box = "centos/7"
  admin.vm.hostname = 'admin'
  admin.vm.network :private_network, ip: "172.16.1.10", netmask: "255.255.0.0", mac: "0800276464d9", virtualbox__intnet: "home_network" 
  admin.vm.provider :virtualbox do |v|
		    v.memory = 1024
    		v.cpus = 2
    		v.gui = true
    		v.name = "admin"
  end
	admin.vm.provision "shell", inline: <<-SHELL
	  yum -y update
		yum install  -y vim wget git epel-release  bind-utils screen libselinux-python
		yum -y update
		yum -y install ansible
		sed -i.bak "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
		bash -c "cat << EOF > /etc/resolv.conf
search home
nameserver 172.16.1.11
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF"
		git clone https://github.com/ac427/my_cm.git
		sed -i.bak_$(date +%s) "s/^PEERDNS/#PEERDNS/g" /etc/sysconfig/network-scripts/ifcfg-eth0
		sed -i.bak_$(date +%s) "s/^PEERDNS/#PEERDNS/g" /etc/sysconfig/network-scripts/ifcfg-eth1
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
		echo "172.16.1.11 cobbler cobbler.home"  >> /etc/hosts
		init 6
	SHELL
  end

 config.vm.define "cobbler" do |cobbler|
 cobbler.vm.box = "centos/7"
 cobbler.vm.hostname = 'cobbler'
 cobbler.vm.network :private_network, ip: "172.16.1.11", netmask: "255.255.0.0",  mac: "080027ab5bcf", virtualbox__intnet: "home_network" 
 cobbler.vm.provider :virtualbox do |v|
    		v.memory = 1024
    		v.cpus = 1
    		v.gui = true
    		v.name = "cobbler"
 end
 cobbler.vm.provision "shell", inline: <<-SHELL
    bash -c "cat << EOF > /home/vagrant/cobbler.sh
wget http://mirror.cs.vt.edu/pub/CentOS/7/isos/x86_64/CentOS-7-x86_64-Minimal-1511.iso -P /tmp
sudo mkdir -p /mnt/centos7
sudo mount -o loop /tmp/CentOS-7-x86_64-Minimal-1511.iso /mnt/centos7/
sudo cobbler import --path=/mnt/centos7/ --name=centos7-x86_64 --available-as=http://admin.home/centos7
EOF"
    ###some how copy the admin hosts root id_rsa.pub to here ie; admin:/root/.ssh/id_rsa.pu /root/.ssh/authorzied_keys
    ## looks like sync folder doesn't share files across vms  
    chmod +x /home/vagrant/cobbler.sh
    sed -i.bak "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
    bash -c "cat << EOF > /etc/resolv.conf
search home
nameserver 172.16.1.11
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
    init 6
  SHELL
  end
	
 config.vm.define "compute1" do |compute1|
 compute1.vm.box = "centos/7"
 compute1.vm.hostname = 'compute1'
 compute1.vm.network :private_network, mac: "080027C282F3", virtualbox__intnet: "home_network"
 compute1.vm.provider :virtualbox do |v|
                v.memory = 1024
                v.cpus = 1
                v.gui = true
                v.name = "compute1"
 end
 compute1.vm.provision "shell", inline: <<-SHELL
	   sed -i.bak "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
	   init 6
 SHELL
 end

  puppetboxes.each do |opts|
    config.vm.define opts[:name] do |config|
      config.vm.box= "centos/7"
      config.vm.hostname = opts[:name]
      config.vm.provider "virtualbox" do |v|
        v.memory = opts[:mem]
        v.cpus = opts[:cpu]
        v.name = opts[:name]
        end
      config.vm.network :private_network, mac: opts[:mac],virtualbox__intnet: "home_network"
      end
  end
end
