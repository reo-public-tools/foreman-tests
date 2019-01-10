# openstack-provision
Tools to automate and provision devices for various openstack installation tools


## Overview

When working with developers for openstack deployment systems and solutions, they require
a various array of environments ranging from an all in one solution to a full blown environment.
Many times a hybrid would a better solution.  For example if you are testing out compute or storage
hardware, you may need a small simulated control plane to test the hardware out.  Maybe you want a
baremetal simulated control plan with some VMs or ironic nodes spun up to handle testing on PaaS 
solutions that need an IaaS framwork to support it.  

Ironic is great, but requires the IaaS(undercloud) to start with and is very limited in scope.  For
example you can't do ironic-on-ironic without some hackery.  It also doesn't have all of the lifecycle
management components and flexibility that something like cobbler has.  Cobbler is great and is the 
first thing most seasoned linux admins go to when needing to provision large amounts of hardware. The
templating additions and api can make some tasks that a normally a pain really easy to deal with.  The
foreman(with katello) seems to be the new kid on the block.  It has everything cobbler does and a bunch
of additional plugins and functionality.  Thanks to Redhat using it for the newer spacewalk backend, its
constantly being improved. 

Just some of the things that it supports that can be really helpful when deploying an environment prepared
for an openstack install.

* The Foreman Katello Plugin: 
  * Adds a frontend to the pulp repo software.  
  * It supports debian, redhat, ostree, python(pypy), docker and puppet repos.  
  * Allows you to create snapshots of these repos to assist in versioning the repos along with your custom software.
* Provisioning:
  * Pulp smart proxies allow you to spread out repo content in various datacenters or locations.
  * A mix of dhcp, tftp, puppet... proxies can be spread out for differnt environments, clusters and/or customer locations.
  * Can handle all of the templating, metadata, ip management, kickstart/preseed and much more neede when provisioning systems.
  * Can spin up directly to openstack, vmware, gce, ovirt, Rackspace and libvirt as well as the normal baremetal provisiing.
* Post-Provisioning Usage:
  * After provisioning, the foreman db already has all your host data, network info, facts, metadata and other scoped variables
    available.
  * The api or ansible plugins can be used to do auto configuration of your openstack deployment system(osa, osp...) using 
    existing provisioning info. 



## Foreman Installation Steps(single node AIO)

[Setting up a Foreman AIO with the Katello Plugin](./install_foreman/README.md)

## Learning process

I'm not sure how far I can get with this. I will use this area to document the testing to start out with, which will hopefully
evolve into something better as I go. At this point I have played around with the install and tested out the openstack connectivity.
I will break this down into various subtasks and take notes on each as I go.


### Creating a new Lab Environment

To start out with, I'm just setting up the environment to use for testing. This will
involve setting up a lab org, location and user.  We will have an option of using vlans
already trunked down to the ironic nodes for things requiring network performance, or 
to use vxlans with auto-generated network info. 

[Creating a new Environment](./setup_lab_environment/README.md)


### Test some python code out using the api to "check out" vlan networks

We will need the ability to check out pre defined vlan network groups for labs. These will
be presented as subnet objects under a domain object set up for each vlan group. In this test
We have two parameters tied to the domain.

* type(vlan or vxlan): Track if its a static vlan or dynamic vxlan network layout.
* in-use(yes or no): Just a simple var to track if the domain is in use or not.

[Working with static VLAN groups](./static_vlan_tests/README.md)




### Generate and save vxlan domains and subnets(TODO).

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



