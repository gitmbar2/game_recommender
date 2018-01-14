We should build a recommender system, but if the user is in cold start phase, we can instead recommend them the most popular items, or weight popularity with a weak recommendation.  


Adjust for bias?  Games that are always highly rated; people who always rate high/low.

Consider users and games with less than n ratings from model or games/users with many many ratings and how they impact the model training.  

We are considering time playing a rating metric, but it could also be considered implicit.

Normalize for games that people play longer on average?

Graph improvements with more data.

Recommend something to deal with cold start.

Compare to recommending most popular games

# FROM NOTEBOOK

cumulative survivorship score?  
removing users with 5+ games but no games outside of bucket 1 (affects item clustering)
    - going further, remove all users who rate everything the same
maybe remove gamers with 100+ games (also affects item clustering)  
normalize to users instead of games (does ALS model adjust for user bias?)  
Split train/val/test based on time - test on most recent.  What about preference shift?  
Must do - Site papers.  

Add data from 3 4 (6, 7) game users for training only.
Use 4, 5, 6, 7 cutoffs and graph

find examples of each item rank to get a sense of latent features
