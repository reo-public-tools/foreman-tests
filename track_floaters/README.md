# Overview

We will need two floating ip addresses. One on the ironic network for the external
vip. Its the same network that we used to provision the hosts. This one will need 
pulled using heat or openstack api calls. The other being from the management
network created in foreman.  This will be used for the internal API.

## Internal VIP

We will start with the internal vip from foreman. This will be pulled from the 
LAB(X)-MGMT network created in the earlier steps. We will probably want to store
these somewhere globally as it will be used when configuring the openstack layers
later on. The internal_floating_ip was used as a domain parameter on the static
network we set up earlier for vlan based network layouts.  For the dynamic vxlan
based environments we will need to generate as we create the domain and subnets.
We are just taking from earlier scripts and adding it on.

For these tests, I updated the library to allocate the floater during dynamic
domain creation with vxlans. The tests in this section are using the same scripts
from the vxlan domain creation.  I have cut off the output dump to show the new
internal_Floating_ip in the domain parameters.

Test management floater allocation
```bash
[root@lab-deploy01 track_floaters]# ./create_vxlan_domain.py | head -n 10
Password: 
{u'description': None, u'network_address': u'172.22.0.0/22', u'id': 291, u'name': u'LAB2-MGMT'}

Domain: lab2.phobos.rpc.rackspace.com(LAB2 Dynamic Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: internal_floating_ip value: 172.22.0.10
		name: in-use value: yes
		name: multicast_group value: 239.1.33.60
		name: type value: vxlan

[root@lab-deploy01 track_floaters]# ./delete_all_vxlan_domains.py 
Password: 
Deleting lab2.phobos.rpc.rackspace.com

```

### External VIP

Set up a virtualenv with the pythonclient if not already.
```bash
virtualenv /root/foreman-tests-venv
. /root/foreman-tests-venv/bin/activate
pip install openstackclient

```

Set up the openstack config
```bash
mkdir -p /root/.config/openstack/
cat <<EOF > /root/.config/openstack/clouds.yaml
clouds:
  default:
    auth:
      auth_url: http://172.20.4.10:5000/v3
      project_name: labs-project
      tenant_name: labs-project
      username: labs-admin
      password: <removed>
      user_domain_name: labs-domain
      project_domain_name: labs-domain
    region_name: RegionOne
    interface: internal
    identity_api_version: "3"
EOF

# test it out
openstack --os-cloud default --insecure token issue
```

Script Tests
```
(foreman-tests-venv) # ./create_domain_with_external_vip.py 
Password: 
Authenticating and setting some env info
Creating a dynamic lab env
Requesting neutron port
Using project id (removed) from auth session
Using matching neutron net id (removed)
Requesting new port for tenant_id (removed) and network (removed)
New Port IP: 172.20.41.108
Setting external_floating_ip parameter for domain lab2.phobos.rpc.rackspace.com
Pulling domain info and printing results

Domain: lab2.phobos.rpc.rackspace.com(LAB2 Dynamic Domain)
	Org: Lab Organization => Lab Organization
	Location: Lab Location => Lab Location
	Parameters:
		name: external_floating_ip value: 172.20.41.108
		name: internal_floating_ip value: 172.22.0.10
		name: in-use value: yes
		name: multicast_group value: 239.1.33.245
		name: type value: vxlan



(foreman-tests-venv) ]# ./delete_all_domains_and_vips.py 
Password: 
Authenticating and setting some env info
Deleting neutron port for ip 172.20.41.108
Using project id (removed) from auth session
Using matching neutron net id 1cc6207d-a1f5-4dfe-b97d-a8c967eb8548
Deleting  port for tenant_id (removed), network (removed) and ip 172.20.41.108
Deleting lab2.phobos.rpc.rackspace.com

```

