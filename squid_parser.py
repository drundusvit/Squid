


import os
import re
import ipaddress

def expand_ranges(IPRanges,ACLString):#функция дополняющая список объектов IPv4Address объектами и диапазонов адресов
	PatternRange = r'\b[0-9]+(?:\.[0-9]+){3}\s*-\s*[0-9]+(?:\.[0-9]+){3}\b'
	listrange = re.findall(PatternRange,ACLString)
	pattern = r'\b([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s*)-(\s*[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\b'
	for Var in listrange:
		m = re.match(pattern,Var)
		cand = list(ipaddress.summarize_address_range(ipaddress.IPv4Address(m.group(1)), ipaddress.IPv4Address(m.group(2))))
		IPRanges.extend(cand)
	ACLString = re.sub(pattern, r'',ACLString)
	return IPRanges, ACLString

def IPStringTransform(ACLString):#return list of IPv4Networks objects
	IPRanges=[]# Список для заполнения результатами парсинга
	PatternIp = r'\b[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+(?:/[0-9]+)?\b'#REG для ip адресов и сеток
#получить список диапазонов ip адресов
	IPRanges, ACLString = expand_ranges(IPRanges,ACLString)
	listip = re.findall(PatternIp,ACLString)#найти все одиночные ip и ip с масками
	SoloIPRanges = list(map(lambda x: ipaddress.ip_network(x), listip))#преобразовать в объекты IPv4Address
	IPRanges.extend(SoloIPRanges)
	return IPRanges

while True:
	try:
		IPCheck=ipaddress.ip_address(input('Please enter IP address to check: '))
	except ValueError:
		print('Please enter valid IP Address')
		continue
	break


with open('/media/damir/TOURO S/python3/acl.txt') as inpt:
	ListName=[]#list of all acl tables where the ip is located
	DSTDic={}
	https=[]
	for ACLString in inpt:#read the file line by line
		ACLString = ACLString.rstrip()
		#print(ACLString)
		if re.search(r'(?<=^acl)\s*([^\s]+)\s*(?=src)',ACLString)!=None:#searching for acl src tables
			FinalList = IPStringTransform(ACLString)
			#print(FinalList)
			if any(map(lambda x: IPCheck in x,FinalList)):
				m=re.search(r'(?<=^acl)\s*([^\s]+)\s*(?=src)',ACLString)
				ListName.append(m.group(1))#add the name of acl
				#print(ListName)
		elif re.search(r'(?<=^acl)\s+([^\s]+)\s+(?:dstdomain\s|dst\s)(.*)#?',ACLString)!=None:
			ml = re.search(r'(?<=^acl)\s+([^\s]+)\s+(?:dstdomain\s|dst\s)(.*)#?',ACLString)
			DSTDic[ml.group(1)] = ml.group(2).split()
		
		elif re.search(r'^\s*(?<!=\#)(http_access(?:\s+\w+)+)',ACLString)!=None:
			https.append(ACLString)
#		else:
#			print(ACLString)
#(lambda x: print(x,DSTDic[x],sep=' '),*DSTDic)
if len(ListName)!=0:
	rez={}
	print('The ip is in acls: ',ListName)#list of acl where IP is in
	for var in ListName:
		for string in https:
			#print('\b{}\b'.format(var))
			if re.search(r'\b{}(\b|$)'.format(var), string)!=None:
				num = https.index(string)
				string = re.sub(var,'\033[1m'+var+'\033[0m',string)
				rez[num]=string
			elif 'deny' in string:
				rez[https.index(string)]=string
	#print(rez)
	for i in sorted(rez):
		print(i,' ',rez[i])
		for opt in DSTDic:
			if re.search(r'\b{}(\b|$)'.format(opt),rez[i])!=None:
				print('\t',end='')
				print(opt, DSTDic[opt], sep=': ')
	#print('http_access deny stop_internet')
	#print('http_access deny all')
else:
	print('No match')

#print(https)

'''
with open('/media/damir/ECE0E74BE0E71A9A/drop/python/files/acl.txt') as inpt:
	if len(ListName)!=0:
		for ACLString in inpt:#read the file line by line
			ACLString = ACLString.rstrip()
			for var in ListName:#the cycle is inpenetrable if the list is empty
                               #print('1')
				if re.search(var,ACLString)!=None:#print acl line
					print(var)
					if re.search(r'(?<={})\s+(.+)'.format(var),ACLString)!=None:
						Domain = re.search(r'(?<={})\s+(.+)'.format(var),ACLString)
						Domain = Domain.group(1)
						print(var,DSTDic[Domain],sep=': ')
'''
#(ListName)!=0:#for other lines in the file
	#		for var in ListName:#the cycle is inpenetrable if the list is empty
	#			#print('1')
	#			if re.search(var,ACLString)!=None:#print acl line
	#				if re.search(r'(?<={})\s+(.+)'.format(var),ACLString)!=None:
#
#						Domain = re.search(r'(?<={})\s+(.+)'.format(var),ACLString)
#						Domain = Domain.group(1)
#						print(var,DSTDic[Domain],sep=': ')
#					else:
#						print(ACLString)
		#else:
			#print(ACLString)
	#print(DSTDic)
#FinalList = IPStringTransform(ACLString)
#print(FinalList)

	#To make list shorter
#testlist=[ipadr for ipadr in ipaddress.collapse_addresses(IPRanges)]
#print(len(testlist))
#print(*map(lambda x: x, testlist),sep=' ')
