# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, json
import inspect
from os import environ as env

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.xsmall"
private_net = "UPPMAX 2021/1-5 Internal IPv4 Network"
image_name = "Ubuntu 18.04"
key_name = "joli-laptop"

vm_name = "joli-lab3"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

cfg_file_path = os.getcwd()+'/cloud-config.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-config.txt is not in current working directory")

secgroups = ['default', 'joli']

print("Creating instance ... ")
instance = nova.servers.create(name=vm_name, image=image, flavor=flavor, userdata=userdata, nics=nics,
                               security_groups=secgroups, key_name=key_name)
inst_status = instance.status
print("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status == 'BUILD':
    print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status
print("Instance: " + instance.name + " is in " + inst_status + " state")

stream = os.popen('openstack floating ip list -f json')
output = stream.read()
ip_objs = json.loads(output)

print('Associating a floating IP...')
for ip_obj in ip_objs:
    if ip_obj['Port'] is None:
        ip_address = ip_obj["Floating IP Address"]
        os.system(f'openstack server add floating ip {vm_name} {ip_address}')
        print(f'Floating IP {ip_address} associated.')
        break
print('Service ready.')
