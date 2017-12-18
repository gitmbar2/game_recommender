# Recommending Steam Games
There are many... many games on the Steam platform that a user could purchase or download for free - from small, indie developers to the 15th game in a massive, popular series.

The initial minimum goal of this project is to create a recommender system based on a user's current played games to find new games they would like to spend time playing.

There are a few questions we might want to know to recommend games to users:

Which games should you buy?
If you buy a game, how long will you play it?
Which games are most worth the money?

There are many potential stakeholders who will get value from building such models.  Obviously this will benefit people who want to buy games that they will play a long time (we assume they probably enjoy such games).  Therefore, building a platform that recommends games very well has a lot of market value.  The stakeholder who stands to gain the most would probably be Steam - depending on how games are recommended.

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
Matrix factorization will be the key to reducing the feature dimensions for this problem.
One of the next steps will be deciding whether to recommend based on User-User similarity or Game-Game similarity.  According to data from 2014 there were 500 million played games on Steam, and according to Valve in 2015, there were about 125 million "Active" Steam accounts.

# Potential Problems
Cold start - We can't say new users or the games they play makes them similar to someone / something else because we have no data on them.  We can overcome this with general, popular recommendations.
We are not sure if users are randomly distributed - Would need to contact Steam or see if user distribution by id can be found somewhere online.
The recommendations are not generalizable to users whose profiles are not public.
Data sparsity means we need to choose how we recommend carefully.
The recommendations should be fast for an individual user, and this may sacrifice some recommendation power.
Old data might be much less useful than data on games within the last couple years.
User preferences might change - if someone plays many games but then disappears for a long time, the Cold Start issue may return to some extent.
Getting additional data:
  According to a 2014 survey, 781 million registered games had never been played at all, while 493 million have been played.  There will have to be some cleaning of data to make sure the games and users are relevant to the recommendations.

# Data Overview
See data/data_overview.md

# Data Sources
Kaggle 200k dataset:
https://www.kaggle.com/tamber/steam-video-games/data
Valve's official API:
https://developer.valvesoftware.com/wiki/Steam_Web_API#GetUserStatsForGame_.28v0002.29
Base game recommendations for new users:
http://store.steampowered.com/stats/

# Ideal additional data
How much money does a user spend on an in-game store etc
  (What is the true dollar cost of a game)

# Libraries
GraphLab's factorization recommender might be used
