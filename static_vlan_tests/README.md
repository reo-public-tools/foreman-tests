# Checking that we can check in/out vlan domains

## Test the api scripts to check out and release a domain

### Testing the check out actions
```bash
[root@lab-deploy01 static_vlan_tests]# ./check_out_vlan_domain.py 
Password: 
Found domain: id: 2 name: lab1.phobos.rpc.rackspace.com fullname: LAB1 Static Domain
Domain lab1.phobos.rpc.rackspace.com is free to use
Domain lab1.phobos.rpc.rackspace.com is of type vlan
Domain lab1.phobos.rpc.rackspace.com is free to check out

Domain: lab1.phobos.rpc.rackspace.com(LAB1 Static Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: in-use value: yes
		name: type value: vlan
	Subnets:
		network: 172.20.64.0/22       name: LAB1-MGMT            desc: LAB1 management network with static VLANs
		network: 172.20.68.0/22       name: LAB1-STOR-MGMT       desc: LAB1 storage management network with static VLANs
		network: 172.20.72.0/22       name: LAB1-STORAGE         desc: LAB1 storage network with static VLANs
		network: 172.20.76.0/22       name: LAB1-TENANT          desc: LAB1 tenant network with static VLANs
		network: 172.20.80.0/22       name: LAB1-LBAAS           desc: LAB1 lbaas network with static VLANs
		network: 172.20.84.0/22       name: LAB1-INSIDE-NET      desc: LAB1 inside net network with static VLANs
		network: 172.20.88.0/22       name: LAB1-GW-NET          desc: LAB1 gateway net network with static VLANs


[root@lab-deploy01 static_vlan_tests]# ./check_out_vlan_domain.py 
Password: 
Found domain: id: 2 name: lab1.phobos.rpc.rackspace.com fullname: LAB1 Static Domain
Domain lab1.phobos.rpc.rackspace.com is of type vlan
Domain lab1.phobos.rpc.rackspace.com is either the wrong type or in use

```


### Testing the release actions
```bash
[root@lab-deploy01 static_vlan_tests]# ./release_vlan_domain.py 
Password: 
Found domain: id: 2 name: lab1.phobos.rpc.rackspace.com fullname: LAB1 Static Domain
Domain lab1.phobos.rpc.rackspace.com is of type vlan
Domain lab1.phobos.rpc.rackspace.com is free to check out

Domain: lab1.phobos.rpc.rackspace.com(LAB1 Static Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: in-use value: no
		name: type value: vlan
	Subnets:
		network: 172.20.64.0/22       name: LAB1-MGMT            desc: LAB1 management network with static VLANs
		network: 172.20.68.0/22       name: LAB1-STOR-MGMT       desc: LAB1 storage management network with static VLANs
		network: 172.20.72.0/22       name: LAB1-STORAGE         desc: LAB1 storage network with static VLANs
		network: 172.20.76.0/22       name: LAB1-TENANT          desc: LAB1 tenant network with static VLANs
		network: 172.20.80.0/22       name: LAB1-LBAAS           desc: LAB1 lbaas network with static VLANs
		network: 172.20.84.0/22       name: LAB1-INSIDE-NET      desc: LAB1 inside net network with static VLANs
		network: 172.20.88.0/22       name: LAB1-GW-NET          desc: LAB1 gateway net network with static VLANs


[root@lab-deploy01 static_vlan_tests]# ./release_vlan_domain.py 
Password: 
Found domain: id: 2 name: lab1.phobos.rpc.rackspace.com fullname: LAB1 Static Domain
Domain lab1.phobos.rpc.rackspace.com is free to use
Domain lab1.phobos.rpc.rackspace.com is of type vlan
Domain lab1.phobos.rpc.rackspace.com is already released

```
