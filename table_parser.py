import re
import ipaddress
import socket
from paramiko import SSHClient
from scp import SCPClient


def Table(IPParts,dict={}):
	IPParts = re.sub(r'[{}\s]','',IPParts)#удаляет ненужные символы
	IPParts = re.sub(r',',' ',IPParts)
	IPTable = re.split(r'\s',IPParts)
	if IPTable[0] == 'any':
		return [ipaddress.ip_network('0.0.0.0/0')]
	IPTable = list(map(lambda x: IPRepr(x), IPTable))
	NegTable, IPTable = NotIPRange(IPTable)
	IPTable = list(map(lambda x: GetIP(x), IPTable))
	NegTable = list(map(lambda x: IPStringTransform(x),NegTable))
	NegTable = ExpandList(NegTable)
	IPTable = list(map(lambda x: IPStringTransform(x,dict),IPTable))
	IPTable = ExpandList(IPTable)
	try:
		Rez = SubTract(IPTable, NegTable)
		Rez = list(ipaddress.collapse_addresses(Rez))
	except:
		print('\n'*3)
		print('There are letters in the row. Fix the definition of the table:',IPTable)
	return Rez

def IPRepr(num):
	dots = num.count('.')
	if '/' in num and dots < 3:
		List = re.split(r'/',num)
		if dots == 0:
			return List[0]+'.0.0.0'+'/'+List[1]
		elif dots == 1:
			return List[0]+'.0.0'+'/'+List[1]
		elif dots == 2:
			return List[0]+'.0'+'/'+List[1]
	return num

def GetIP(arg):
	if re.search(r'\.[a-z]+$', arg):
		return socket.gethostbyname(arg)
	return arg

def IPStringTransform(x,dict={}):
	
	PatternIp = r'\b(?<!\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'#REG для ip адресов и сеток
	PatternRange = r'\b[0-9]+(?:\.[0-9]+){3}\s*-\s*[0-9]+(?:\.[0-9]+){3}\b'
	pattern = r'\b([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s*)-(\s*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\b'

	if re.fullmatch(PatternIp, x)!=None:
		return ipaddress.ip_network(x)
	elif re.fullmatch(PatternRange, x)!=None:
		m = re.match(pattern,x)
		cand = list(ipaddress.summarize_address_range(ipaddress.IPv4Address(m.group(1)), ipaddress.IPv4Address(m.group(2))))
		return cand
	elif x in dict:
		return dict[x]
	return x

def NotIPRange(xList):
	PatternNotIp = r'(?<=\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?'
	NTable = []
	ExList = []
	for i in xList:
		m = re.search(PatternNotIp,i)
		if m!=None:
			NTable.append(m.group(0))
		else:
			ExList.append(i)
	return NTable, ExList

def Exclude(A,B):
	try:

		m = list(A.address_exclude(B))

		return m
	except ValueError:
		return A


def SubTract(pos, neg):
	Final = []
	for i in pos:
		rez = [i]

		for j in neg:
			rez = list(map(lambda x: Exclude(x,j), rez))

			rez = ExpandList(rez)

		Final.extend(rez)
	return Final


def ExpandList(rez):
	final = []
	for x in rez:
		if type(x)==list:
			final.extend(x)
		else:
			final.append(x)
	return final

def ErrorCheck(y,x):
	try:
		if y in x:
			return True
		else:
			return False
	except:
		print('Please, check table definition:',x)
		print('\n'*3)
		return True


Inpt = ipaddress.IPv4Address('10.13.252.123')


h_petr = SSHClient()
h_petr.load_system_host_keys()
h_petr.connect('85.114.0.138',
				password='Gai2juch',
				username='mingalimov')

print(h_petr.get_transport())

squid='/usr/local/etc/squid/squid.conf'
pfconf='/etc/pf.conf'

with SCPClient(h_petr.get_transport()) as Conf:

	Conf.get(pfconf, 
				local_path='/home/damir/Python/files/pf.conf')


fromto=r'(?<!#)(?:[^#]*)from\s+([^#{}\s]+|{[^#]+})\s+to\s+([^#{}\s]+|{[^#port]+})'
with open('/home/damir/Python/files/pf.conf','r',encoding= 'utf-8', errors='ignore') as inpt:
	TabList={}
	
	for ACLString in inpt:#read the file line by line
		ACLString = ACLString.rstrip()
		if re.search(r'^\s*#', ACLString)!=None:
			continue
		
		if re.search(r'(?<=^table)\s*([^\s#]+)\s*(?=[^#])([^#]*)(?=#|$)',ACLString)!=None:#searching for acl tables
			obj = re.search(r'(?<=^table)\s*([^\s#]+)\s*(?=[^#])([^#]*)(?=#|$)', ACLString)
			TabList[obj.group(1)] = Table(obj.group(2))
		elif re.search(fromto, ACLString)!=None:
			
			m = re.match(fromto, ACLString)
			From = m.group(1)
			To = m.group(2)
			
			
			FromList = Table(From,TabList)
			ToList = Table(To,TabList)
			if any(map(lambda x: ErrorCheck(Inpt,x),FromList)):
				print(ACLString)
			elif any(map(lambda x: ErrorCheck(Inpt,x),ToList)):
				print(ACLString)

