# Configure X-Pack Security 

## 1. stop kibana

    sudo systemctl stop kibana

## 2. Stop elasticsearch 

    sudo systemctl stop elasticsearch

## 3. enable xpack in elasticsearch.yml

    sudo nano /etc/elasticsearch/elasticsearch.yml
    xpack.security.enabled: true

## 4. Setup default user passwords

    sudo systemctl start elasticsearch
    cd /usr/share/elasticsearch/bin
    sudo ./elasticsearch-setup-passwords auto


## System Passwwords 

### << Default user passwords go here >>



Changed password for user apm_system
PASSWORD apm_system = 2oNBnEkD2E00JcZ0mQk8

Changed password for user kibana_system
PASSWORD kibana_system = nzze23DH1oci9KaMRkAZ

Changed password for user kibana
PASSWORD kibana = nzze23DH1oci9KaMRkAZ

Changed password for user logstash_system
PASSWORD logstash_system = oLlINldOg1abTBc6WKZ2

Changed password for user beats_system
PASSWORD beats_system = GynI0zW73pei6ZMwP6uo

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = 9yvaBZZCiNLHPDGiwcMQ

Changed password for user elastic
PASSWORD elastic = FiLKeBQZE4EiT6yw78rj

## 5. Add the default username in kibana
elasticsearch.username: "kibana"

elasticsearch.password: "new_password"



