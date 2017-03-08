import requests
from bs4 import BeautifulSoup
import requests

class Year(object):

	def __init__(self, wins, losses):
		self.wins = wins
		self.losses = losses

years={}

url = 'http://www.sports-reference.com/cfb/schools/utah/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
utah_html = requests.get(url, headers = header)

utah_bs = BeautifulSoup(utah_html.text, 'html.parser')
utah_table = utah_bs.find('div', id='all_utah')
#import pdb; pdb.set_trace()
utah_tbody = utah_table.find('tbody')
for yearRow in utah_tbody.find_all('tr', class_=None):
	col = yearRow.find_all('td')
	year=col[0].text
	wins=col[2].text
	losses=col[3].text
	print(year+'|'+wins+'|'+losses)
	years[year] = Year(wins,losses)

#print('2016: '+years['2016'].wins)
for k,v in years.iteritems():
	print(k+': '+v.wins+','+v.losses)


