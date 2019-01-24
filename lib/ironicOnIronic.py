import openstack


class ironicOnIronic:

    conn = None

    def __init__(self):

        # Init and enable debugging
        openstack.enable_logging(debug=False)

        # Connect
        self.conn = openstack.connect(cloud='default')

    def get_nodes_by_system_type(self, system_type):

        ret_nodes = []

        # Get and parse nodes
        for node in self.conn.baremetal.nodes(details=True,
                                              provision_state='available',
                                              associated=False,
                                              is_maintenance=False):

            # Convert to dict
            node_data = node.to_dict()

            # capabilities is a long string and we only need system_type:
            # key:var,key:var,key:var
            capabilities = node_data['properties']['capabilities'] .split(',')
            for cap in capabilities:
                if 'system_type' in cap:
                    cur_system_type = cap.split(':')[1]
                    if (cur_system_type == system_type):
                        ret_nodes.append(node)

        return ret_nodes

    def get_flavor_capability(self, flavor_name, key_name):
        """
        We are using the system_type capability setting
        to map flavors to ironic nodes.
        """

        flavorinfo = self.conn.get_flavor(flavor_name)
        capname = "capabilities:{}".format(key_name)

        return flavorinfo['extra_specs'][capname]

    def check_capacity(self, request_array):
        """
        In order to check the capacity, we will need a list of
        baremetal flavors and a count of how many of each needed.

        ex:

        request_array = [
          {
            "flavor": "ironic-standard",
            "count": 2
          },
             "flavor": "ironic-storage-perf",
             "count": 3
          }
        """
        cap_avail = True
        for curelement in request_array:
            system_type = self.get_flavor_capability(curelement['flavor'],
                                                     'system_type')
            found_nodes = self.get_nodes_by_system_type(system_type)

            if curelement['count'] <= len(found_nodes):
                print ("SUCCESS: We found {} available nodes of flavor {} "
                       "for a request of {}".format(len(found_nodes),
                                                    curelement['flavor'],
                                                    curelement['count']))
            else:
                print ("FAILURE: We found {} available nodes of flavor {} "
                       "for a request of {}".format(len(found_nodes),
                                                    curelement['flavor'],
                                                    curelement['count']))
                cap_avail = False

        return cap_avail

    def get_node_pxe_macs(self, node_id):

        """
        The mac address for dhcp is associated with a neutron port.
        We will need to pull the macs for lab use later on.

        We will send back an array as we could have more than one.
        """
        ports = self.conn.baremetal.ports(node=node_id)
        macs = []
        for port in ports:
            macs.append(port['address'])

        return macs

    def check_out_nodes(self, reason, request_array):
        """
        In order to check the nodes, we will need a list of
        baremetal flavors and a count of how many of each needed.
        The overall capacity should be checked first with
        self.check_capacity.

        The reason will be unique per lab environment(maybe domain
        name).  This will allow us to match, clear and clean later.

        request_array ex:

        request_array = [
          {
            "flavor": "ironic-standard",
            "count": 2
          },
             "flavor": "ironic-storage-perf",
             "count": 3
          }
        """
        ret_list = []

        for curelement in request_array:
            retelement = curelement
            retelement['node_list'] = []
            system_type = self.get_flavor_capability(curelement['flavor'],
                                                     'system_type')
            avail_nodes = self.get_nodes_by_system_type(system_type)
            use_nodes = avail_nodes[0:curelement['count']]
            avail_nodes = ''
            for node in use_nodes:
                print "Checking out node {}".format(node['name'])
                self.conn.set_machine_maintenance_state(node['id'],
                                                        state=True,
                                                        reason=reason)
                macs = self.get_node_pxe_macs(node['id'])
                appendme = {
                    'id': node['id'],
                    'name': node['name'],
                    'cpu_arch': node['properties']['cpu_arch'],
                    'cpus': node['properties']['cpus'],
                    'memory_mb': node['properties']['memory_mb'],
                    'local_gb': node['properties']['local_gb'],
                    'size': node['properties']['size'],
                    'ipmi_username': node['driver_info']['ipmi_username'],
                    'ipmi_address': node['driver_info']['ipmi_address'],
                    'ipmi_password': node['driver_info']['ipmi_password'],
                    'macs': macs
                }

                retelement['node_list'].append(appendme)
            ret_list.append(retelement)

        return ret_list

    def release_node(self, id):
        """
        Instead of just taking the node out of maintenance state, we shoud
        probably put it in manage then provide after to make sure a good
        cleaning is done on the node in production.
        """

        print("Setting node id {} to provision state {}".format(id, 'manage'))
        self.conn.node_set_provision_state(id, 'manage')

        print("Setting node id {} to maint state".format(id))
        self.conn.remove_machine_from_maintenance(id)

        print("Setting node id {} to provision state {}".format(id, 'provide'))
        self.conn.node_set_provision_state(id, 'provide')
