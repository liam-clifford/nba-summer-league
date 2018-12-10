# nba-summer-league
NBA Summer League Game Scraper

Two important inputs that currently have to stay as follows are:
Last_Game_Date = datetime.date(2018, 7, 18)
Opening_Night_Date = datetime.date(2018, 7, 2)

Once you've established this, execute the script and it will create a CSV desktop file
with data stemming from all of the games play over this range, formatted like so: 
PLAYER / POS / MINS / FGM / FGA / TREYSM / TREYSA / OREB / DREB / REB / AST / STL / BLK / TO / PF / +- / PTS / TEAM / DATE / MATCHUP

Have fun with it in excel/your prefered choice for analytics!

Note - - - - - 

The only constraint to this script are these 4 lines of codes: 

LAST_DNP_INDICATION_PER_TEAM.insert(83,1248)
LAST_DNP_INDICATION_PER_TEAM.insert(143,2132)
LAST_DNP_INDICATION_PER_TEAM.insert(150,2232)
LAST_DNP_INDICATION_PER_TEAM.insert(170,2532)

Since the data is pulling directly from ESPN, these 4 lines are accounting for the few instances where there was data associated to a team that had all their players participate in a game. 

The reason this is worth mentioning is because the script relies on the assumption that, for every summer league game played, each team had at least one player not play- which would be represented as 'DNP' on the ESPN webpage. The reason this assumption was made was because, within the html structure of the webpage, their was no 'Team' tag that I was able to loop over and associate to the players in my dataset. 

In short, by not having the 'Team' tag conveniently accesable to scrape, I used the indice of the last player on a team who did not play (aka had a 'DNP') as a reference point to tell my script that the next player belonged to the next team. 
