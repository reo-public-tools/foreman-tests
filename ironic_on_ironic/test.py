#!/usr/bin/env python

import os
import sys
import time
import json
import getpass
import openstack

sys.path.append(os.path.abspath('../lib/'))

import ironicOnIronic
import foremanAction


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


    # Instantiate the ironicOnIronic class object
    ioi = ironicOnIronic.ironicOnIronic()


    # Set up the request array based on user values given
    request_array = [
        {
            'flavor': 'ironic-standard',
            'count': 1
        },
        {
             'flavor': 'ironic-storage-perf',
             'count':1 
        }]

    # Check the capacity before continuing.
    if ioi.check_capacity(request_array):
        print "Capacity is good, we can check out the nodes now"
    else:
        print "Not enough capacity. Stopping the process."
        sys.exit(1)

    # Check out the nodes
    retinfo = ioi.check_out_nodes('lab1.phobos.rpc.rackspace.com', request_array)
    json_paramval = json.dumps(retinfo)

    # Set the parameter on the domain
    fa.set_ironic_on_ironic_data('lab1.phobos.rpc.rackspace.com', json_paramval)

    # Sleep a little
    sleep_secs = 20
    print "Sleeping {}".format(sleep_secs)
    time.sleep(sleep_secs)

    # Get the parameter on the domain
    retdata = fa.get_ironic_on_ironic_data('lab1.phobos.rpc.rackspace.com')
    retinfo = json.loads(retdata)

    # Release nodes
    for group in retinfo:
        for node in group['node_list']:
            ioi.release_node(node['id'])

    fa.delete_ironic_on_ironic_data('lab1.phobos.rpc.rackspace.com')




if __name__ == '__main__':
    main()
