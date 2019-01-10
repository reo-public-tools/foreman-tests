#!/usr/bin/env python

import sys
import getpass
import requests


def get_domains(cururl, curuser, curpass):
  
  # Get a collection of domains(will need to work with pages later if results > 20)
  headers = {'Accept': 'version=2,application/json'}
  try:
    r = requests.get(cururl + '/domains', auth=(curuser, curpass), headers=headers)
    r.raise_for_status()

    domains = r.json()['results']
    return domains
  except requests.exceptions.HTTPError as e:
    print "get_domains request encountered an http error:"
    print e
    sys.exit(1)
  except requests.exceptions.Timeout:
    print "get_domains request timed out"
    sys.exit(1)
  except requests.exceptions.RequestException as e:
    print "get_domains request encounterd an error:"
    print e
    sys.exit(1)



def get_domain_details(cururl, curuser, curpass, domain_id):
  
  # Get a collection of domains(will need to work with pages later if results > 20)
  headers = {'Accept': 'version=2,application/json'}
  try:
    r = requests.get(cururl + '/domains/%s' % domain_id, auth=(curuser, curpass), headers=headers)
    r.raise_for_status()
    return r.json() 
  except requests.exceptions.HTTPError as e:
    print "get_domain_details request encountered an http error:"
    print e
    sys.exit(1)
  except requests.exceptions.Timeout:
    print "get_domain_details request timed out"
    sys.exit(1)
  except requests.exceptions.RequestException as e:
    print "get_domain_details request encounterd an error:"
    print e
    sys.exit(1)

def release_domain(cururl, curuser, curpass, domain_id):
  # Get a collection of domains(will need to work with pages later if results > 20)
  headers = {'Accept': 'version=2,application/json', 'Content-Type': 'application/json'}
  data = '{"value": "no"}'
  try:
    r = requests.put(cururl + '/domains/%s/parameters/in-use' % domain_id, auth=(curuser, curpass), headers=headers, data=data)
    r.raise_for_status()
    return r.json() 
  except requests.exceptions.HTTPError as e:
    print "check_out_domain request encountered an http error:"
    print e
    sys.exit(1)
  except requests.exceptions.Timeout:
    print "check_out_domain request timed out"
    sys.exit(1)
  except requests.exceptions.RequestException as e:
    print "check_out_domain request encounterd an error:"
    print e
    sys.exit(1)

def print_domain_details(curdomaininfo):

  print "\nDomain: %s(%s)" % (curdomaininfo['name'], curdomaininfo['fullname'])
  for organization in curdomaininfo['organizations']:
    print "\tOrg: %s => %s" % (organization['name'], organization['title'])
  for location in curdomaininfo['locations']:
    print "\tLocation: %s => %s" % (location['name'], location['title'])
  print "\tParameters:"
  for parameter in curdomaininfo['parameters']:
    print "\t\tname: %s value: %s" % (parameter['name'], parameter['value'])
  print "\tSubnets:"
  for subnet in curdomaininfo['subnets']:
    print "\t\tnetwork: %-20s name: %-20s desc: %s" % (subnet['network_address'], subnet['name'], subnet['description'])


def main():

  foreman_api = "https://lab-deploy01.localdomain/api"
  username = 'labadmin'
  password = getpass.getpass()
  domain_name_to_release = 'lab1.phobos.rpc.rackspace.com'

  domain_list = get_domains(foreman_api, username, password)

  # Get the domain info and check for type vlan
  for domain in domain_list:

    # Inore the default domain
    if domain['name'] != domain_name_to_release:
      continue

    print "Found domain: id: %s name: %s fullname: %s" % (domain['id'], domain['name'], domain['fullname'])

    # Make an api call to get the domain details
    curdomaininfo = get_domain_details(foreman_api, username, password, domain['id'])

    # init a couple of check vars
    is_free_for_use = 0
    is_type_vlan = 0

    # go through the parameters to see if this is a vlan domain that is not in use
    for parameter in curdomaininfo['parameters']:
      if parameter['name'] == 'in-use' and parameter['value'] == 'no':
        print "Domain %s is free to use" % domain['name']
        is_free_for_use = 1
      if parameter['name'] == 'type' and parameter['value'] == 'vlan':
        print "Domain %s is of type vlan" % domain['name']
        is_type_vlan = 1

    # Check the results
    if is_free_for_use == 0 and is_type_vlan == 1:
      # We have a winner, lets release it
      print "Domain %s is in use and can be released" % domain['name']

      # Check out the domain and print the domain info
      release_domain(foreman_api, username, password, domain['id'])
     
      # get the updated domain details
      curdomaininfo = get_domain_details(foreman_api, username, password, domain['id'])

      # print out the details for the domain just checked out
      print_domain_details(curdomaininfo)

      break
    else:
      print "Domain %s is already released" % domain['name']
      continue

if __name__ == '__main__':
  main()
