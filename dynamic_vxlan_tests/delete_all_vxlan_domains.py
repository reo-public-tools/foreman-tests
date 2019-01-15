#!/usr/bin/env python

import os
import sys
import getpass

sys.path.append(os.path.abspath('../lib/'))

import foremanAction


def main():

    foreman_api = "https://lab-deploy01.localdomain/api"
    username = 'labadmin'
    password = getpass.getpass()

    # Set up the session to the foreman api
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
            if (parameter['name'] == 'type'
                    and parameter['value'] == 'vxlan'):
                print "Deleting {}".format(domain['name'])
                fa.delete_dynamic_lab(domain['name'])

if __name__ == '__main__':
    main()
