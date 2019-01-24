# ironic-on-ironic allocation

In order to allow baremetal testing with OSA or overcloud setup with OSP, we
need a way to take existing ironic nodes out of the environment to be used in
the created lab. To do this we can set the nodes into maintenance mode and
provide the users with the ipmi info needed for their ironic node registrations.

By default it looks like the ipmi password is encrypted. After digging around,
it looks like you can add a show_password policy.json entry for the ironic api
servers to allow specific users access.  For now we will stick with the masked
pass and worry about this later on as we don't want to make env changes during
these tests. Once we do get it, we will probably want a way to security save
the info and decrypt after during the deploy.

In this test, we will want a process something like the following:

* Provide an array of baremetal flavors and the count for each.
* Check the total capacity and drop out if the full env can't be built.
* Check out the nodes(put into maintenance mode and update reason with maybe 
  the lab name to match later)
* Return the request along with the allocated node information.
* Store this info scoped to the lab env(Domain for now). (ioi_data Base64 encoded json)

To back out we will probably want something like:

* parse through the lab env data and free up any ironic nodes
  (clear maint  & reason, start cleaning process)
* Delete ioi_data base64 encoded json parameter for given domain



Test Output
```bash
# . /root/foreman-tests-venv/bin/activate

(foreman-tests-venv) # ./test.py 
Password: 
Authenticating and setting some env info
SUCCESS: We found 4 available nodes of flavor ironic-standard for a request of 1
SUCCESS: We found 5 available nodes of flavor ironic-storage-perf for a request of 1
Capacity is good, we can check out the nodes now
Checking out node 605094-ironic10
Checking out node 711488-ironic17
{"parameter": {"name": "ioi_data", "value": "W3sY291bnQiOiAxLCAiZmxhdm9yIjogImlyb25pYy1zdGFuZGFyZCIsICJub2RlX2xpc3QiOiBbeyJtYWNzIjogWyI5YzpkYzo3MTpkNjoxMzpiMCJdLCAiaXBtaV91c2VybmFtZSI6ICJyb290IiwgImNwdXMiOiAzMiwgImlwbWlfcGFzc3dvcmQiOiAiKioqKioqIiwgImxvY2FsX2diIjogNTU3LCAiaWQiOiAiMGY4MGU3MDEtOWViNi00MjcyLTlmNzQtMmRhOWZiYjc1MGQ5IiwgInNpemUiOiA1NTgsICJjcHVfYXJjaCI6ICJ4ODZfNjQiLCAibmFtZSI6ICI2MDUwOTQtaXJvbmljMTAiLCAibWVtb3J5X21iIjogMjU3ODM4LCAiaXBtaV9hZGRyZXNzIjogIjE3Mi4yMC44LjI3In1dfSwgeyJjb3VudCI6IDEsICJmbGF2b3IiOiAiaXJvbmljLXN0b3JhZ2UtcGVyZiIsICJub2RlX2xpc3QiOiBbeyJtYWNzIjogWyI5YzpkYzo3MTpkNjpjMDplOCJdLCAiaXBtaV91c2VybmFtZSI6ICJyb290IiwgImNwdXMiOiAzMiwgImlwbWlfcGFzc3dvcmQiOiAiKioqKioqIiwgImxvY2FsX2diIjogNzQ0LCAiaWQiOiAiN2UzMzY1M2MtMWVkNy00OGFmLWJhZGUtYjAyNGE3ZWMzMjBjIiwgInNpemUiOiA3NDUsICJjcHVfYXJjaCI6ICJODZfNjQiLCAibmFtZSI6ICI3MTE0ODgtaXJvbmljMTciLCAibWVtb3J5X21iIjogMTMxMDcyLCAiaXBtaV9hZGRyZNzIjogIjE3Mi4yMC44Ljc4In1dfV0="}}
Sleeping 20
Setting node id 0f80e701-9eb6-4272-9f74-2da9fbb750d9 to provision state manage
Setting node id 0f80e701-9eb6-4272-9f74-2da9fbb750d9 to maint state
Setting node id 0f80e701-9eb6-4272-9f74-2da9fbb750d9 to provision state provide
Setting node id 7e33653c-1ed7-48af-bade-b024a7ec320c to provision state manage
Setting node id 7e33653c-1ed7-48af-bade-b024a7ec320c to maint state
Setting node id 7e33653c-1ed7-48af-bade-b024a7ec320c to provision state provide

```
