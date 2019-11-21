import requests
import praw
from bs4 import BeautifulSoup
import pandas as pd

class bot:
    """A reddit moderation bot designed for the 12thman subreddit.
    """
    def __init__(self):
        self.api_key = get_api()
        self.reddit = praw.Reddit(client_id=self.api_key[0].strip(), client_secret=self.api_key[1].strip(), user_agent='A moderation bot for /r/12thman', username=self.api_key[2].strip(), password=self.api_key[3].strip())
        self.sports = ['football','mens-basketball','baseball','mens-track-and-field','volleyball','womens-basketball','equestrian','womens-track-and-field','womens-soccer','mens-soccer']
        def get_api():

            with open('api_keys.txt','r') as file:
                data = [x.strip() for x in file.readlines()]
            return data

    def get_schedules(self):
        """Update scores for defined sports
        
        Returns:
            dict -- a dictionary of dataframes with individual sports as the keys
        """
        urls = self.sports

        dataframes = {}
        for sport in urls:
            url = f'https://12thman.com/sports/{sport}/schedule'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            dates = soup.find_all(class_='sidearm-schedule-game-opponent-date')
            opp = soup.find_all(class_='sidearm-schedule-game-opponent-name')
            result = soup.find_all(class_='sidearm-schedule-game-result')
            dates = [' '.join(x.stripped_strings) for x in dates]
            opp = [' '.join(x.stripped_strings) for x in opp]
            results = [' '.join(x.stripped_strings) for x in result]
            while len(results) < len(opp):
                results.append('TBD')
            dataframes[sport] = pd.DataFrame([dates, opp, results], index=['Date','Opponent','Result'])

        return dataframes