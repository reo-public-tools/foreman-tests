# Create a new environment

## Global parameter scope.

To know what we need for the environment, we need to know how the foreman scopes
variables.  Any smaller in scope will override the larger.  A list is provided 
below from the parameters section here: https://www.theforeman.org/manuals/1.18/index.html#4.2.3Parameters

* **Global**: Applies to all hosts.
* **Organization**: Can have muliple orgs per customer or environment.
* **Location**: Could be used to define location based variables(ntp, dns caching...)
* **Domain**: Applied when hosts are associated with a DNS domain.
* **Subnet**: Applied when hosts are associated with a subnet.
* **Operating System**: Applied with hosts are assocated with an OS.
* **Hostgroup Parameters**: Applied to hosts grouped within a hostgroup.
* **Host Parameters**: Applied to a single host.

Be aware that you can use organizations and locations to separate out resources and assign
RBAC permissions for access to those.  This means that you will need to define any repos
again.  If you define the same repo though, the packages in the repos are just linked to
the existing via pulp. This is for a lab environment where we are not worried about permissions
across environments.  For the lab environment, we will just be creating a new domain, subnets and
hostgroup for each lab.  This will allow us to use the 'domain' as our environment global variables
, subnets for subnet specific variables.  We can name everything off of the subdomain for ease of
tracking.



## Basic configuration for lab


### Set up an org, location and user

Just to go through the process.  I'll create a new org and location to run things in.
Make sure to add the default smart proxy or else you will have missing template vars
such as puppermaster and puppet_ca_server.

```bash
hammer organization create --label "lab_org" --name "Lab Organization"
hammer proxy list
hammer location create --name "Lab Location" --smart-proxy-ids 1
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


### Allocate a floating ip from the management work

We are picking .10 from the 0-50 range left for manual use. It can be anything that you
are not expecting to be used by hosts or containers in the future build steps. So I'm 
setting a internal_floating_ip paramter on the domain to hold it. The external will need
to be a floater generated from openstack's ironic network. When ironic nodes are being spun
up they will pull from the same networks, so the floater will be tied to the primary interface
later on with either keepalived(osa) or pacemaker(osp).

```bash
hammer domain set-parameter --domain "lab1.phobos.rpc.rackspace.com" --name "internal_floating_ip" --value "172.20.68.10"
```


## Set up openstack lab project

I attempted to set up a domain admin, but it needs higher privs than that.  We will just create an admin user
and a separate project just for the labs.

```bash


openstack project create --description "Shared LAB Project" --domain labs-domain labs-project

openstack user create --project labs-project --password-prompt --description 'LABS Domain Admin User' --enable labs-admin

openstack role add --project labs-project --user labs-admin admin
openstack role add --domain default --user labs-admin admin

openstack quota set --ram='-1' --instances=100 --cores='-1' --floating-ips=1 --gigabytes='-1' labs-project

neutron security-group-list --tenant_id <project id>

(find the default)

neutron security-group-rule-create --protocol icmp --direction ingress <project default security group id>
neutron security-group-rule-create --protocol tcp --port-range-min 1 --port-range-max 65535 --direction ingress <project default security group id>
neutron security-group-rule-create --protocol udp --port-range-min 1 --port-range-max 65535 --direction ingress <project default security group id>

```
