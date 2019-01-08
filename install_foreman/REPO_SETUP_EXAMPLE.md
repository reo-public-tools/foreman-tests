# Create an ubuntu repo

```bash

hammer product create  --organization-label Default_Organization --description 'Ubuntu 16.04' --name ubuntu_xenial --label ubuntu_xenial

hammer organization list
hammer product list --organization-id 3

wget http://us.archive.ubuntu.com/ubuntu/dists/xenial/Release.gpg
hammer gpg create --key Release.gpg --name 'xenial' --organization-id 3

hammer repository create --organization-id 3 --product-id 2 --name 'Ubuntu 16.04' --content-type deb --url http://us.archive.ubuntu.com/ubuntu --deb-releases xenial --deb-architectures 'amd64' --mirror-on-sync true --publish-via-http true --gpg-key xenial

hammer repository list



tmux
hammer repository synchronize --organization-id 3 --product-id 2 --id 2
Ctrl-B d


```




