import os
import re
import ipaddress
import codecs

class Table():
	clsnum=[]

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
		self.clsnum.append(self.name)
	def __del__(self):
		#print('Deleted')
		self.clsnum.remove(self.name)


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
		IPRanges.extend(cand)
	ACLString = re.sub(pattern, r'',ACLString)
	return IPRanges, ACLString

def IPStringTransform(ACLString):
	'''
	на вход принимает сырую строку с ip адресами
	return list of IPv4Networks objects
	'''
	IPRanges=[]# Список для заполнения результатами парсинга
	PatternIp = r'\b(?<!\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'#REG для ip адресов и сеток
	PatternNotIp = r'\b(?<=\!)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'
#получить список диапазонов ip адресов
	IPRanges, ACLString = expand_ranges(IPRanges,ACLString)
	listip = re.findall(PatternIp,ACLString)#найти все одиночные ip и ip с масками
	SoloIPRanges = list(map(lambda x: ipaddress.ip_network(x), listip))#преобразовать в объекты IPv4Address
	listnotip = re.findall(PatternNotIp,ACLString)#найти все одиночные отрицательные ip и ip с масками
	SoloNotIPRanges = list(map(lambda x: ipaddress.ip_network(x), listnotip))#преобразовать в объекты IPv4Address
	#IPRanges.add_nets(SoloIPRanges)
	#IPRanges.add_notnets(SoloNotIPRanges)
	#print(IPRanges)
	#print(SoloNotIPRanges)
	return SoloIPRanges, SoloNotIPRanges

def table(ACLString):
	table_string=Table()
	m = re.search(r'(?<=^(table))\s*([^\s]+)\s*({[^#]*})(.*)',ACLString)
	table_string.add_name(m.group(2))
	table_string.add_leftoveres(m.group(4))
	table_string.nets,table_string.notnets = IPStringTransform(m.group(3))
	print(table_string.name, table_string.nets,table_string.notnets, table_string.leftovers, sep='\n')
	return table_string

def IsIn(ip,List):
	for i in List:
		if isinstance(i,ipaddress.IPv4Network):
			if ip in i:
				return True
		else:
			for j in *i:
				if ip in j.nets and ip not in j.notnets:
					return True
		return False

	#else:


def MakeMeList(Str):
	'''
	принимает на вход строку c ip и именами table
	выдает список IPNetwork и имен table
	'''
	Str = Str.replace('}','')
	Str = Str.replace('{','')
	Str = Str.replace(',','')
	StrList = Str.split()
	for item in range(len(StrList)):
		try:
			StrList[item] = ipaddress.ip_network(StrList[item])
			#print(StrList[item])
		except ValueError:
			
			print('Error')


	return StrList



fromto=r'(?<!#)(?:[^#]*)from\s+([^#{}\s]+|{[^#]+})\s+to\s+([^#{}\s]+|{[^#]+})'
with open('/home/damir/Python/files/pf.conf.oneline','r',encoding= 'utf-8', errors='ignore') as inpt:
	TabList={}
	
	for ACLString in inpt:#read the file line by line
		ACLString = ACLString.rstrip()
		
		if re.search(r'(?<=^table)\s*([^\s#]+)\s*(?=[^#])([^#]*)(?=#|$)',ACLString)!=None:#searching for acl tables
			#print(ACLString)
			obj = re.search(r'(?<=^table)\s*([^\s#]+)\s*(?=[^#])([^#]*)(?=#|$)', ACLString)
			TabList[obj.group()1] = obj.group(2)
			

		elif re.search(fromto, ACLString)!=None:
			#print(ACLString)
			m = re.match(fromto, ACLString)
			From = m.group(1)
			To = m.group(2)
			#print(From)#from
			#print(To)#to
			if From == 'any' or To == 'any':
				print(ACLString)
			else:
				



			#FinalList = IPStringTransform(ACLString)
			#print(FinalList.nets)
			#print(FinalList.notnets)
			#if any(map(lambda x: IPCheck in x,FinalList)):
			#	m=re.search(r'(?<=^acl)\s*([^\s]+)\s*(?=src)',ACLString)
			#	ListName.append(m.group(1))#add the name of acl
			#	#print(ListName)
