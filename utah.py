import requests
from bs4 import BeautifulSoup
import requests
import re
import getopt,sys

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
	offsets =  [ 
		{	# Without time column
			"date": 0,
			"opponent": 4,
			"winLoss": 6,
			"pointsFor": 7,
			"pointsAgainst": 8
		},
		{	# With time colulmn
			"date": 0,
			"time": 1,
			"opponent": 5,
			"winLoss": 7,
			"pointsFor": 8,
			"pointsAgainst": 9 
		}
	]

	schedule=[]
	url = urls[team]+year+'-schedule.html'
	schedule_html = requests.get(url, headers=header)
	schedule_bs = BeautifulSoup(schedule_html.text, 'html.parser')
	schedule_table = schedule_bs.find('table', id='schedule')
	schedule_tbody = schedule_table.find('tbody')
	schedule_thead = schedule_table.find('thead')
	tableHeader = schedule_thead.find('tr')
	headerCols = tableHeader.find_all('th')
	dataOffsets = offsets[1] if headerCols[2].text == 'Time' else offsets[0]
	if schedule_tbody:
		for gameRow in schedule_tbody.find_all('tr'):
			cols = gameRow.find_all('td')
			if cols[dataOffsets['date']].find('a') == None:
				date = cols[dataOffsets['date']].text
			else:
				date = cols[dataOffsets['date']].find('a').text
			if cols[dataOffsets['opponent']].find('a') == None:
				opponent = cols[dataOffsets['opponent']].text
			else:
				opponent = cols[dataOffsets['opponent']].find('a').text
			opponent = re.sub(r'\([0-9]+\)', r'',opponent).strip()
			winLoss = cols[dataOffsets['winLoss']].text
			pointsFor = cols[dataOffsets['pointsFor']].text
			pointsAgainst = cols[dataOffsets['pointsAgainst']].text
			schedule.append(Game(opponent,date,winLoss,pointsFor,pointsAgainst))
	return schedule

def usage() :
    print("This is my usage")

#import pdb; pdb.set_trace()

print('Starting:')
try:
    opts, args = getopt.getopt(sys.argv[1:], 'hy:t:')
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(1)

options = {}

try:
    for o,a in opts:
        if o == '-h':
            usage()
            sys.exit(1)
        elif o == '-y':
            options['year'] = a
        elif o == '-t':
            options['team'] = a
        else:
            print('why is this here?')

except ValueError as err:
    print str(err)
    usage()
    sys.exit(1)

print('getting urls')
urls = getTeamUrls()

if 'team' in options and not 'year' in options:
    print('team: '+options['team'])
if 'year' in options and not 'team' in options:
    print('year: '+options['year'])
if 'year' in options and 'team' in options:
    print('team: '+options['team']+' in '+options['year'])
    teamInfo = {}
    teamInfo[options['team']]=getRecordsForTeam(urls,options['team'])
    teamInfo[options['team']]['results'] = {}
    teamInfo[options['team']]['results'] = getScheduleForTeamAndYear(urls, options['team'],options['year'])
    for g in teamInfo[options['team']]['results']:
	print(g.opponent+'|'+g.date+'|'+g.winLoss+'|'+g.pointsFor+'|'+g.pointsAgainst)

#for g in foo:
#	print(g.opponent+'|'+g.date+'|'+g.winLoss+'|'+g.pointsFor+'|'+g.pointsAgainst)
#
#for k in teamHistory['Utah']:
#	print(k)
#	sched = getScheduleForTeamAndYear(urls, 'Utah', k)
#	for g in sched:
#		print(g.opponent+'|'+g.date+'|'+g.winLoss+'|'+g.pointsFor+'|'+g.pointsAgainst)


