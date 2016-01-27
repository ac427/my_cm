
# Ansible code to provison infrastructue compute (WIP). The code is tested on a virtualbox private network 
My virtualbox setup
 1. Admin node with 2 interface, 1 as bridge network and 2nd internal
 2. Multiple compute nodes with internel network cards
 3. Admin node runs squid proxy and cobbler
 4. DNS and DHCP is managed via cobbler on Admin node

# Ansible Role definition
 - role base will install sudo users and copy ssh_known_hosts of all hosts and will also run yum update and install some basic packages
 - role ldap will configure openldap server ( no encryption for now)
 - role openldap_client will configure all nodes as openldap clients
 - role ceph will install ceph server ( WIP)
