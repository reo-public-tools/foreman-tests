# Create a new environment

## Global parameter scope.

To know what we need for the environment, we need to know how the foreman scopes
variables.  Any smaller in scope will override the larger.  A list is provided 
below from the parameters section here: https://www.theforeman.org/manuals/1.18/index.html#4.2.3Parameters

* **Global**: Applies to all hosts.
* **Organization**: Can have muliple orgs per customer or environment.
* **Location**: Could be used to define location based variables(ntp, dns caching...)
* **Domain**: Applied when hosts are associated with a DNS domain.
* **Subnet**: Applied when hosts are associated with a subnet.
* **Operating System**: Applied with hosts are assocated with an OS.
* **Hostgroup Parameters**: Applied to hosts grouped within a hostgroup.
* **Host Parameters**: Applied to a single host.

Be aware that you can use organizations and locations to separate out resources and assign
RBAC permissions for access to those.  This means that you will need to define any repos
again.  If you define the same repo though, the packages in the repos are just linked to
the existing via pulp. This is for a lab environment where we are not worried about permissions
across environments.  For the lab environment, we will just be creating a new domain, subnets and
hostgroup for each lab.  This will allow us to use the 'domain' as our environment global variables
, subnets for subnet specific variables.  We can name everything off of the subdomain for ease of
tracking.



## Setting up the framework


Set up a domain
```bash
hammer domain create --description "Test Domain" --name mnaio.phobos.rpc.rackspace.com --organization-id 3 --location-id 4

```



