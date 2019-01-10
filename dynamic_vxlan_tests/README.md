# Generate and save vxlan domains and subnets(TODO).

Most of these environments can be on a shared flat network.  We can use a random multicast group and vxlan range to seperate out
the needed openstack networks. Some info needed is.

* Random multicast group
* Random vxlan base id. We will increment and assign to each of the networks needed.
  * host/provision network: Provided from the existing flat network during provision. Also for the external haproxy floating ip.
  * management/container network:  Used for control plane management and communictions. Also the internal haproxy floating ip.
  * vlan network: Tenant neutron vlan networks
  * vxlan network: Tenant neutron private networks.
  * storage network: ceph, cinder backend communications.
  * lbaas network: octavia
  * ironic network: ironic python agent and provisioning
  * ipmi network: ironic out of band ipmi provisioning.
  * a random id for haproxy(better if managed) to keep keepalived from conflicting with other clusters.

With foreman we can create subnets and save some metadata for each of these.  We will probably want to save the multicast info somewhere
at a higher scope, such as the environment, location...  We will need all of this information to configure the vxlan(or vlan) interfaces
, bridges, ip addresses and static routes needed to be setup before openstack is installed.  We will also need all of this info to be
available to do some auto-configuration of things like openstack-ansible, redhat osp, or whatever openstack deployment system you are
working with. We should be able to set this up in such a way that the subnets will get assocaited to hosts and handle all of the
ip management for us.  The dhcp smart proxy also has an infoblox plugin to assist with changes made with the openstack installer after.

