import Mongo
import SteamPoweredAPI
import random
import time

'''
Script to move data from Steam to local MongoDB,
with db and collection specified in SteamMongo class
'''

db = Mongo.SteamMongo()

steam_api = SteamPoweredAPI.SteamPoweredAPI()

# steam ids are 17 digits long, maybe starting at around 76561197960265729
first_id = 76561197960265729
last_id = first_id + 200000000
sample_count = 10000
users_to_query = random.sample(range(first_id, last_id), sample_count)

usable_count = 0
games_added = 0

start_time = time.time()
for user in users_to_query:
    user = str(user)
    # Don't add twice
    if db.user_exists(user):
        print('duplicate ID')
        continue

    # Fetch from Steam API
    time.sleep(2)
    print('querying ', user)
    games = steam_api.get_games_for_user(user)
    if games is None:
        print('No games found for user.')
        continue

    # Add to MongoDB
    # We are creating a dataset where all users have played at least 1 game,
    # not just purchased some games without playing them
    should_add = False
    for game in games:
        if game['playtime_forever'] is not 0:
            should_add = True
    if should_add:
        print('FOUND {} GAMES FOR USER'.format(len(games)))
        db.insert_item(games)
        usable_count += 1
        games_added += len(games)
    else:
        print('User had no games with playtime greater than 0')

print('total useful out of {} ids: {}'.format(sample_count, usable_count))
print('total games added: {}'.format(games_added))
print('total time: {}'.format(time.time() - start_time))

# to dump as line delimited json from command line:
'''
mongo localhost/steam --eval "db.game_plays.find(
  {}, {
    '_id': 0
  }).forEach(function(x){
    printjsononeline(x);
  })" | tail -n +4 >> filename
'''
