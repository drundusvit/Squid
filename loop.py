
def Exclude(A,B):
	try:
		m = list(ipaddress.A.address_exclude(B))
		return m
	except ValueError:
		return A


def SubTract(pos, neg):
	Final = []
	for i in pos:
		rez = [i]
		for j in pos:
			rez = map(lambda x: Exclude(x,j), rez)
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
	
	rez = []
for i in FlatList:
	for j in NFlatList:
		try:
#			print(i)
#			print(j)
			rez.extend(list(i.address_exclude(j)))
		except ValueError:
			continue
