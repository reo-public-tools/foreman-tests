# Installing Foreman



## Envirnment Info

We are setting up a small foreman AIO instance attached directly to a shared flat network for a lab environment.

* Version: The Foreman 1.18 with Katello 3.7(for debian repo support)
* Newtork: On a VM attached to an Ironic flat network to allow vxlan mesh for lab seperation. We have access to all over vpn.
* OS: Centos 7
* Flavor: 8 vcpu, 16 GB vram, 100GB disk


## Installation Steps

Steps from: https://theforeman.org/plugins/katello/3.10/installation/index.html

```bash
yum -y localinstall http://fedorapeople.org/groups/katello/releases/yum/3.10/katello/el7/x86_64/katello-repos-latest.rpm
yum -y localinstall http://yum.theforeman.org/releases/1.20/el7/x86_64/foreman-release.rpm
yum -y localinstall https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
yum -y localinstall http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y install foreman-release-scl python-django

yum -y update
yum -y install katello

foreman-installer --scenario katello --help

echo "$(ip addr show dev eth0 | awk '/inet /{print $2}' | sed -e 's/\/22//g') $(hostname).localdomain $(hostname)" >> /etc/hosts

foreman-installer --scenario katello --enable-foreman-compute-openstack --enable-foreman-compute-libvirt

(Save the credentials somewhere)

# Run puppet so that it sets up the foreman host to be used by the org.
puppet agent --test
```



## Basic configuration for lab


### Set up an org, location and user

Just to go through the process.  I'll create a new org and location to run things in.

```bash
hammer organization create --label "lab_org" --name "Lab Organization"
hammer location create --name "Lab Location"
```

Create a new user for the org
```bash
hammer auth-source list
hammer organization list
hammer location list

hammer user create --ask-password true --auth-source-id 1 --default-location "Lab Location" --default-organization "Lab Organization" --description "Lab Admin"  --login labadmin --mail test@example.com --organization-id 3 --location-id 4 --admin true
Enter user's new password: 
User [labadmin] created.

```


### Set up static domains with vlan info.

```bash
hammer domain create --description "LAB1 Static Domain" --location "Lab Location" --name "lab1.phobos.rpc.rackspace.com" --organization "Lab Organization"
hammer domain set-parameter --domain "lab1.phobos.rpc.rackspace.com" --name "type" --value "vlan"
hammer domain set-parameter --domain "lab1.phobos.rpc.rackspace.com" --name "in-use" --value "no"
hammer domain info --name 'lab1.phobos.rpc.rackspace.com'
Id:            2
Name:          lab1.phobos.rpc.rackspace.com
Description:   LAB1 Static Domain
DNS Id:        
Subnets:       

Locations:     
    Lab Location
Organizations: 
    Lab Organization
Parameters:    
    in-use => no
    type => vlan
Created at:    2019/01/08 21:39:32
Updated at:    2019/01/08 21:39:32

```


### Set up static networks tied to the new domain


```bash
# The from->to is the range that IPAM assigns ips. Lets keep with the lower part of the range to make the openstack config easier.
hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.64.50 --to 172.20.64.255 --gateway 172.20.64.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.64.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-MGMT" --vlanid 289 --description "LAB1 management network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.68.50 --to 172.20.68.255 --gateway 172.20.68.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.68.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-STOR-MGMT" --vlanid 290 --description "LAB1 storage management network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.72.50 --to 172.20.72.255 --gateway 172.20.72.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.72.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-STORAGE" --vlanid 291 --description "LAB1 storage network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.76.50 --to 172.20.76.255 --gateway 172.20.76.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.76.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-TENANT" --vlanid 292 --description "LAB1 tenant network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.80.50 --to 172.20.80.255 --gateway 172.20.80.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.80.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-LBAAS" --vlanid 293 --description "LAB1 lbaas network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.84.50 --to 172.20.84.255 --gateway 172.20.84.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.84.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-INSIDE-NET" --vlanid 294 --description "LAB1 inside net network with static VLANs"

hammer subnet create --boot-mode Static --domains "lab1.phobos.rpc.rackspace.com" --from 172.20.88.50 --to 172.20.88.255 --gateway 172.20.88.1 --ipam "Internal DB" --location "Lab Location" --mask "255.255.252.0" --network "172.20.88.0" --network-type "IPv4" --organization "Lab Organization" --name "LAB1-GW-NET" --vlanid 295 --description "LAB1 gateway net network with static VLANs"

hammer subnet list
---|-----------------|--------------|----------------|---------------|---------|----------
ID | NAME            | NETWORK ADDR | NETWORK PREFIX | NETWORK MASK  | VLAN ID | BOOT MODE
---|-----------------|--------------|----------------|---------------|---------|----------
2  | LAB1-MGMT       | 172.20.64.0  | 22             | 255.255.252.0 | 289     | Static   
3  | LAB1-STOR-MGMT  | 172.20.68.0  | 22             | 255.255.252.0 | 290     | Static   
4  | LAB1-STORAGE    | 172.20.72.0  | 22             | 255.255.252.0 | 291     | Static   
5  | LAB1-TENANT     | 172.20.76.0  | 22             | 255.255.252.0 | 292     | Static   
6  | LAB1-LBAAS      | 172.20.80.0  | 22             | 255.255.252.0 | 293     | Static   
7  | LAB1-INSIDE-NET | 172.20.84.0  | 22             | 255.255.252.0 | 294     | Static   
8  | LAB1-GW-NET     | 172.20.88.0  | 22             | 255.255.252.0 | 295     | Static   
---|-----------------|--------------|----------------|---------------|---------|----------

```

