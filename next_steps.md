# Next Steps  

## Cold Start
Our model currently is not trained to make predictions for users with less than some number of games played.  
For these users, we can instead recommend them the most popular items, or weigh popularity with a recommendation based on Item Similarity instead of Collaborative Filtering.  

Even for Users who have played the minimum number of games to pass the cutoff to receive recommendations, it may be useful to combine the recommendations from Collaborative Filtering with an Item Similarity based model to give the user some confidence in the recommendation system.  As the user plays more games, we can weight the Collaborative Filtering recommendation more highly.  
This would need to be A / B tested, but also chosen based on product goals.  

For new items, it may benefit the community to randomly recommend them to some people based on Item Similarity.  A less risky approach is just to have a "New Content" section.  


## Alternate Evaluation
Instead of comparing NDCG to a random model, we could compare it to recommending the games with the highest average normalized playtimes.  


## Algorithm Optimization
The documentation for Spark ALS seems to suggest that it is not training the model to normalize for user and item bias.  Games that are always highly rated and people who always rate high/low will make the collaborative filtering less effective.  To improve the model, we may have to manually implement this algorithm in Scala in the Spark codebase.  

We are normalizing the game play time before it enters the model, but the bias will not be updated at each step of the ALS to include the predictions.  


## More Granular Results
Currently we are training the model by setting a minimum number of games played for users and plays for the game.  We then evaluate with these same cutoffs.  
But it is also possible to train with certain cutoffs and test with others.  In this way we could see how including users with 4+, 5+, or 6+ games in the model impacts the NDCG increase for users with 7+ games, if we were choosing 7 as our cutoff.  

The value of this would be reducing the time / cost of training the model once we focus in on a few possible cutoffs.


## Hyperparameter Tuning
Ideally, hyperparameters such as Rank and Lambda would be tuned with the dataset that would actually be used in production - not just a small subset, and not the entire dataset.  

How many iterations of ALS to run through would have to be chosen based on model evaluation metrics as well as absolute time cost.
