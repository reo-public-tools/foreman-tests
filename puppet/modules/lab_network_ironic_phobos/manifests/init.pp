# Class: lab_network_ironic_phobos
# ===========================
#
# Full description of class lab_network_ironic_phobos here.
#
# Parameters
# ----------
#
# Document parameters here.
#
# * `sample parameter`
# Explanation of what this parameter affects and what it defaults to.
# e.g. "Specify one or more upstream ntp servers as an array."
#
# Variables
# ----------
#
# Here you should define a list of variables that this module would require.
#
# * `sample variable`
#  Explanation of how this variable affects the function of this class and if
#  it has a default. e.g. "The parameter enc_ntp_servers must be set by the
#  External Node Classifier as a comma separated list of hostnames." (Note,
#  global variables should be avoided in favor of class parameters as
#  of Puppet 2.6.)
#
# Examples
# --------
#
# @example
#    class { 'lab_network_ironic_phobos':
#      servers => [ 'pool.ntp.org', 'ntp.local.company.com' ],
#    }
#
# Authors
# -------
#
# Author Name <author@domain.com>
#
# Copyright
# ---------
#
# Copyright 2019 Your name here, unless otherwise noted.
#
class lab_network_ironic_phobos {

  # Being interface loop
  $foreman_interfaces.each | $interface | {

    # Find and create physical network configs to attach to a bond
    if $interface['type'] == 'Interface' and $interface['mac'] {
      file { "/etc/systemd/network/${interface['identifier']}.network":
        ensure => file,
        content => epp('lab_network_ironic_phobos/physical_interface.epp', {'interface' => $interface['identifier'], 'bond' => 'bond0' }),
        notify => Service['systemd-networkd'],
      }
    }

    # Set up the bond interface from primary interface info
    if $interface['primary'] == true {

      file { "/etc/systemd/network/bond0.netdev":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bond-netdev.epp', {'bond' => 'bond0'}),
        notify => Service['systemd-networkd'],
      }

      file { "/etc/systemd/network/bond0.network":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bond-network.epp', {'bond' => 'bond0'}),
        notify => Service['systemd-networkd'],
      }

      file { "/etc/systemd/network/br-vlan.netdev":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bridge-netdev.epp', {'bridge' => 'br-vlan'}),
        notify => Service['systemd-networkd'],
      }

      # After the first run, the primary ip info will be setting on br-vlan
      if ('br-vlan' in $networking['interfaces']) and ($networking['interfaces']['br-vlan']['ip']) {
          $primary_ip = $networking['interfaces']['br-vlan']['ip']
          $primary_network = $networking['interfaces']['br-vlan']['network']
          $primary_netmask = $networking['interfaces']['br-vlan']['netmask']
      } else {
          $primary_ip = $networking['interfaces']['bond0']['ip']
          $primary_network = $networking['interfaces']['bond0']['network']
          $primary_netmask = $networking['interfaces']['bond0']['netmask']
      }

      file { "/etc/systemd/network/br-vlan.network":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bridge-network.epp', {
                          'bridge' => 'br-vlan', 
                          'address' => $primary_ip, 
                          'network' => $primary_network, 
                          'cidr' => lab_network_ironic_phobos::netmask_to_cidr($primary_netmask),
                          'gw' => lab_network_ironic_phobos::find_gateway("${primary_network}/${primary_netmask}")
                      }),
        notify => Service['systemd-networkd'],
      } # End br-vlan.network config


      # Update main interfaces file to remove bond0 and slaves
      file { "/etc/network/interfaces":
        source => 'puppet:///modules/lab_network_ironic_phobos/etc_network_interfaces',
        ensure => file,
        owner  => 'root',
        group  => 'root',
        notify => Service['systemd-networkd'],
      }
  
    } # End primary interface conditional


    # Start br-mgmt and tagged interface config
    if 'name' in $interface['subnet'] and 'MGMT' in $interface['subnet']['name'] {

      file { "/etc/systemd/network/br-mgmt.netdev":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bridge-netdev.epp', {'bridge' => 'br-mgmt'}),
        notify => Service['systemd-networkd'],
      }

      file { "/etc/systemd/network/br-mgmt.network":
        ensure => file,
        content => epp('lab_network_ironic_phobos/bridge-network.epp', {
                          'bridge' => 'br-mgmt', 
                          'address' => $interface['ip'], 
                          'network' => $interface['subnet']['network'], 
                          'cidr' => lab_network_ironic_phobos::netmask_to_cidr($interface['subnet']['mask']),
                      }),
        notify => Service['systemd-networkd'],
      } # End br-mgmt.network config

      # br-mgmt should have either a vlanid on the interface or vxlanid on the 
      # subnet.
      if $type == 'vxlan' {
        $cursubnet = $interface['subnet']['name']
        $matchingsubnet = $foreman_subnets.filter | $hash | { $hash['name'] == $cursubnet }
        $tagid = $matchingsubnet[0]['parameters']['vxlan-id']
        $curdevname = "bond0.vxlan${tagid}"
      } else {
        $tagid = $interface['vlanid']
        $curdevname = "bond0.vlan${tagid}"
      }

      file { "/etc/systemd/network/${curdevname}.netdev":
        ensure => file,
        content => epp('lab_network_ironic_phobos/tagged-netdev.epp', {'type' => $type,
                                                                       'tagid' => $tagid,
                                                                       'mcgroup' => $multicast_group,
                                                                       'devname' => $curdevname
                                                                      }),
#        notify => Service['systemd-networkd'],
      }



    } # End br-mgmt config


  } # End interface loop


  # Service handler
  service { 'systemd-networkd':
    ensure => running,
    enable => true,
  }

} # End class lab_network_ironic_phobos
