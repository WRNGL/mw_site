import requests, urllib2, re, time
from urllib import urlopen

session = requests.session()

def BaseStats():
	req_basestats = session.get('http://team.alpha-legion.pro/profile.html')
	start_tag = '<tbody>'
	end_tag = 'Death Ratio'
	start_index = req_basestats.content.find(start_tag)
	end_index = req_basestats.content.find(end_tag)
	text_raw = req_basestats.content[start_index:end_index].replace(',','')
	stat_list =  re.findall(r'\d+', text_raw)
	#return stat_list[1]
	print req_basestats.content.find(start_tag)
	print stat_list[1]

print BaseStats()





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


winlose_values = (
	player, mc, kill, death, cbills, exp, win, lose, tiem
	)
 
'''