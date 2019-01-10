# Openstack in Opestack lab component testing

This is mainly for helping openstack developers build environments within an existing openstack
environment using ironic. This repo is temporary for testing some basic functionality. 


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


We are going to test out just he rpc-o and rpc-r on ironic nodes along with ironic-on-ironic to begin with. This layout should 
make it really easy to start expanding into mixed environmets to include VMs and scalable simulated(mnaio) style setups in the 
future though.



## Foreman Installation Steps(single node AIO)

[Setting up a Foreman AIO with the Katello Plugin](./install_foreman/README.md)


## Creating a new Lab Environment

To start out with, I'm just setting up the environment to use for testing. This will
involve setting up a lab org, location and user.  We will have an option of using vlans
already trunked down to the ironic nodes for things requiring network performance, or 
to use vxlans with auto-generated network info. 

[Creating a new Environment](./setup_lab_environment/README.md)


## Test some python code out using the api to "check out" vlan networks

We will need the ability to check out pre defined vlan network groups for labs. These will
be presented as subnet objects under a domain object set up for each vlan group. In this test
We have two parameters tied to the domain.

* type(vlan or vxlan): Track if its a static vlan or dynamic vxlan network layout.
* in-use(yes or no): Just a simple var to track if the domain is in use or not.

[Working with static VLAN groups](./static_vlan_tests/README.md)<br>
[check_out_vlan_domain.py](./static_vlan_tests/check_out_vlan_domain.py)<br>
[release_vlan_domain.py](./static_vlan_tests/release_vlan_domain.py)<br>



## Generate and save vxlan domains and subnets(TODO).

We have a limited amount of vlans trunked down to the environment. Vxlans allow us to 
set up the same layout without requiring netsec or dcops intervention. Since the domain
object doesn't exist, we will need to create it along with generating the associated 
subnets.  We can store vxlan info within the subnets for each. The multicast group info
can be stored with the domain at a higher level. 

[Working with dynamic vxlan groups](./dynamic_vxlan_tests/README.md)


## Allocate floating ip addresses for external and internal(TODO):

Whatever code handles the overall lab setup, it will need to pull an ip from the management
network and allocate a port or floating ip from the base 'ironic' network. We will need
to track these somewhere global to the environment.  Domain attributes will probably be
the best place.

[Tracking external and internal lb floaters](./track_floaters/README.md)


## Look into ironic-on-ironic checkout(TODO)

ironic-on-ironic will allow us to use our existing baremetal to allocate OSP overcloud
nodes, or openstack-ansible ironic nodes for testing on the existing ironic infrastructure.

May need to look into setting up host objects to account for each checked out ironic node with
useful info for each.  When subnets are assigned to hosts, foreman will pull a free ip from
the subnet for each if needed.  This can be used to auto-generate the OSP network templates
with pre-defined ip addresses for the overcloud later on.  It can also be used for the 
ironic node registration steps as well for both OSP and openstack-ansible style setups.

[Checking out ironic nodes for ironic-on-ironic](./ironic_on_ironic/README.md)


## Look into method to build out hosts including networking and disk(TODO)

We can either test out using foreman's compute plugin to start building out the environment, or
run it externally.  Here we can look at making sure the host objects get created under a domain.
From there we can use either ansible or puppet to use all of the data in foreman to configure
networking and disks to prepare for openstack installs. This might involve setting up the ansible
plugin and using the public ansible dynamic inventory script for foreman. 

[Build and Configure the ENV](./build_and_configure/README.md)


## Look into openstack auto-configuration using foreman data(TODO)

We already have some config-automation scripts tested in other envs.  Foreman should have all the
info we need at this point to auto-configure the environment.  

[Auto-Configure Openstack Deploy](./auto_configure/README.md)


## Stopping point

We are stopping here as we should have an env ready for either an OSP or openstack-ansible deploy.
They each have their own way of deployment.  The steps here will probably be external to foreman.



