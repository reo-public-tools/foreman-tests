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

    # Get a full domain listing
    domains = fa.get_domains()

    # Get the domain info and check for type vlan
    for domain in domains:

        # Inore the default domain
        if domain['name'] == 'localdomain':
            continue

        print "Found domain: id: {} name: {} fullname: {}".format(
            domain['id'],
            domain['name'],
            domain['fullname'])

        # Make an api call to get the domain details
        curdomaininfo = fa.get_domain_details(domain['id'])

        # init a couple of check vars
        is_free_for_use = 0
        is_type_vlan = 0

        # go through the parameters to see if this is a vlan
        # domain that is not in use
        for parameter in curdomaininfo['parameters']:
            if parameter['name'] == 'in-use' and parameter['value'] == 'no':
                print "Domain {} is free to use".format(domain['name'])
                is_free_for_use = 1
            if parameter['name'] == 'type' and parameter['value'] == 'vlan':
                print "Domain {} is of type vlan".format(domain['name'])
                is_type_vlan = 1

        # Check the results
        if is_free_for_use == 1 and is_type_vlan == 1:
            # We have a winner, lets check it out
            print "Domain {} is free to check out".format(domain['name'])

            # Check out the domain and print the domain info
            fa.check_out_domain(domain['id'])

            # get the updated domain details
            curdomaininfo = fa.get_domain_details(domain['id'])

            # print out the details for the domain just checked out
            print_domain_details(curdomaininfo)

            break
        else:
            print "Domain {} is either the wrong type or in use".format(
                domain['name'])
            continue

if __name__ == '__main__':
    main()
