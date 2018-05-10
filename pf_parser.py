import os
import re
import ipaddress

class Table():

	def __init__(self):
		self.nets=[]
		self.notnets=[]
		self.name=''
		self.leftovers=''

	def add_nets(self,*net):
		for i in net:
			self.nets.append(i)
	def add_notnets(self,*net):
		for i in net:
			self.notnets.append(i)
	def add_leftoveres(self,string):
		self.leftovers=string

	def add_name(self,string):
		self.name=string
    


def expand_ranges(IPRanges,ACLString):#
	'''функция дополняющая список объектов IPv4Address объектами из диапазонов адресов(192.168.1.1 - 192.168.2.1)
		на вход принимает list, который пополняет и сырую строку с ip
	'''
	PatternRange = r'\b[0-9]+(?:\.[0-9]+){3}\s*-\s*[0-9]+(?:\.[0-9]+){3}\b'
	listrange = re.findall(PatternRange,ACLString)
	pattern = r'\b([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s*)-(\s*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\b'
	for Var in listrange:
		m = re.match(pattern,Var)
		cand = list(ipaddress.summarize_address_range(ipaddress.IPv4Address(m.group(1)), ipaddress.IPv4Address(m.group(2))))
		IPRanges.nets.extend(cand)
	ACLString = re.sub(pattern, r'',ACLString)
	return IPRanges, ACLString

def IPStringTransform(ACLString):
	'''
	на вход принимает сырую строку с ip адресами
	return list of IPv4Networks objects
	'''
	IPRanges=Table()# Список для заполнения результатами парсинга
	PatternIp = r'\b(?<!\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'#REG для ip адресов и сеток
	PatternNotIp = r'\b(?<=\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'
#получить список диапазонов ip адресов
	IPRanges, ACLString = expand_ranges(IPRanges,ACLString)
	listip = re.findall(PatternIp,ACLString)#найти все одиночные ip и ip с масками
	SoloIPRanges = list(map(lambda x: ipaddress.ip_network(x), listip))#преобразовать в объекты IPv4Address
	listnotip = re.findall(PatternNotIp,ACLString)#найти все одиночные отрицательные ip и ip с масками
	SoloNotIPRanges = list(map(lambda x: ipaddress.ip_network(x), listnotip))#преобразовать в объекты IPv4Address
	IPRanges.add_nets(SoloIPRanges)
	IPRanges.add_notnets(SoloNotIPRanges)
	#print(IPRanges)
	#print(SoloNotIPRanges)
	return IPRanges.nets, IPRanges.notnets

def table(ACLString):
	table_string=Table()
	m = re.search(r'(?<=^(table))\s*([^\s]+)\s*({[^#]*})(.*)',ACLString)
	table_string.add_name(m.group(2))
	print(table_string.name)
	table_string.add_leftoveres(m.group(4))
	print(table_string.leftovers)




with open('/home/damir/Python/files/pf.conf.oneline') as inpt:
	#ListName=[]#list of all acl tables where the ip is located
	#DSTDic={}
	#https=[]
	for ACLString in inpt:#read the file line by line
		ACLString = ACLString.rstrip()
		print(ACLString)
		if re.search(r'(?<=^table)\s*([^\s]+)\s*(?={)',ACLString)!=None:#searching for acl tables
			table(ACLString)
			#FinalList = IPStringTransform(ACLString)
			#print(FinalList.nets)
			#print(FinalList.notnets)
			#if any(map(lambda x: IPCheck in x,FinalList)):
			#	m=re.search(r'(?<=^acl)\s*([^\s]+)\s*(?=src)',ACLString)
			#	ListName.append(m.group(1))#add the name of acl
			#	#print(ListName)
