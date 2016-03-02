# Ansible code to provison infrastructue compute (WIP). The code is tested on a virtualbox private network 
My virtualbox setup

 1. Admin node with 2 interface, 1 as bridge network and 2nd internal
 2. Multiple compute nodes with internel network cards
 3. Admin node runs squid proxy and cobbler
 4. DNS and DHCP is managed via cobbler on Admin node

# Playbook definition
 - playbooks/add_node will add a new node to cobbler 
