import re
import ipaddress
import socket

def Table(IPParts,dict=[]):
	IPParts = re.sub(r'[{}\s]','',IPParts)#удаляет ненужные символы
	IPParts = re.sub(r',',' ',IPParts)
	IPTable = re.split(r'\s',IPParts)
	IPTable = list(map(lambda x: IPRepr(x), IPTable))
	NegTable, IPTable = NotIPRange(IPTable)
	IPTable = list(map(lambda x: GetIP(x), IPTable))
	NegTable = list(map(lambda x: IPStringTransform(x),NegTable))
	NegTable = ExpandList(NegTable)
	IPTable = list(map(lambda x: IPStringTransform(x,dict),IPTable))
	IPTable = ExpandList(IPTable)
	Rez = SubTract(IPTable, NegTable)
	Rez = list(ipaddress.collapse_addresses(Rez))
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
	if re.search(r'^[a-zA-Z.]+$', arg):
		return socket.gethostbyname(arg)
	return arg

def IPStringTransform(x,dict=[]):
	
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

Rez = Table('{ 85.114.2.0/24, !85.114.4.190, !79.142.85.16/30, 1/8, ping.eu, 8.8.8.0/24, 10.6.7.6-10.6.7.10, 10.2.34.2 - 10.2.34.4 }')

TableDict = {'<teamviewer>':Rez}

Str = '{ <teamviewer>, 46.163.100.220 , !8.8.8.9}'

#print(TableDict)
print(Table(Str,TableDict))