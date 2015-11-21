import requests, urllib2, re, sqlite3, getpass
from urllib import urlopen
from datetime import datetime, date

def Killz(shit):
	start_tag = '<tbody>'
	end_tag = 'Death Ratio'
	start_index = shit.find(start_tag)
	end_index = shit.find(end_tag)
	text_raw = shit[start_index:end_index].replace(',','')
	stat_list =  re.findall(r'\d+', text_raw)
	return stat_list[1]

# def GetMechStats():

# def GetMapStats():

'''
mah_list = GetBaseStats()
player = GetName()
mc = mah_list[0]
kill = mah_list[1]
death = mah_list[2]
cbills = mah_list[3]
exp = mah_list[4]
win = mah_list[5]
lose = mah_list[6]
tiem = datetime.now()
'''