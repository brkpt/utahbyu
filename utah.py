import requests
from bs4 import BeautifulSoup
import requests
import re

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
site = 'http://www.sports-reference.com'
schoolsPage = 'cfb/schools'

class Team(object):
	def __init__(self, name, wins, losses):
		self.name = name
		self.wins = wins
		self.losses = losses

class Game(object):
	def __init__(self, opponent, date, winloss, pointsFor, pointsAgainst):
		self.opponent = opponent
		self.date = date
		self.winLoss = winloss
		self.pointsFor = pointsFor
		self.pointsAgainst = pointsAgainst

teamHistory = {}

def makeLink(path):
	return site + path

def getTeamUrls():
	url = site + '/' + schoolsPage

	school_urls = {}
	schools_html = requests.get(url, headers = header)
	school_bs = BeautifulSoup(schools_html.text, 'html.parser')
	schools_table = school_bs.find(id='schools')
	teams_tbody = schools_table.find('tbody')
	for schoolRow in teams_tbody.find_all('tr', class_=None):
		cols = schoolRow.find_all('td')
		schoolLink = cols[0].find('a')
		school = schoolLink.text
		link = makeLink(schoolLink.get('href'))
		school_urls[school] = link
	return school_urls

def getRecordsForTeam(links,team):
	history={}
	url = urls[team]
	team_html = requests.get(url, headers = header)

	team_bs = BeautifulSoup(team_html.text, 'html.parser')
	team_table = team_bs.find('div', id='all_utah')
	team_tbody = team_table.find('tbody')
	for yearRow in team_tbody.find_all('tr', class_=None):
		col = yearRow.find_all('td')
		year=col[0].text
		wins=col[2].text
		losses=col[3].text
		history[year] = Team('Utah', wins,losses)
	return history

def getScheduleForTeamAndYear(links, team, year):
	schedule=[]
	url = urls[team]+str(year)+'-schedule.html'
	schedule_html = requests.get(url, headers=header)
	schedule_bs = BeautifulSoup(schedule_html.text, 'html.parser')
	schedule_table = schedule_bs.find('table', id='schedule')
	schedule_tbody = schedule_table.find('tbody')
	if schedule_tbody:
		for gameRow in schedule_tbody.find_all('tr'):
			cols = gameRow.find_all('td')
			if cols[0].find('a') == None:
				date = cols[0].text
			else:
				date = cols[0].find('a').text
			time = cols[1].text
			if cols[4].find('a') == None:
				opponent = cols[5].text
			else:
				opponent = cols[5].find('a').text
			opponent = re.sub(r'\([0-9]+\)', r'',opponent).strip()
			winLoss = cols[7].text
			pointsFor = cols[8].text
			pointsAgainst = cols[9].text
			schedule.append(Game(opponent,date,winLoss,pointsFor,pointsAgainst))
	return schedule

#import pdb; pdb.set_trace()
urls = getTeamUrls()

teamRecords=getRecordsForTeam(urls,'Utah')
teamHistory['Utah'] = teamRecords
#foo = getScheduleForTeamAndYear(urls, 'Utah', 2016)
#for g in foo:
#	print(g.opponent+'|'+g.date+'|'+g.winLoss+'|'+g.pointsFor+'|'+g.pointsAgainst)

for k in teamHistory['Utah']:
	print(k)
	sched = getScheduleForTeamAndYear(urls, 'Utah', k)
	for g in sched:
		print(g.opponent+'|'+g.date+'|'+g.winLoss+'|'+g.pointsFor+'|'+g.pointsAgainst)


