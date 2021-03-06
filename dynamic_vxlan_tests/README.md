# Generate and save vxlan domains and subnets.

Most of these environments can be on a shared flat network(ironic).  We can use a random multicast group and vxlan range to seperate out
the needed openstack networks. Some info needed is.

* Random multicast group compared against other domains to make sure its unique
* Random vxlan base id. We will increment and assign to each of the networks needed.
  * host/provision network: Provided from the existing flat network during provision. Also for the external haproxy floating ip.
  * management/container network:  Used for control plane management and communictions. Also the internal haproxy floating ip.
  * storage-management: Used on OSP envs
  * storage network: ceph, cinder backend communications.
  * lbaas network: octavia
  * inside-net: shared neutron private network
  * gateway-net: shared neutron external/gw network
  * tenant network: Tenant/tunnel neutron private networks.
  * ipmi network: simulated ipmi. (leaving out until we get into simulated envs)
  * ironic network: simulated ironic network (leaving out until we get into simulated envs)
  * a random id for haproxy(better if managed) to keep keepalived from conflicting with other clusters.

We are saving the multicast info at the domain object level and the vxlan info with the associated subnets. This info
should be available to both the config management solution for network and disk config.  It will eventually be available
for the osa/osp config using something like an ansible dynamic inventory scripts.

We are leaving the first 49 ips per network for any needed manual setup.  Ips 50 - 255 is used for forman ipam assignments
so we can make it easier to set up the used ips with osa later on.

## Testing out vxlan domain and subnet creation
```bash
# ./create_vxlan_domain.py 
Password: 

Domain: lab2.phobos.rpc.rackspace.com(LAB2 Dynamic Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: in-use value: yes
		name: multicast-group value: 239.1.33.230
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
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713507
		name: LAB2-STOR-MGMT
			desc: None
			network: 172.22.4.0/22
			gateway: 172.22.4.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.4.50 to: 172.22.4.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713508
		name: LAB2-STORAGE
			desc: None
			network: 172.22.8.0/22
			gateway: 172.22.8.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.8.50 to: 172.22.8.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713509
		name: LAB2-TENANT
			desc: None
			network: 172.22.12.0/22
			gateway: 172.22.12.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.12.50 to: 172.22.12.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713510
		name: LAB2-LBAAS
			desc: None
			network: 172.22.16.0/22
			gateway: 172.22.16.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.16.50 to: 172.22.16.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713511
		name: LAB2-INSIDE-NET
			desc: None
			network: 172.22.20.0/22
			gateway: 172.22.20.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.20.50 to: 172.22.20.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713512
		name: LAB2-GW-NET
			desc: None
			network: 172.22.24.0/22
			gateway: 172.22.24.1
			mask: 255.255.252.0
			cidr: 22
			from: 172.22.24.50 to: 172.22.24.255
			boot_mode: DHCP
			network_type: IPv4
			ipam: Internal DB
			param: name: type value: vxlan
			param: name: vxlan-id value: 7713513

```


## Cleanup all vxlan domains created for testing
```bash
 ./delete_all_vxlan_domains.py 
Password: 
Deleting lab2.phobos.rpc.rackspace.com
```
