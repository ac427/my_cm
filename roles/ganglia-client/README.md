Role Name
=========

Installs ganglia-gmond. Make sure to include gangla data_source in group_vars

If the host will be part of a new data_source in Ganglia. Please make sure to add new name in ganglia_data_sources and the udp send channel hostname in groups_var/all. Also add the new data_source name as ganglia_group in  the groups_var/ansible hostgroup

