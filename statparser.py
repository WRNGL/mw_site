import requests, urllib2, re, sqlite3, getpass
from urllib import urlopen
from datetime import datetime, date

def Statz(stat_data):
	if '<html>' in stat_data:
		start_tag = '<tbody>'
		end_tag = 'Death Ratio'
		start_index = stat_data.find(start_tag)
		end_index = stat_data.find(end_tag)
		text_raw = stat_data[start_index:end_index].replace(',','')
		stat_list =  re.findall(r'\d+', text_raw)
		return stat_list
	else:
		start_tag = 'MechWarrior Credits'
		end_tag = 'HOME'
		start_index = stat_data.find(start_tag)
		end_index = stat_data.find(end_tag)
		text_raw = stat_data[start_index:end_index].replace(',','')
		stat_list =  re.findall(r'\d+', text_raw)
		return stat_list

'''
	start_tag = '<tbody>'
	end_tag = 'Death Ratio'
	start_index = stat_data.find(start_tag)
	end_index = stat_data.find(end_tag)
	text_raw = stat_data[start_index:end_index].replace(',','')
	stat_list =  re.findall(r'\d+', text_raw)
	return stat_list

# not used
def TextStatz(text_data):
	start_tag = 'MechWarrior Credits'
	end_tag = 'HOME'
	start_index = req_basestats.find(start_tag)
	end_index = req_basestats.find(end_tag)
	text_raw = req_basestats[start_index:end_index].replace(',','')
	stat_list =  re.findall(r'\d+', text_raw)
	return stat_list
'''