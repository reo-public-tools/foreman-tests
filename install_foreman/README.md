# Installing Foreman



## Envirnment Info

We are setting up a small foreman AIO instance attached directly to a shared flat network for a lab environment.

* Version: The Foreman 1.18 with Katello 3.7(for debian repo support)
* Newtork: On a VM attached to an Ironic flat network to allow vxlan mesh for lab seperation. We have access to all over vpn.
* OS: Centos 7
* Flavor: 8 vcpu, 16 GB vram, 100GB disk


## Installation Steps

Steps from: https://theforeman.org/plugins/katello/3.7/installation/index.html

```bash
yum -y localinstall http://fedorapeople.org/groups/katello/releases/yum/3.7/katello/el7/x86_64/katello-repos-latest.rpm
yum -y localinstall http://yum.theforeman.org/releases/1.18/el7/x86_64/foreman-release.rpm
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


Create an ubuntu repo
```bash

hammer product create  --organization-label Default_Organization --description 'Ubuntu 16.04' --name ubuntu_xenial --label ubuntu_xenial

hammer organization list
hammer product list --organization-id 3

wget http://us.archive.ubuntu.com/ubuntu/dists/xenial/Release.gpg
hammer gpg create --key Release.gpg --name 'xenial' --organization-id 3

hammer repository create --organization-id 3 --product-id 2 --name 'Ubuntu 16.04' --content-type deb --url http://us.archive.ubuntu.com/ubuntu --deb-releases xenial --deb-architectures 'amd64' --mirror-on-sync true --publish-via-http true --gpg-key xenial

hammer repository list



tmux
hammer repository synchronize --organization-id 3 --product-id 2 --id 2
Ctrl-B d


```




