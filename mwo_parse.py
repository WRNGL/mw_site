import requests, urllib2, re, sqlite3, getpass
from urllib import urlopen


LOGIN_URL = 'https://mwomercs.com/do/login'

login_data = {
	'email':raw_input('Enter email: '),
	'password':getpass.getpass('Enter password:'),
	'submit':'login'
}

session = requests.session()
session.post(LOGIN_URL, data=login_data)
req_basestats = session.get('https://mwomercs.com/profile/stats?type={0}')
# req.content

def GetName():
	req_nickname = session.get('https://mwomercs.com/profile')
	start_tag = '<h1>'
	end_tag = '</h1>'
	start_index = req_nickname.content.find(start_tag) + len(start_tag)
	end_index = req_nickname.content.find(end_tag)
	return req_nickname.content[start_index:end_index]

def GetBaseStats():
	req_basestats = session.get('https://mwomercs.com/profile/stats?type={0}')
	start_tag = '<tbody>'
	end_tag = 'Death Ratio'
	start_index = req_basestats.content.find(start_tag)
	end_index = req_basestats.content.find(end_tag)
	text_raw = req_basestats.content[start_index:end_index].replace(',','')
	stat_list =  re.findall(r'\d+', text_raw)
	return stat_list

# def GetMechStats():

# def GetMapStats():


mah_list = GetBaseStats()
player = GetName()
mc = mah_list[0]
kill = mah_list[1]
death = mah_list[2]
cbills = mah_list[3]
exp = mah_list[4]
win = mah_list[5]
lose = mah_list[6]

winlose_values = (
	player, mc, kill, death, cbills, exp, win, lose
	)

connection = sqlite3.connect('mwo.db')
c = connection.cursor()

c.execute("INSERT INTO BaseStats VALUES(?, ?, ?, ?, ?, ?, ?, ?)", winlose_values)
connection.commit()
print 'All your stats are belong to us, ',player, '!' 