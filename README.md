# NBA-Summer-League
NBA Summer League Game Scraper

	
There are two date inputs for the script:
Last_Game_Date = datetime.date(year, month, day) # aka end date
Opening_Night_Date = datetime.date(2019, 7, 2)   # aka start date

Once you've established this, execute the script and it will create a CSV file
that includes data for each player and game played across the predefined date range.
The 23 fields below are included and will be formatted horizontally.

'Name', 
'Date', 
'Team', 
'Opp', 
'Pos', 
'Mins', 
'FGM', 
'FGA', 
'3PM', 
'3PA', 
'FTM', 
'FTA', 
'OREB', 
'DREB', 
'REB', 
'AST', 
'STL', 
'BLK', 
'TOV', 
'PF', 
'+/-', 
'PTS', 
'F.PTS'
