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

The only constraint to this script are these lines of codes: 

LAST_DNP_INDICATION_PER_TEAM.insert(83,1248)
LAST_DNP_INDICATION_PER_TEAM.insert(143,2132)
LAST_DNP_INDICATION_PER_TEAM.insert(150,2232)
LAST_DNP_INDICATION_PER_TEAM.insert(170,2532)

These codes map the exact instances where there were no DNP instances - meaning that the Team list no longer would accurately
know when to change to the next team in the list without making a mistake
