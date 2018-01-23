## Playtime Distribution (playtime_distribution.ipynb)
We can see that the number of users who have played n or more games drops off very quickly.  
![alt text](figures/user_dropoff.png "Logo Title Text 1")

## Train / Test split
The standard train test split does not necessarily work for recommender systems.  
The method used here for creating splits is to split only by users, feeding
some percentage of the test users' data back into the training set.  
