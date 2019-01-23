#!/usr/bin/env python

import os
import sys
import getpass
import openstack

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


def delete_neutron_port(network_name, domain_name, ip):

    # Init and enable debugging
    openstack.enable_logging(debug=False)

    # Connect
    conn = openstack.connect(cloud='default')

    """
    Get the project_id from the authed session.
    We are using this as to map the name to project
    you need list_projects permissions which are
    locked down for project admins.
    """
    project_id = conn.config.get_session().get_project_id()
    print "Using project id {} from auth session".format(project_id)

    # Get Neutron Network
    networks = conn.network.networks(name=network_name)
    for network in networks:
        if network_name == network['name']:
            ironic_network_id = network['id']
            print "Using matching neutron net id {}".format(ironic_network_id)
            break

    # List ports for this project
    port_found = 0
    ports = conn.network.ports(tenant_id=project_id)
    for port in ports:
        if (port['name'] == '{}_external_floating_ip'.format(domain_name) and
                port['fixed_ips'][0]['ip_address'] == ip):
            port_found = 1
            break

    # Create a port if not found
    if port_found == 1:
        print "Deleting  port for tenant_id {}, network {} and ip {}".format(
            project_id, ironic_network_id, ip)

        portinfo = conn.network.delete_port(port)
    else:
        print "No matchint port for tenant_id {}, network {} and ip {}".format(
            project_id, ironic_network_id, ip)


def main():

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

    # Lets parse through all the vxlan based
    # domains and do some testing cleanup
    domains = fa.get_detailed_domain_list()
    for domain in domains:

        if domain['parameters'] == []:
            continue
        for parameter in domain['parameters']:
            if parameter['name'] == 'external_floating_ip':
                print "Deleting neutron port for ip {}".format(
                    parameter['value'])
                delete_neutron_port(neutron_network_name,
                                    domain['name'],
                                    parameter['value'])
            if (parameter['name'] == 'type'
                    and parameter['value'] == 'vxlan'):
                print "Deleting {}".format(domain['name'])
                fa.delete_dynamic_lab(domain['name'])


if __name__ == '__main__':
    main()
