from paramiko import SSHClient
from scp import SCPClient

kant7 = SSHClient()
kant7.load_system_host_keys()
kant7.connect('support.kant7.obit.ru')

print(kant7.get_transport())

scp = SCPClient(kant7.get_transport())

scp.get('testtest', local_path='files/')

scp.close()
