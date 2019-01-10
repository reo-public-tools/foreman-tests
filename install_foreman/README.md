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

