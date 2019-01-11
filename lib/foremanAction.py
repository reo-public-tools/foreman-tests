#!/usr/bin/env python

import sys
import requests


class foremanAction:

    session = requests.Session()
    endpoint = 'https://localhost/api'
    headers = {
        'Accept': 'version=2,application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self, endpoint_url='', curuser='', curpass=''):
        if endpoint_url != '':
            self.set_endpoint(endpoint_url)
        if curuser != '' and curpass != '':
            self.auth(curuser, curpass)

    def do_request(self, debug_id, prepped_req):
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
        self.endpoint = endpoint_url

    def auth(self, curuser, curpass):
        """ Only pass the user & pass once. Use sessions after """

        # Prep the auth request
        newreq = requests.Request('GET',
                                  "{}{}".format(self.endpoint, '/v2/status'),
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

    def check_out_domain(self, domain_id):
        """ Check out a domain for use """

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
        """ Release used domain """

        data = '{"value": "no"}'

        newreq = requests.Request('PUT',
                                  "{}/domains/{}/parameters/in-use".format(
                                      self.endpoint,
                                      domain_id),
                                  data=data,
                                  headers=self.headers)
        prepped_req = newreq.prepare()

        r = self.do_request('foremanAction.get_domains', prepped_req)
