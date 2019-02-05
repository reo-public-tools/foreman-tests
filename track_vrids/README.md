# Allocating external/internal keepalived vids for haproxy

osa uses keepalived with haproxy for the external and internal floating vips. This
requires unique virtual_router_ids for each VRRP. By default osa uses 10 and 11 for
the ids on all clusters.  When we have multiple clusters on the same flat ironic
network we will need to make sure the external virtual router id is unique in each
environment.  We will go ahead make the internal id unique as well just in case.

Modifications were made to automatically allocate them on a new dynamic vxlan
domain creation.  The domain params are external_vrid and internal_vrid. For 
static vlan domains, we just set/delete the params for that domain. A function
is used on either to pull a random id between 1 and 254 and verify its not
already in use.

Since the dynamic vxlan domain creation script work was done on the backend, we
just symlinked the scripts over from the previous tests and dumped the params
to stdout to make sure we have the params set.


## Dynamic vxlan domain tests.
```bash
(foreman-tests-venv) [root@lab-deploy01 track_vrids]# ./create_vxlan_domain.py | head -n 20
Password: 

Domain: lab2.phobos.rpc.rackspace.com(LAB2 Dynamic Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: external_vrid value: 140
		name: internal_floating_ip value: 172.22.0.10
		name: internal_vrid value: 5
		name: in-use value: yes
		name: multicast-group value: 239.1.33.205
		name: type value: vxlan
	Subnets:
		name: LAB2-MGMT
			desc: None
			network: 172.22.0.0/22
			gateway: 172.22.0.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.0.50 to: 172.22.0.255
			boot_mode: DHCP
(foreman-tests-venv) [root@lab-deploy01 track_vrids]# ./delete_all_vxlan_domains.py 
Password: 
Deleting lab2.phobos.rpc.rackspace.com

```



## Static vlan domain test

```bash
(foreman-tests-venv) [root@lab-deploy01 track_vrids]# ./test.py 
Password: 
Authenticating and setting some env info
Domain Info Before Changes

Domain: lab1.phobos.rpc.rackspace.com(LAB1 Static Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: internal_floating_ip value: 172.20.68.10
		name: in-use value: no
		name: type value: vlan
Found free external virtual router id: 240
Found free internal virtual router id: 198
Setting external_vrid on lab1 to 240
Setting internal_vrid on lab1 to 198
Info After Changes

Domain: lab1.phobos.rpc.rackspace.com(LAB1 Static Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: external_vrid value: 240
		name: internal_floating_ip value: 172.20.68.10
		name: internal_vrid value: 198
		name: in-use value: no
		name: type value: vlan
Sleeping 20
Deleting external_vrid param for lab1
Deleting internal_vrid param for lab1
Info After Delete

Domain: lab1.phobos.rpc.rackspace.com(LAB1 Static Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: internal_floating_ip value: 172.20.68.10
		name: in-use value: no
		name: type value: vlan

```
