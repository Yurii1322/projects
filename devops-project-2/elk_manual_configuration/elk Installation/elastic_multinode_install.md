#Installation and configuration of a multi-node elasticsearch cluster

## 1. Install elasticsearch on all nodes but do not start the service

## 2. First generate a CA from any node

    cd /usr/share/elasticsearch/bin

    ./elasticsearch-certutil ca

## 3. Generate certificate for elasticsearch using CA certificate

    ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12

### Notes :  Certificates .p12 are generated at 
    cd /usr/share/elasticsearch/

## 4.  Copy the certificate to elasticsearch config
    cp /tmp/elastic-certificates.p12 /etc/elasticsearch/elastic-certificates.p12

## 5. Copy to /tmp for download 
    cp elastic-certificates.p12 /tmp/elastic-certificates.p12
    cd /tmp/
    chmod 777 /tmp/elastic-certificates.p12 


## 6. Make changes to elk-1 elasticsearch.yml

### Cluster settings 
discovery.seed_hosts: ["192.168.1.3", "192.168.1.4", "192.168.1.5"]
cluster.initial_master_nodes: ["elk-1", "elk-2"]

### Security settings 
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.client_authentication: required
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/certs/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/certs/elastic-certificates.p12

# 7. On elk-2 and elk-3

## Copy elasticsearch certificate from ~/home to elasticsearch config
    cp /home/labittraining3/elastic-certificates.p12 .

# 8. change elasticsearch.yml and copy the settings from elk-1
# 9.  restart elasticsearch
    sudo systemctl restart elasticsearch

### To troubleshoot

    journalctl -f -u elasticsearch



### Troubleshooting tip

## In case nodes dont join 
###Shut down all the nodes.
systemctl stop elasticsearch
###Completely wipe each node by deleting the contents of their data folders.
rm -rf /var/lib/elasticsearch/*
###Configure cluster.initial_master_nodes as described above.

###Restart all the nodes and verify that they have formed a single cluster.
systemctl restart elasticsearch

#### if you previously setup passwords , on any node
cd /usr/share/elasticsearch/bin/
./elasticsearch-setup-passwords auto

### change kibana password
nano /etc/kibana/kibana.yml

### secure kibana communication

# 1. Generate a http certificate to encrypt encryption on elasticsearch
./elasticsearch-certutil http
Generate a CSR? [y/N]n
Use an existing CA? [y/N]y
Generate a certificate per node? [y/N]n
hostname : *.*
IP -> list all node IPs and localhost

# 2. Unzip the zip file and from elasticsearch directory in zip
    cp http.p12 /etc/elasticsearch/

#3. in leasticsearch.yml
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/certs/http.p12


# 3. kibana

## From zip/kibana directory
cp elasticsearch-ca.pem /etc/kibana/

# 4. edit kibana.yml

## add all hosts to the list , queries are performed in round robin fashion

elasticsearch.hosts: ["https://192.168.1.3:9200", "https://192.168.1.4:9200", "https://192.168.1.5"]

## add new password
elasticsearch.username: "kibana_system"
elasticsearch.password: "Er4aLuGEOSpn24j7tsu1"

elasticsearch.ssl.certificateAuthorities: [ "/etc/kibana/elasticsearch-ca.pem" ]

# 5. restart kibana
systemctl restart kibana

