#!/usr/bin/env python

import os
import sys
import getpass

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
    print "\tSubnets:"
    for subnet in curdomaininfo['subnets']:
        print "\t\tnetwork: {:20} name: {:20} desc: {:20}".format(
            subnet['network_address'],
            subnet['name'],
            subnet['description'])

def main():

    foreman_api = "https://lab-deploy01.localdomain/api"
    username = 'labadmin'
    password = getpass.getpass()

    # Set up the session to the foreman api
    fa = foremanAction.foremanAction(foreman_api, username, password)
    fa.set_domain_name('phobos.rpc.rackspace.com')
    fa.set_organization('Lab Organization')
    fa.set_location('Lab Location')

    dominfo = fa.create_dynamic_lab()

    print_domain_details(dominfo)

if __name__ == '__main__':
    main()
