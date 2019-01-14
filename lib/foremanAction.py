import sys
import json
import random
import requests


class foremanAction:
    """
    Collection of forman api actions that we are using to deploy lab
    environments.
    """

    """
    Class vars:
      - Set up a session so creds are only sent once
      - Define a default endpoint for api calls.
      - Define some default headers for the requests call
      - Set up a prefix to use for lab names. Dynamically
        generated domains will use this to find the slot
        available.
      - Set a domain to use during domain creatino.
      - Set the default organization to add objects to
      - Track the organization id pulled on name set for api calls
      - Set the default location to add objects to
      - Track the location id pulled on name set for api calls
      - Set up a multicast base ip(last octet uses for dynamic domains)
      - Set up the vxlan generation(netmask and step for 3rd octet must match)
    """
    session = requests.Session()
    endpoint = 'https://localhost/api'
    headers = {
        'Accept': 'version=2,application/json',
        'Content-Type': 'application/json'
    }

    domain_name_prefix = 'lab'
    domain_name = 'example.com'

    max_labs = 50

    organization = 'Default Organization'
    organization_id = 1
    location = 'Default Location'
    location_id = 2

    multicast_group_base = '239.1.33'
    vxlan_network_prefix = '172.22'
    vxlan_netmask = '255.255.252.0'
    vxlan_third_octet_step = 4

    def __init__(self, endpoint_url=None, curuser=None, curpass=None,
                 domain_name=None, domain_name_prefix=None,
                 organization=None, location=None):
        """ Allow setting of the endpoint url and creds on __init_ """

        if endpoint_url:
            self.set_endpoint(endpoint_url)
        if curuser and curpass:
            self.auth(curuser, curpass)
        if domain_name_prefix:
            self.set_domain_name_prefix(organization)
        if domain_name:
            self.set_domain_name(organization)
        if organization:
            self.set_organization(organization)
        if location:
            self.set_location(location)

    def do_request(self, debug_id, prepped_req):
        """
        Wrapper for actual api request.
        (TODO)We need to implement paging on large(>20) responses
         here at some point.
        """
        try:
            r = self.session.send(prepped_req)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            print "{}: request encountered an http error: {}".format(debug_id,
                                                                     str(e))
            sys.exit(1)
        except requests.exceptions.Timeout:
            print "{} request timed out.".format(debug_id)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print "{}: request encounterd an error: {}".format(debug_id,
                                                               str(e))
            sys.exit(1)

    def set_endpoint(self, endpoint_url):
        """ Allow setting of foreman api endpoint after instantiation """
        self.endpoint = endpoint_url

    def set_domain_name_prefix(self, prefix):
        """ Allow changing of prefix used for dynamic lab creation. """
        self.domain_name_prefix = prefix

    def set_domain_name(self, domain):
        """ Allow setting of domain used for dynamic lab creation. """
        self.domain_name = domain

    def set_organization(self, organization):
        """ Allow setting of organization used for dynamic lab creation. """
        self.organization = organization

        newreq = requests.Request('GET',
                                  "{}/organizations/{}".format(
                                      self.endpoint,
                                      organization),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.set_organization', prepped_req)
        self.organization_id = r.json()['id']

    def set_location(self, location):
        """ Allow setting of location used for dynamic lab creation. """
        self.location = location

        newreq = requests.Request('GET',
                                  "{}/locations/{}".format(
                                      self.endpoint,
                                      location),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.set_location', prepped_req)
        self.location_id = r.json()['id']

    def auth(self, curuser, curpass):
        """
        Only pass the user & pass once. Use sessions after instantiation
        """

        # Prep the auth request
        newreq = requests.Request('GET',
                                  "{}{}".format(self.endpoint,
                                                '/v2/status'),
                                  headers=self.headers,
                                  auth=(curuser, curpass))
        prepped_req = newreq.prepare()

        # Make the request and set the cookie header for future requests
        r = self.do_request('foremanAction.auth', prepped_req)
        self.headers['Cookie'] = r.headers['set-cookie']

    def get_domains(self):
        """ Get a listing of domains this session has access to """

        newreq = requests.Request('GET',
                                  "{}{}".format(self.endpoint, '/domains'),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domains', prepped_req)
        return r.json()['results']

    def get_domain_details(self, domain_id):
        """ Get the details of a single domain """

        newreq = requests.Request('GET',
                                  "{}/domains/{}".format(self.endpoint,
                                                         domain_id),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domain_details', prepped_req)
        return r.json()

    def get_detailed_domain_list(self):
        """ Get a full list of domains with details attached """

        ret_domains = []
        newreq = requests.Request('GET',
                                  "{}{}".format(self.endpoint, '/domains'),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domains', prepped_req)
        domains = r.json()['results']

        for domain in domains:
            curdomaininfo = self.get_domain_details(domain['id'])
            ret_domains.append(curdomaininfo)

        return ret_domains

    def check_out_domain(self, domain_id):
        """ Check out a domain for use by setting the in-use param to 'yes' """

        data = '{"value": "yes"}'

        newreq = requests.Request('PUT',
                                  "{}/domains/{}/parameters/in-use".format(
                                      self.endpoint,
                                      domain_id),
                                  data=data,
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domains', prepped_req)
        return r.json()

    def release_domain(self, domain_id):
        """ Release used domain by setting the in-use param to 'no'. """

        data = '{"value": "no"}'

        newreq = requests.Request('PUT',
                                  "{}/domains/{}/parameters/in-use".format(
                                      self.endpoint,
                                      domain_id),
                                  data=data,
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domains', prepped_req)

    def find_available_lab_slot(self):
        """ Find a free domain slot for a dynamic(vxlan) based lab """

        domains = self.get_domains()
        x = 1
        while(x < self.max_labs):
            found_match = 0
            for domain in domains:
                domain_match = "{}{}.{}".format(self.domain_name_prefix,
                                                x, self.domain_name)
                if domain_match == domain['name']:
                    found_match = 1
                    break
            if found_match == 0:
                retdomaininfo = {
                    'domain_name': "{}{}.{}".format(self.domain_name_prefix,
                                                    x, self.domain_name),
                    'index': x
                }
                return retdomaininfo
            else:
                x += 1

    def find_new_multicast_group(self):
        """
        Make sure we have a unique multicast group. We will randomize the last
        octet for now and check existing domain entries.
        """

        domain_list = self.get_detailed_domain_list()

        free_for_use = 0
        while free_for_use != 1:
            randip = random.randint(1, 254)
            mcgroup = "{}.{}".format(self.multicast_group_base, randip)
            free_for_use = 1
            for domain in domain_list:
                if domain['parameters'] == []:
                    continue
                for parameter in domain['parameters']:
                    if (parameter['name'] == 'type'
                            and parameter['value'] != 'vxlan'):
                        continue
                    if parameter['name'] == 'multicast-group':
                        if parameter['value'] == mcgroup:
                            free_for_use = 0

        return mcgroup

    def create_dynamic_lab_domain(self):
        """ Create a new vxlan backed dynamic lab """

        slotinfo = self.find_available_lab_slot()
        description = "{}{} Dynamic Domain".format(
            self.domain_name_prefix.upper(),
            slotinfo['index'])

        """ Request an unused multicast group """
        multicast_group = self.find_new_multicast_group()

        """ Make requests to create the new dynamic vxlan domain """
        data = {
            'organization_id': self.organization_id,
            'location_id': self.location_id,
            'domain': {
                'name': slotinfo['domain_name'],
                'fullname': description,
                'domain_parameters_attributes': [
                    {'name': 'type', 'value': 'vxlan'},
                    {'name': 'in-use', 'value': 'yes'},
                    {'name': 'multicast-group', 'value': multicast_group},
                ],
            }
        }
        newreq = requests.Request('POST',
                                  "{}/domains".format(self.endpoint),
                                  data=json.dumps(data),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.create_dynamic_lab_domain',
                            prepped_req)

        return r.json()

    def delete_dynamic_lab_domain(self, domain_name):
        """ Delete a dynamic lab domain """

        newreq = requests.Request('DELETE',
                                  "{}/domains/{}".format(self.endpoint,
                                                         domain_name),
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.delete_dynamic_lab_domain',
                            prepped_req)

        return r.json()
