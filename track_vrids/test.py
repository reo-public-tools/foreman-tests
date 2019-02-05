#!/usr/bin/env python

import os
import sys
import time
import json
import getpass
import openstack

sys.path.append(os.path.abspath('../lib/'))

import foremanAction


def print_domain_details(curdomaininfo):

    print "\nDomain: {}({})".format(curdomaininfo['name'],
                                    curdomaininfo['fullname'])
    for organization in curdomaininfo['organizations']:
        print "\tOrg: {} => {}".format(organization['name'],
                                       organization['title'])
    for location in curdomaininfo['locations']:
        print "\tLocation: {} => {}".format(location['name'],
                                            location['title'])
    print "\tParameters:"
    for parameter in curdomaininfo['parameters']:
        print "\t\tname: {} value: {}".format(parameter['name'],
                                              parameter['value'])


def main():

    # Connect and prep foreman api
    foreman_api = "https://lab-deploy01.localdomain/api"
    neutron_network_name = 'ironic'
    username = 'labadmin'
    password = getpass.getpass()

    # Set up the session to the foreman api
    print "Authenticating and setting some env info"
    fa = foremanAction.foremanAction(foreman_api, username, password)
    fa.set_domain_name('phobos.rpc.rackspace.com')
    fa.set_organization('Lab Organization')
    fa.set_location('Lab Location')


    # Get and print the params
    print "Domain Info Before Changes"
    dominfo = fa.get_domain_details('lab1.phobos.rpc.rackspace.com')
    print_domain_details(dominfo)
 

    # Request external and internal haproxy/keepalived router id
    external_vrid = fa.find_new_virtual_router_id('external')
    print "Found free external virtual router id: {}".format(external_vrid)

    internal_vrid = fa.find_new_virtual_router_id('internal')
    print "Found free internal virtual router id: {}".format(internal_vrid)

    # Set the parameter on the domain
    print "Setting external_vrid on lab1 to {}".format(external_vrid)
    fa.set_external_virtual_router_id('lab1.phobos.rpc.rackspace.com', external_vrid)

    print "Setting internal_vrid on lab1 to {}".format(internal_vrid)
    fa.set_internal_virtual_router_id('lab1.phobos.rpc.rackspace.com', internal_vrid)

    print "Info After Changes"
    dominfo = fa.get_domain_details('lab1.phobos.rpc.rackspace.com')
    print_domain_details(dominfo)

    # Sleep a little
    sleep_secs = 20
    print "Sleeping {}".format(sleep_secs)
    time.sleep(sleep_secs)

    # clean it up
    print "Deleting external_vrid param for lab1"
    fa.delete_external_virtual_router_id('lab1.phobos.rpc.rackspace.com')
    print "Deleting internal_vrid param for lab1"
    fa.delete_internal_virtual_router_id('lab1.phobos.rpc.rackspace.com')

    print "Info After Delete"
    dominfo = fa.get_domain_details('lab1.phobos.rpc.rackspace.com')
    print_domain_details(dominfo)





if __name__ == '__main__':
    main()
