from paramiko import SSHClient
from scp import SCPClient

h_petr = SSHClient()
h_petr.load_system_host_keys()
h_petr.connect('85.114.0.138',
				password='',
				username='')

print(h_petr.get_transport())

squid='/usr/local/etc/squid/squid.conf'
pfconf='/etc/pf.conf'

with SCPClient(h_petr.get_transport()) as squid:

	squid.get(pfconf, 
				local_path='/home/damir/Python/files/pf.conf')