
import requests
from bs4 import BeautifulSoup
import string 
import csv
import urllib
import decimal
import re
import numpy as np
import datetime
import time
import fileinput

t0 = time.time()

date_today = datetime.date.today()
day = date_today.day
month = date_today.month
year = date_today.year

Last_Game_Date = datetime.date(year, month, day)
Opening_Night_Date = datetime.date(2019, 6, 30)

#Last_Game_Date = most recent date of games
#Opening_Night_Date = first game of summer league 
# format: YEAR , MONTH , DAY

days = [Opening_Night_Date + datetime.timedelta(days=x) for x in range((Last_Game_Date-Opening_Night_Date).days + 1)]

SL_Data = []
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

#------------------------------------------------------------------------------------

for item in boxscore_URL_list:
	for i in boxscore_URL_code_list:
		if item.find(i) == 54:
			UNIQUE_URLs.append(item) #create list of unique URLs without Date (7/2/19 - this isn't actually unique)

UNIQUE_URLs = list(set(UNIQUE_URLs)) #this will convert the list --> set --> back to a list (and will make it only contain unique elements)

#------------------------------------------------------------------------------------

csv_file = open('NBA_Summer_League.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Date', 'Team', 'Opp', 'Pos', 'Mins', 'FGM', 'FGA', '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-', 'PTS', 'F.PTS'])

for i in UNIQUE_URLs:	
	p = requests.get(i)
	soup = BeautifulSoup(p.content, "html.parser")
	game_info  = soup.find_all("title")
	game_data  = soup.find_all('table')[1] # grabs first  table
	game_data1 = soup.find_all('table')[2] # grabs second table

	raw   = str(game_info).split('<title>')[1].split('</title>')[0].split('ESPN')[0]
	date  = raw.split('Score - ')[1].split(' -')[0]
	team  = raw.split(' vs.')[0]
	opp   = raw.split(' vs. ')[1].split(' -')[0]

	for i in game_data: # pulls 1st table data
		try:
			for item in i:
				try:
					name = str(item).split('class="name"><span>')[1].split('</span>')[0]
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
						ftm = "DNP"
						fta = "DNP"
					else:
						ft = ft.split('[<td class="ft">')[1].split("</td>]")[0]
						ft = re.sub("-","|",ft)
						ftm = ft[0:ft.find("|")]
						fta = ft[ft.find("|")+1:]
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
					if pts == "DNP":
						fps = "DNP"
					else:
						fps = (int(reb))*1.2+(int(ast)*1.5)+(int(stl)*3)+(int(blk)*3)-(int(to))+(int(pts))

					csv_writer.writerow([name, date, team, opp, pos, minutes, fgm, fga, treysM, treysA, ftm, fta, oreb, dreb, reb, ast, stl, blk, to, pf, plusminus, pts, fps])

				except:
					continue
		except:
			continue
	
	for i in game_data1: # pulls 2nd table data
		try:
			for item in i:
				try:
					name = str(item).split('class="name"><span>')[1].split('</span>')[0]
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
						ftm = "DNP"
						fta = "DNP"
					else:
						ft = ft.split('[<td class="ft">')[1].split("</td>]")[0]
						ft = re.sub("-","|",ft)
						ftm = ft[0:ft.find("|")]
						fta = ft[ft.find("|")+1:]
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
					if pts == "DNP":
						fps = "DNP"
					else:
						fps = (int(reb))*1.2+(int(ast)*1.5)+(int(stl)*3)+(int(blk)*3)-(int(to))+(int(pts))

					csv_writer.writerow([name, date, opp, team, pos, minutes, fgm, fga, treysM, treysA, ftm, fta, oreb, dreb, reb, ast, stl, blk, to, pf, plusminus, pts, fps])

				except:
					continue
		except:
			continue

csv_file.close()

#------------------------------------------------------------------------------------

seen = set() # set for fast O(1) amortized lookup
for line in fileinput.FileInput('NBA_Summer_League.csv', inplace=1): # This will resolve the dup problem --> looks in csv after it's created and consolidates w unique values
    if line in seen: continue # skip duplicate
    seen.add(line)
    print line, 

#------------------------------------------------------------------------------------

t1 = time.time()
total = t1-t0
print('Finished @ %ss' % (round(total,2)))






