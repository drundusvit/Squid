
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

    def add_name(self,string):
    	self.name=string