# Overview

Here we will go over all the steps needed to provision a host within the openstack environment. 
When all is said and done, we should have an environment ready to deploy osa or osp to.

## Provisioning Configuration

### Add rackspace ca certs

The url used on a compute resource must have a valid certificate. In order to verify,
the system needs set up with the ca certs used to sign your openstack endpoint certs.


```bash



cat <<EOF > /etc/pki/ca-trust/source/anchors/rs_root_ca_1.crt 
-----BEGIN CERTIFICATE-----
MIIFTDCCAzSgAwIBAgIQNJwfKVTMrbBDWXAjkS7/UzANBgkqhkiG9w0BAQsFADA3
MRcwFQYDVQQKEw5SYWNrc3BhY2UgSW5jLjEcMBoGA1UEAxMTUmFja3NwYWNlIFJv
b3QgQ0EgMTAeFw0xNzA1MTAxNjMyMTdaFw00MjA1MTAxNjMyMTdaMDcxFzAVBgNV
BAoTDlJhY2tzcGFjZSBJbmMuMRwwGgYDVQQDExNSYWNrc3BhY2UgUm9vdCBDQSAx
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwWmZdFgUAmeHqijMGVc3
WyGSPZDelBfB88Cd91jRJCP2YhNcXG0RMwBYTYsJwI2BI5tSdwDIfDb32XqfbPKd
or6oLITDNzLoOQN1klSnzV7eVuMBQfo5We+EcYWaqYUqgFbDRx/yLugogADhFDT9
0M63aaK1Plixeyw+oajjYxbrRiMq+p2O9m4XijEqOK+vHxLTBLDfZ0S+DMXThAFD
XKGhNnKM2j8XEIEnLjuMyiZNuQEfSdhJigr7iDizaWWdrBYfZLWgDCjF8CX3xZxg
Ft51Po0sq6bDsGayOn7POrvK8m2PrZCXvUAXc3OXv14JiGa/IIM+f+sBNBUXvV3F
uwWMzmPqKHmP8nZN8VYQzNhQ0NrtXzgClbHYFjCoOdGHzoQzOcD//vUUvcL3Pd1a
CzpKSivxVLr8EdZhCjW8QzGXr0lMK9ajeCEZghMfV7e7XlKSj+zL7NFYkKYKf50v
ChjERQ0VM6Ty87l2EMHagwrHL6hI0L7O/Bquoc3RcqEOqBT5wjjuyQZOe3Q7X2Fw
rcsVnRmgFv3fE/MARwL5uKdc8JJopuU8EILxxSBv4CWMVMtAaeoFmlLskoeGMHHP
fp1qHNIEopt/8i0BsN7VOyyWcqbuy0vxgNv6+5BK9YlxitxR9pC0+EhbsP2yzKOW
/wGsphP2m9X91zbKr7Q4MEUCAwEAAaNUMFIwDgYDVR0PAQH/BAQDAgEGMA8GA1Ud
EwEB/wQFMAMBAf8wHQYDVR0OBBYEFIMvOaa5mQFs2X4W279J8Oyw1CvGMBAGCSsG
AQQBgjcVAQQDAgEAMA0GCSqGSIb3DQEBCwUAA4ICAQBbEUAHbBLGdeLYNCJSfwM2
Jhs2Y+ZPxn70slHST2fr7jorg++/1GwPKb/QnyLzYd7d4Xv0umtoMsb1WwuIdzvY
vSgQLCk+ueoJYQv6B0yodByLBNDusWkdfGyOt1PK6HDfGJrG2L61ZwAvBNvBceox
W0fNuj28PiCAiiyIv4rsjFtzIZlUUmYoJ5RIY1WfW1UhpT6SNW9EgOBzpaXlpGX3
ZBzd4SIWOhGUZH00/ZAhqVwYYyHnpituTj/Gz2c5if3VDOb7Gzo1rFnnjh0mv8I6
9a8HvFUZguQnobxwCEIPzo5z6v+l1/Wp/Kl0obztZw5Z/eK75vIF40BjpS7/uSkN
md8mmsm4fRoWNj9VxOSIaPcPsfhTFTdVdeVYGMVtCfkpfvAxFog8Vsuzw13KeqNJ
nlbkALs+AJ70BQcLSaHEvc+B+g5mDWrQWtCYwrcO6wVPEuK8pDV9U7UvO89Wh5P+
cq42OAJ0HxOZmLECuuBw+ynjShPcrmGx0GodNVptm81BrFjO04xWWCvyXKrC7L2o
7we0xbpp3Iv0WlwdikOI2rZ40L2sNoiGUhFLqRA3dHIGmVsl0CltqdTB0x2i0TVt
UUdQhV6wj8J6BZ/kBdGnCPLsnhKOMWgsTogpQv/FwBDneSO8WlBfLREMsIGB1wXx
6kexs/oEWYwL7j4KtYqxWg==
-----END CERTIFICATE-----
EOF

cat <<EOF > /etc/pki/ca-trust/source/anchors/rs_issuing_ca_1.crt 
-----BEGIN CERTIFICATE-----
MIIIWjCCBkKgAwIBAgITGQAAAASeol/i3qNNqQAAAAAABDANBgkqhkiG9w0BAQsF
ADA3MRcwFQYDVQQKEw5SYWNrc3BhY2UgSW5jLjEcMBoGA1UEAxMTUmFja3NwYWNl
IFJvb3QgQ0EgMTAeFw0xNzA1MTAxNzM0NDBaFw0yNzA1MTAxNzQ0NDBaMDoxFzAV
BgNVBAoTDlJhY2tzcGFjZSBJbmMuMR8wHQYDVQQDExZSYWNrc3BhY2UgSXNzdWlu
ZyBDQSAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzlh1ffdXX33m
EPNfLAcOccLzsWiH2QDgU8hoF9HPNV0jVauCw4B/gTowKHz2iTmCgeymeLJ3cNR7
zm4buvOBJtWePTNfDVuVJ2viscGgvXCEnNO2QWxgGtwEg9+lZpXISeel6aFHVvYq
c3hKV6L9C0+RU6lV2K8WeBuYZ7YJ43PeDJr06FRZnev9m/TPFDQmG8ZTcL1XSYDy
KlRDtxFrSbeP0bbKWjLFrft1ABkqMNGGq0BxZe1k+HLoavMNRCRyD7l66xnGEbYK
IRfRbpJ7lOKnoQIoTiD+fi3XmFoNo/f8zCL7zCkLUekOjAJ5ACMNok8NxJ9pnhnB
SEDkNtm5LQIDAQABo4IEWjCCBFYwDgYDVR0PAQH/BAQDAgEGMBAGCSsGAQQBgjcV
AQQDAgEAMB0GA1UdDgQWBBQOwQYlUkCDuph0nwhAFnWcjJxrrzCCAyQGA1UdIASC
AxswggMXMIIDEwYMKwYBBAGBo3wEAQEBMIIDATCCAsoGCCsGAQUFBwICMIICvB6C
ArgAVABoAGkAcwAgAEMAZQByAHQAaQBmAGkAYwBhAHQAaQBvAG4AIABBAHUAdABo
AG8AcgBpAHQAeQAgACgAQwBBACkAIABpAHMAIABhACAAUgBhAGMAawBzAHAAYQBj
AGUAIABVAFMALAAgAEkAbgBjAC4AIAAoAFIAYQBjAGsAcwBwAGEAYwBlACkAIABp
AG4AdABlAHIAbgBhAGwAIAByAGUAcwBvAHUAcgBjAGUALgAgAEMAZQByAHQAaQBm
AGkAYwBhAHQAZQBzACAAaQBzAHMAdQBlAGQAIABiAHkAIAB0AGgAaQBzACAAQwBB
ACAAYQByAGUAIABmAG8AcgAgAGkAbgB0AGUAcgBuAGEAbAAgAFIAYQBjAGsAcwBw
AGEAYwBlACAAdQBzAGUAIABvAG4AbAB5AC4AIABBAG4AeQAgAG4AbwBuAC0AUgBh
AGMAawBzAHAAYQBjAGUAIABwAGEAcgB0AHkAIABzAGgAYQBsAGwAIABuAG8AdAAg
AHIAZQBsAHkAIABvAG4AIAB0AGgAaQBzACAAQwBBACAAZgBvAHIAIABhAG4AeQAg
AHIAZQBhAHMAbwBuAC4AIABGAG8AcgAgAG0AbwByAGUAIABpAG4AZgBvAHIAbQBh
AHQAaQBvAG4ALAAgAHAAbABlAGEAcwBlACAAcgBlAGYAZQByACAAdABvACAAdABo
AGUAIABSAGEAYwBrAHMAcABhAGMAZQAgAEMAZQByAHQAaQBmAGkAYwBhAHQAaQBv
AG4AIABQAHIAYQBjAHQAaQBjAGUAIABTAHQAYQB0AGUAbQBlAG4AdAAgAGEAdAA6
ACAAaAB0AHQAcAA6AC8ALwBwAGsAaQAuAHIAYQBjAGsAcwBwAGEAYwBlAC4AYwBv
AG0ALwBjAHAALwBjAHAAcwAuAGgAdABtAGwwMQYIKwYBBQUHAgEWJWh0dHA6Ly9w
a2kucmFja3NwYWNlLmNvbS9jcC9jcHMuaHRtbAAwGQYJKwYBBAGCNxQCBAweCgBT
AHUAYgBDAEEwEgYDVR0TAQH/BAgwBgEB/wIBADAfBgNVHSMEGDAWgBSDLzmmuZkB
bNl+Ftu/SfDssNQrxjBHBgNVHR8EQDA+MDygOqA4hjZodHRwOi8vcGtpLnJhY2tz
cGFjZS5jb20vUmFja3NwYWNlJTIwUm9vdCUyMENBJTIwMS5jcmwwUgYIKwYBBQUH
AQEERjBEMEIGCCsGAQUFBzAChjZodHRwOi8vcGtpLnJhY2tzcGFjZS5jb20vUmFj
a3NwYWNlJTIwUm9vdCUyMENBJTIwMS5jcnQwDQYJKoZIhvcNAQELBQADggIBAJzg
09ZUeoGFAMNM+JtTwWth28K266uIxZpGA2QBfWs9Ft6o0S7kRpopQUw5vDxwEtFd
1qBUubEKPDo1q+DOJpxg1uG/+rwRXTd7NJ+Lz6OWwxzn0LOTRyYsAAI1lIIIesWe
kfGcIrK9tBJaelpIlziK/m+j18hjJOjpY1a/e3h8Oi5jNlwh8edXb8xd+ROL39+S
DNwTMBdReTQ6K9VLuetkocW4j0IEB6Ggb1PuHUa7y2Fxd3v1EARBfwh32G6+qiCW
x0XNdolFLzOv6nj79no9HEvbhPaUXV4CaPKBXliThfHeff9VW2hYUNFYdl79pWvq
OxwQ2oDAIPwOWfq/o7zKPgLY+jYONOn37Z8J40USkdygRm5yDl7K6DKLfJkGsRBD
6LBJAv1TR6s6cUtRykaZBorHhDXEj64JgRe2KYOa02sdz09pxw1Tv00ZcAKVD3a/
vCpwA7bkeiz6wr2dIGf6WTWnMuzkI6/R1Vp0NeZD395M8/P8W4sWFPZLCf9iWESt
Us/XxpW7Eb7yZ6zXfMl6o5KhZ50FRV1uSB236UjmAsRWKEU+dOYq7d5TSzTE68Nk
uqA56R5PGeWor4oXere7B+LP7fx9pUWXMi8Y1LsXQHXdCbUHH/h21+bdQlmhzwtq
zTMydKTeAovWyQF3cKrHlulEmUiWSAdlBntuTy1r
-----END CERTIFICATE-----
EOF


update-ca-trust

systemctl restart foreman-proxy


```

# Set up the compute resource

```bash
#GUI:
#  - Create Compute Resource
#    -> Name: phobos-int.rpc.rackspace.com
#    -> Provider: openstack
#    -> Description: Phobos openstack environment
#    -> URL: http://phobos-int.rpc.rackspace.com:5000/v2.0/tokens
#    -> User: labs-admin
#    -> Pass: <removed>
#    -> Domain: labs-domain
#    -> Tenant: [Load Tenants] select 'labs-project'
#    -> Allow external network as main network: 'checked'
#  - Click -> Test Connection
#  - Locations: 'Lab Location'
#  - Organizations: 'Lab Organization'
#  - Submit


# CLI(password placed in /root/.labs-admin-pass):
hammer compute-resource create \
    --description "Phoobs openstack cluster" \
    --domain labs-domain \
    --tenant labs-project \
    --location 'Lab Location' \
    --organization 'Lab Organization' \
    --name 'phobos-int.rpc.rackspace.com' \
    --url 'http://phobos-int.rpc.rackspace.com:5000/v2.0/tokens' \
    --provider Openstack \
    --user labs-admin \
    --password  $(cat /root/.labs-admin-pass)
```


### Create an Operating System

The image requires an operating system definition to be created. 
We will set up one for xenial and bionic here.

```bash

hammer os create --architectures 'x86_64' \
    --description "Ubuntu Xenial" \
    --family Debian \
    --major 16 \
    --minor 04 \
    --name "ubuntu-xenial" \
    --location 'Lab Location' \
    --organization 'Lab Organization' \
    --password-hash SHA256 \
    --release-name xenial

hammer os create --architectures 'x86_64' \
    --description "Ubuntu Bionic" \
    --family Debian \
    --major 18 \
    --minor 04 \
    --name "ubuntu-bionic" \
    --location 'Lab Location' \
    --organization 'Lab Organization' \
    --password-hash SHA256 \
    --release-name bionic


```


### Import the images to be used


Lets import the ubuntu and bionic images for baremetal.

```bash

# hammer compute-resource image available --compute-resource 'phobos-int.rpc.rackspace.com' | egrep 'baremetal-ubuntu-(xenial|bionic) '
baremetal-ubuntu-bionic                               | 127e41bd-eb08-4214-bd58-d6b2d3a63ec1
baremetal-ubuntu-xenial                               | 4ee7e5a8-05b2-473a-bc6a-44139ad9548a


hammer compute-resource image create \
    --name 'baremetal-ubuntu-xenial' \
    --architecture x86_64 \
    --compute-resource 'phobos-int.rpc.rackspace.com' \
    --operatingsystem 'Ubuntu Xenial' \
    --uuid '4ee7e5a8-05b2-473a-bc6a-44139ad9548a' \
    --username 'ubuntu' \
    --user-data true

hammer compute-resource image create \
    --name 'baremetal-ubuntu-bionic' \
    --architecture x86_64 \
    --compute-resource 'phobos-int.rpc.rackspace.com' \
    --operatingsystem 'Ubuntu Bionic' \
    --uuid '127e41bd-eb08-4214-bd58-d6b2d3a63ec1' \
    --username 'ubuntu' \
    --user-data true

hammer compute-resource image list --compute-resource 'phobos-int.rpc.rackspace.com' 
---|-------------------------|------------------|----------|-------------------------------------
ID | NAME                    | OPERATING SYSTEM | USERNAME | UUID                                
---|-------------------------|------------------|----------|-------------------------------------
3  | baremetal-ubuntu-xenial | Ubuntu Xenial    | ubuntu   | 4ee7e5a8-05b2-473a-bc6a-44139ad9548a
4  | baremetal-ubuntu-bionic | Ubuntu Bionic    | ubuntu   | 127e41bd-eb08-4214-bd58-d6b2d3a63ec1
---|-------------------------|------------------|----------|-------------------------------------


```




### Create compute profiles

I'm not seeing a compute_profile in hammer, but I do in the api. For now we will just use the GUI.

```
- Go to https://172.20.41.149/compute_profiles
  -> 'Create Compute Profile'
    -> name: 'ironic-standard-bionic'
    -> submit
  -> 'Infrastructure'
    -> 'Compute Profiles'
      -> ironic-controller
      -> compute resource: 'phobos-int.rpc.rackspace.com(Openstack)'
        -> Compute Profile: 'ironic-standard-bionic'
        -> Compute resource: 'phobos-int.rpc.rackspace.com' 
        -> Flavor: 'ironic-standard'
        -> Availibility zone: nova
        -> Image: baremetal-ubuntu-bionic
        -> Tenant: labs-project
        -> Security Groups: default
        -> Internal network: ironic 
        -> Floating IP: none
        -> Boot from volume: leave unchecked
        -> New boot volume size(GB): leave blank.
        -> Scheduler hint filter: None
  -> 'Infrastructure'
    -> 'Compute Profiles'
      -> ironic-storage-perf-bionic
      -> compute resource: 'phobos-int.rpc.rackspace.com(Openstack)'
        -> Compute Profile: 'ironic-storage-perf-bionic'
        -> Compute resource: 'phobos-int.rpc.rackspace.com' 
        -> Flavor: 'ironic-storage-perf'
        -> Availibility zone: nova
        -> Image: baremetal-ubuntu-bionic
        -> Tenant: labs-project
        -> Security Groups: default
        -> Internal network: ironic 
        -> Floating IP: none
        -> Boot from volume: leave unchecked
        -> New boot volume size(GB): leave blank.
        -> Scheduler hint filter: None
  
```







### Fix to use internalURL for our needs

Cinder volume issues due to internalURL returning external endpoint(broke in cinder newton)

```
[root@lab-deploy01 app]# vi /usr/share/foreman/app/models/compute_resources/foreman/model/openstack.rb
        #:openstack_endpoint_type     => "publicURL"
        :openstack_endpoint_type     => "internalURL"

[root@lab-deploy01 app]# grep '#volume' /usr/share/foreman/app/models/compute_resources/foreman/model/openstack.rb
      #volume_client.volumes.delete(@boot_vol_id) if args[:boot_from_volume]
[root@lab-deploy01 app]# grep '#boot' /usr/share/foreman/app/models/compute_resources/foreman/model/openstack.rb
      #boot_from_volume(args) if Foreman::Cast.to_bool(args[:boot_from_volume])


systemctl restart foreman-proxy

```


### Disable safe mode rendering

We need access to subnet parameters.  Safemode keeps us from doing this.

```
  - 'Administer'
    -> 'safe' -> search
    -> Update 'Safemode rendering' to 'No'
```


### Create userdata template

Where we are using ironic images, we will want to set up a userdata
template for cloud-init.

```
  - 'Hosts'
    -> 'Provisioning Templates'
    -> Search for 'default-userdata'
      -> 'Clone'
        -> Name: custom-baremetal-userdata
        -> Association Tab: Move over all OS's defined

(Put template info here, or a link to the text)

  - 'Hosts'
    -> 'Operating Systems'
      -> 'Ubuntu Bionic'
        -> Templates
          -> User data template 'custom-baremetal-userdata'
          -> Submit
    
```



### Create a labenv environment for puppet

We will start by creating a simple lab environment and installing a motd module into it.

```bash
mkdir -p /etc/puppetlabs/code/environments/compute_resource_phobos
hammer environment create --name compute_resource_phobos --location "Lab Location" --organization "Lab Organization"
puppet module install --environment compute_resource_phobos puppetlabs-motd

hammer proxy list  (get the proxy id for the import command)
hammer proxy import-classes --environment compute_resource_phobos --location "Lab Location" --organization "Lab Organization" --id 1
```



### Create a Host Group

Just for testing, it looks like associating puppet classes may be easier
with host groups.  I'll give it a try here.

```bash
  - 'Configure'
    -> 'Host Groups'
      -> 'Create Host Group'
        -> Host Group(Tab)
          -> Name: ironic-general
          -> Description: Testing a general ironic config
```
          
    

### Fix subnet parameters in node classifer

The subnets parameters are missing from the ENC data.  This is a hack to add them back
in. 


```bash
vi /etc/puppetlabs/puppet/foreman.yaml   (update the user/password with admin creds)

vi /etc/puppetlabs/puppet/node.rb
...
############################
# Starting Custom Block
############################

def pull_subnet_info(subnet_id)
  foreman_url      = "#{url}/api/subnets/#{subnet_id}?format=yml"
  uri              = URI.parse(foreman_url)
  req              = Net::HTTP::Get.new(uri.request_uri)
  http             = Net::HTTP.new(uri.host, uri.port)
  req.basic_auth "#{SETTINGS[:user]}", "#{SETTINGS[:password]}"

  http.use_ssl     = uri.scheme == 'https'
  if http.use_ssl?
    if SETTINGS[:ssl_ca] && !SETTINGS[:ssl_ca].empty?
      http.ca_file = SETTINGS[:ssl_ca]
      http.verify_mode = OpenSSL::SSL::VERIFY_PEER
    else
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    end
    if SETTINGS[:ssl_cert] && !SETTINGS[:ssl_cert].empty? && SETTINGS[:ssl_key] && !SETTINGS[:ssl_key].empty?
      http.cert = OpenSSL::X509::Certificate.new(File.read(SETTINGS[:ssl_cert]))
      http.key  = OpenSSL::PKey::RSA.new(File.read(SETTINGS[:ssl_key]), nil)
    end
  end
  res = http.request(req)

  raise "Error retrieving subnet info for #{subnet_id}: #{res.class}\nCheck Foreman's /var/log/foreman/production.log for more information." unless res.code == "200"
  res.body
end

def add_subnet_params(certname, orig_result)

  yaml = YAML.load(orig_result)
  for entry in yaml["parameters"]["foreman_subnets"]
    testresult = pull_subnet_info("#{entry['name']}")
    cursubnet = YAML.load(testresult)
    entry["parameters"] = Hash.new
    for curentry in cursubnet["parameters"]
      entry["parameters"]["#{curentry['name']}"] = "#{curentry['value']}"
    end
  end

 yaml.to_yaml
end

############################
# Ending Custom Block
############################

...
          # modified for subnet params
          orig_result = enc(certname)
          result = add_subnet_params(certname, orig_result)
          # modified for subnet params

...
```


################################
# Build out a networking module
################################


Generate an empty module.

```bash
puppet module generate shananigans-lab_network_ironic_phobos --environment compute_resource_phobos
```

Import it into the environment in foreman
```bash
  -> 'Configure'
    -> 'Environments'
      ->  'Click down arrow next to classes' -> 'Immport classes from lab-deploy01.localdomain'
        -> Click 'lab_network_ironic_phobos' box then add.
```




