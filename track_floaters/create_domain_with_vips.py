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


def get_neutron_port(network_name, domain_name):

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

    # Get Neutron Networks
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
        if port['name'] == '{}_external_floating_ip'.format(domain_name):
            port_found = 1
            break

    # Create a port if not found
    if port_found == 0:
        print "Requesting new port for tenant_id {} and network {}".format(
            project_id, ironic_network_id)
        portdescription = "{} external_floating_ip".format(domain_name)
        portname = "{}_external_floating_ip".format(domain_name)

        portinfo = conn.network.create_port(project_id=project_id,
                                            description=portdescription,
                                            name=portname,
                                            network_id=ironic_network_id)
    else:
        print "Using existing port for tenant_id {} and network {}".format(
            project_id, ironic_network_id)
        portinfo = port

    return portinfo


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

    print "Creating a dynamic lab env"
    dominfo = fa.create_dynamic_lab()

    print "Requesting neutron port"
    portinfo = get_neutron_port(neutron_network_name, dominfo['name'])
    external_floating_ip = portinfo['fixed_ips'][0]['ip_address']

    print "New Port IP: {}".format(external_floating_ip)

    print "Setting external_floating_ip parameter for domain {}".format(
        dominfo['name'])
    fa.set_external_floating_ip(dominfo['id'], external_floating_ip)

    print "Pulling domain info and printing results"
    dominfo = fa.get_domain_details(dominfo['id'])
    print_domain_details(fa, dominfo)


if __name__ == '__main__':
    main()
