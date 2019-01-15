#!/usr/bin/env python

import os
import sys
import getpass

sys.path.append(os.path.abspath('../lib/'))

import foremanAction


def print_domain_details(faobj, curdomaininfo):

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
        cursubnetinfo = faobj.get_subnet_details(subnet['id'])
        print "\t\tname: {}".format(subnet['name'])
        print "\t\t\tdesc: {}".format(subnet['description'])
        print "\t\t\tnetwork: {}".format(subnet['network_address'])
        print "\t\t\tgateway: {}".format(cursubnetinfo['gateway'])
        print "\t\t\tmask: {}".format(cursubnetinfo['mask'])
        print "\t\t\tcidr: {}".format(cursubnetinfo['cidr'])
        print "\t\t\tfrom: {} to: {}".format(cursubnetinfo['from'],
                                             cursubnetinfo['to'])
        print "\t\t\tboot_mode: {}".format(cursubnetinfo['boot_mode'])
        print "\t\t\tnetwork_type: {}".format(cursubnetinfo['network_type'])
        print "\t\t\tipam: {}".format(cursubnetinfo['ipam'])
        for parameter in cursubnetinfo['parameters']:
            print "\t\t\tparam: name: {} value: {}".format(parameter['name'],
                                                           parameter['value'])


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

    print_domain_details(fa, dominfo)

if __name__ == '__main__':
    main()
