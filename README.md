# Recommending Steam Games
There are many... many games on the Steam platform that a user could purchase or download for free - from small, indie developers to the 15th game in a massive, popular series.  

The initial goal of this project is to create a recommender system based on a user's current played games to find new games they would like to spend time playing.  

There are a few questions we might want to know to recommend games to users:

Which games should you buy?  
If you buy a game, how long will you play it?  
Which games are most worth the money?  

There are many potential stakeholders who will get value from building such models.  Obviously this will benefit people who want to buy games that they will play a long time (we assume they probably enjoy such games).  Therefore, building a platform that recommends games very well has a lot of value.  The stakeholder who stands to gain the most would likely be Steam.  

# Why Recommend?
Research has shown that when users have too many choices they are less likely to
make a purchase.  
Recommendation has been proven to be valuable on major platforms -  
Netflix - 2 out of 3 of movies watched were recommended (2014)  
Amazon - 35% of sales from recommendations (2014)  

Good recommendations need a lot of data and Steam has it.  
2017 data showed Steam at 67 Million Monthly Active Users.  
According to data from 2014 there were 500 million played games on Steam, and according to Valve in 2015, there were about 125 million "Active" Steam accounts.  

# Offline evaluation of Recommenders
Offline evaluation of Recommender Systems is not as effective as A/B testing.  
So why evaluate offline?  
It forces us to set clear goals.  
We can confirm that there is enough data to make good recommendations.  
Constantly changing a model in production can confuse users.
After multiple experiments, we can start to see what the correlation is between
our offline metrics and improvements in metrics testing online.  



# Path To Success
We will start by predicting play times for the steam-200k dataset, removing a percent of real playtime data and measuring how well we can backfill it with predictions.
If there is time, we will fetch data from more users and games to improve the model.
Once we can recommend games well, we can start to look into whether attributes of the games or users are useful in making recommendations.  

# Data Pipeline
The basic dataset already exists as steam-200k.csv  
To add additional users to this dataset:
  Hit the API with some subset of user space not already in 200k
  Specifically hit 'IPlayerService/GetOwnedGames/v0001' steam API
  Add new row with steamid hit, 'appid', 'playtime_forever'  

# Data Science
Matrix factorization will be the key to reducing the dimensions of this problem.  
We will use the ALS algorithm built into SparkML for the collaborative filtering.  

# Potential Problems
Cold start - We can't say new users or the games they play makes them similar to someone / something else because we have no data on them.  We can overcome this with general, popular recommendations.  
Our initial model does not take time into account because it does not have timestamps.  
The recommendations should be fast for an individual user.  
Old data might be much less useful than data on games within the last couple years.  
User preferences might change - if someone plays many games but then disappears for a long time, the Cold Start issue may return to some extent.  

# Data Overview
See data/data_overview.md

# Data Sources
Kaggle 200k dataset:
https://www.kaggle.com/tamber/steam-video-games/data
Valve's official API:
https://developer.valvesoftware.com/wiki/Steam_Web_API#GetUserStatsForGame_.28v0002.29
Base game recommendations for new users:
http://store.steampowered.com/stats/

# Libraries
SparkML
GraphLab
Pandas
Matplotlib
