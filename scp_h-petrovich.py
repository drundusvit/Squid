from paramiko import SSHClient
from scp import SCPClient

h_petr = SSHClient()
h_petr.load_system_host_keys()
h_petr.connect('85.114.0.138')

print(h_petr.get_transport())

with SCPClient(h_petr.get_transport()) as squid:

	squid.get('/usr/local/etc/squid/squid.conf', local_path='files/')