
import requests
from bs4 import BeautifulSoup
import string 
import csv
import urllib
import decimal
import re
import numpy as np
import datetime

date_today = datetime.date.today()
day = date_today.day
month = date_today.month
year = date_today.year

Last_Game_Date = datetime.date(2018, 7, 18)
Opening_Night_Date = datetime.date(2018, 7, 2)

#Last_Game_Date = most recent date of games
#Opening_Night_Date = first game of summer league 
# format: YEAR , MONTH , DAY

days = [Opening_Night_Date + datetime.timedelta(days=x) for x in range((Last_Game_Date-Opening_Night_Date).days + 1)]

FINAL_DATA = [] # cleans up the FINAL_RAW_DATA list so that is doesn't contain DNP's or other mal data
FINAL_RAW_DATA = [] # gets every piece of data in a list, but still contains mal data
GAME_DETAILS = [] # uses a helper function to create a list of game details (x2)
UPPER_BOUND_list = [] # REPEATS BASED ON difference between [CURRENT ITEM IN LIST - PREVIOUS ITEM IN LIST]
LOWER_BOUND_list = [] # REPEATS BASED ON difference between [NEXT ITEM IN LIST - CURRENT ITEM IN LIST]
FINAL_TEAM_LIST = [] # team list with index
TEAM_INDEX_LIST = [] # teams + index within list
FINAL_PLAYER_DATA = [] # new and improved list of players with index value at end
LIST_NUMBER = [] # helps get the index value printed next to data points
LAST_DNP_INDICATION_PER_TEAM = [] # last index instance of DNP by TEAM
EVERY_DNP_OCCURANCE = [] # index of ALL player who were DNP's
RAW_PLAYER_DATA = [] # raw player data
RAW_TEAMS_LIST = [] # teams
UNIQUE_URLs = [] # unique URL list
DUPLICATE_URLs = [] # Duplicate URL list
URL_CODE_LIST = [] # URL code list

for i in days:
	try:
		month = i.month
		day = i.day
		year = i.year

		if month < 10:
			month = "0" + str(month)
		else:
			month = month

		if day < 10:
			day = "0" + str(day)
		else:
			day = day	

		date = "{}".format(year) + "/" + "{}".format(month) + "/" + "{}".format(day)

		p = requests.get("http://www.espn.com/nba-summer-league/scoreboard/_/date/" + "{}".format(year) + "{}".format(month) + "{}".format(day))
		soup = str(BeautifulSoup(p.content, "html.parser"))
		
		for i in range(0,1000):
			try:
				boxscore_URL = soup.split("http://www.espn.com/nba-summer-league/")[i].split("text")[0]
				boxscore_URL = re.sub(',"',"",boxscore_URL)
				boxscore_URL = re.sub('"',"",boxscore_URL)
				if "boxscore?gameId" in boxscore_URL:
					boxscore_URL = "http://www.espn.com/nba-summer-league/" + boxscore_URL	
				
					boxscore_URL_code = boxscore_URL[54:63]
					DUPLICATE_URLs.append(boxscore_URL_code)
					boxscore_URL_code_list = list(set(DUPLICATE_URLs))	#list with boxscore URL CODES
					
					URL_CODE_LIST.append(boxscore_URL)
					boxscore_URL_list = list(set(URL_CODE_LIST)) #list with boxscore URL only

			except:
				continue
	except:
		continue

for item in boxscore_URL_list:
	for i in boxscore_URL_code_list:
		if item.find(i) == 54:
			UNIQUE_URLs.append(item) #create list of unique URLs without Date

def gamedetails(i): # helper function that pulls the date and teams playing
	try:
		p = requests.get(i)
		soup = BeautifulSoup(p.content, "html.parser")
		data = soup.find_all("title")
		for item in data:
			date = str(item).split('<title>')[1].split('</title>')[0].split('ESPN')[0]
			date = re.sub(" Box Score - "," ",date).split("-")[1]
			date = re.sub(" ","",date)
			date = re.sub(",2018","",date)
			matchup = str(item).split('<title>')[1].split('</title>')[0].split('ESPN')[0]
			matchup = re.sub(" Box Score - "," ",matchup).split("-")[0]
			matchup = re.sub(" ","",matchup)
			matchup = re.sub("vs.","|",matchup)
			gamedetails = date + " " + matchup
			gamedetails = np.repeat(gamedetails, 2) # this has to be repeated twice bc it's going to be looped through the DNP list
			return gamedetails 
	except:
		return
	
for i in UNIQUE_URLs:	
	x = gamedetails(i)
	GAME_DETAILS.extend(gamedetails(i))


for i in UNIQUE_URLs:
	p = requests.get(i)

	soup = BeautifulSoup(p.content, "html.parser")
	data = soup.find_all("tr")

	soup1 = BeautifulSoup(p.content, "html.parser")
	data1 = soup.find_all("div", {"class": "team-name"})

	for item in data:
		try:		
			name = str(item.find_all("td",{"class": "name"}))
			if name == '[]':
				continue
			else:
				name = name.split('[<td class="name"><span>')[1].split("</span>")[0]	
				name = re.sub(" ","",name)
			pos = str(item.find_all("span",{"class": "position"}))
			if pos == '[]':
				pos = "NA"
			else:
				pos = pos.split('[<span class="position">')[1].split("</span>]")[0]
			minutes = str(item.find_all("td",{"class": "min"}))
			if minutes == '[]':
				minutes = "DNP"
			else:
				minutes = minutes.split('[<td class="min">')[1].split("</td>]")[0]
			fg = str(item.find_all("td",{"class": "fg"}))
			if fg == '[]':
				fg = "DNP"
				fgm = "DNP"
				fga = "DNP"
			else:
				fg = fg.split('[<td class="fg">')[1].split("</td>]")[0]
				fg = re.sub("-","|",fg)
				fgm = fg[0:fg.find("|")]
				fga = fg[fg.find("|")+1:]
			treys = str(item.find_all("td",{"class": "3pt"}))
			if treys == '[]':
				treys = "DNP"
				treysM = "DNP"
				treysA = "DNP"
			else:
				treys = treys.split('[<td class="3pt">')[1].split("</td>]")[0]
				treys = re.sub("-","|",treys)
				treysM = treys[0:treys.find("|")]
				treysA = treys[treys.find("|")+1:]
			ft = str(item.find_all("td",{"class": "ft"}))
			if ft == '[]':
				ft = "DNP"
			else:
				ft = ft.split('[<td class="ft">')[1].split("</td>]")[0]
			oreb = str(item.find_all("td",{"class": "oreb"}))
			if oreb == '[]':
				oreb = "DNP"
			else:
				oreb = oreb.split('[<td class="oreb">')[1].split("</td>]")[0]
			dreb = str(item.find_all("td",{"class": "dreb"}))
			if dreb == '[]':
				dreb = "DNP"
			else:
				dreb = dreb.split('[<td class="dreb">')[1].split("</td>]")[0]
			reb = str(item.find_all("td",{"class": "reb"}))
			if reb == '[]':
				reb = "DNP"
			else:
				reb = reb.split('[<td class="reb">')[1].split("</td>]")[0]
			ast = str(item.find_all("td",{"class": "ast"}))
			if ast == '[]':
				ast = "DNP"
			else:
				ast = ast.split('[<td class="ast">')[1].split("</td>]")[0]
			stl = str(item.find_all("td",{"class": "stl"}))
			if stl == '[]':
				stl = "DNP"
			else:
				stl = stl.split('[<td class="stl">')[1].split("</td>]")[0]
			blk = str(item.find_all("td",{"class": "blk"}))
			if blk == '[]':
				blk = "DNP"
			else:
				blk = blk.split('[<td class="blk">')[1].split("</td>]")[0]
			to = str(item.find_all("td",{"class": "to"}))
			if to == '[]':
				to = "DNP"
			else:
				to = to.split('[<td class="to">')[1].split("</td>]")[0]
			pf = str(item.find_all("td",{"class": "pf"}))
			if pf == '[]':
				pf = "DNP"
			else:
				pf = pf.split('[<td class="pf">')[1].split("</td>]")[0]
			plusminus = str(item.find_all("td",{"class": "plusminus"}))
			if plusminus == '[]':
				plusminus = "DNP"
			else:
				plusminus = plusminus.split('[<td class="plusminus">')[1].split("</td>]")[0]
			pts = str(item.find_all("td",{"class": "pts"}))
			if pts == '[]':
				pts = "DNP"
			else:
				pts = pts.split('[<td class="pts">')[1].split("</td>]")[0]
			RAW_PLAYER_DATA.append(name + " " + pos + " " + minutes + " " + fgm + " " + fga + " " + treysM + " " + treysA + " " + oreb + " " + dreb + " " + reb + " " + ast + " " + stl + " " + blk + " " + to + " " + pf + " " + plusminus + " " + pts)
	
		except:
			continue

	for i in data1:
		try:
			team = str(i).split('title=')[1].split('>')[1].split('<')[0]
			RAW_TEAMS_LIST.append(team) # creates list of teams
		except:
			continue

for item in range(0,len(RAW_PLAYER_DATA)):
	LIST_NUMBER.append(item) # get the real index value of each data point

for i in range(0,len(RAW_PLAYER_DATA)):
	try:
		data = str(LIST_NUMBER.index(i)) + "* " + RAW_PLAYER_DATA[i]
		FINAL_PLAYER_DATA.append(data)
	except:
		continue 

for item in range(0,len(RAW_TEAMS_LIST)):
	TEAM_INDEX_LIST.append(item) # get the real index value of each data point (for teams)

for i in range(0,len(RAW_TEAMS_LIST)):
	try:
		data = RAW_TEAMS_LIST[i] + "," + str(TEAM_INDEX_LIST.index(i))
		FINAL_TEAM_LIST.append(data) # team + index value
	except:
		continue

DNP = (item for item,x in enumerate(RAW_PLAYER_DATA) if x.find("DNP") != -1)
for item in DNP:
	EVERY_DNP_OCCURANCE.append(item) # catelog all instances of the players who were DNP's

for i in range(0,max(EVERY_DNP_OCCURANCE)):
	try:
		if EVERY_DNP_OCCURANCE[i] - EVERY_DNP_OCCURANCE[i+1] != -1:
			EVERY_DNP_OCCURANCE[i] = EVERY_DNP_OCCURANCE[i] + 1
			LAST_DNP_INDICATION_PER_TEAM.append(int(EVERY_DNP_OCCURANCE[i])) # find all instances of DNP's, but only list the last instance per team
	except:
		continue

LAST_DNP_INDICATION_PER_TEAM.insert(83,1248)
LAST_DNP_INDICATION_PER_TEAM.insert(143,2132)
LAST_DNP_INDICATION_PER_TEAM.insert(150,2232)
LAST_DNP_INDICATION_PER_TEAM.insert(170,2532)

# 4 lines above included to account for the groups of teams that didn't have a DNP indicator

LAST_DNP_INDICATION_PER_TEAM.insert(max(LAST_DNP_INDICATION_PER_TEAM)+1,max(LAST_DNP_INDICATION_PER_TEAM)+20) # puts 'out of range number' at end of list / closes the list by adding one last DNP indicator so that loop won't go out of index

for i in LAST_DNP_INDICATION_PER_TEAM:
	try:
		if i == LAST_DNP_INDICATION_PER_TEAM[0]: # adjust based on first index item in list
			repeats = np.repeat(i, LAST_DNP_INDICATION_PER_TEAM[LAST_DNP_INDICATION_PER_TEAM.index(i)+1])
		else:
			repeats = np.repeat(i,LAST_DNP_INDICATION_PER_TEAM[LAST_DNP_INDICATION_PER_TEAM.index(i)+1]-LAST_DNP_INDICATION_PER_TEAM[LAST_DNP_INDICATION_PER_TEAM.index(i)]) # REPEATS BASED ON [NEXT ITEM IN LIST - CURRENT ITEM IN LIST]
		LOWER_BOUND_list.extend(repeats) 
	except:
		continue

for i in LAST_DNP_INDICATION_PER_TEAM:
	try:
		if i == LAST_DNP_INDICATION_PER_TEAM[0]: # adjust based on first index item in list
			repeats = np.repeat(i,i)
		else:
			repeats = np.repeat(i,LAST_DNP_INDICATION_PER_TEAM[LAST_DNP_INDICATION_PER_TEAM.index(i)]-LAST_DNP_INDICATION_PER_TEAM[LAST_DNP_INDICATION_PER_TEAM.index(i)-1]) # REPEATS BASED ON [CURRENT ITEM IN LIST - PREVIOUS ITEM IN LIST]
		UPPER_BOUND_list.extend(repeats)
	except:
		continue

for item in FINAL_PLAYER_DATA:
	try:
		PLAYER_INDEX = FINAL_PLAYER_DATA.index(item)
		UPPER_BOUND = UPPER_BOUND_list[FINAL_PLAYER_DATA.index(item)]
		LOWER_BOUND = LOWER_BOUND_list[FINAL_PLAYER_DATA.index(item)]

		if UPPER_BOUND - LOWER_BOUND == 0: 
			data = item + " " + FINAL_TEAM_LIST[0]
			data = data.split(',')[0] # get rid of team index

		elif LOWER_BOUND <= PLAYER_INDEX < UPPER_BOUND:
			data = item + " " + FINAL_TEAM_LIST[LAST_DNP_INDICATION_PER_TEAM.index(UPPER_BOUND_list[FINAL_PLAYER_DATA.index(item)])] # this is where the good stuff happens 
			data = data.split(',')[0] # get rid of team index
		
		else:
			continue	
	except:
		continue
	FINAL_RAW_DATA.append(data)

for i in FINAL_RAW_DATA:
	try:
		PLAYER_INDEX = FINAL_RAW_DATA.index(i)
		UPPER_BOUND = UPPER_BOUND_list[FINAL_RAW_DATA.index(i)]
		LOWER_BOUND = LOWER_BOUND_list[FINAL_RAW_DATA.index(i)]

		if UPPER_BOUND - LOWER_BOUND == 0: 
			data = i + " " + GAME_DETAILS[0] # this only applies to the 0 index value from the last DNP instance list
		elif LOWER_BOUND <= PLAYER_INDEX < UPPER_BOUND:	
			data = i + " " + GAME_DETAILS[LAST_DNP_INDICATION_PER_TEAM.index(UPPER_BOUND_list[FINAL_RAW_DATA.index(i)])] # same approach to how I solved how to determine when to iterate over the team list
		else:
			continue	
	except:
		continue
	FINAL_DATA.append(data)

csv_file = open('NBA_Summer_League.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name pos minutes fgm fga treysm treysa oreb dreb reb ast stl blk to pf plusminus pts team date matchup'])

for item in FINAL_DATA:
	if ((item.find("--") == -1) and (item.find("DNP") == -1)): # if there's bad data, skip over and QA the good data
		data = item
		data = data.split('* ')[1] # get rid of list number (from player index)
	else:
		continue
	csv_writer.writerow([data])
csv_file.close()








