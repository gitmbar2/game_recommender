import pymongo

# inserted documents will be formatted as:
# {game_id": 238960, "user_id": "76561198118905277", "playtime_forever": 362}

class SteamMongo(object):
    '''
    Wrapper around the pymongo API to simplify queries.
    '''
    def __init__(self):
        try:
            self.conn=pymongo.MongoClient()
            print("Connected successfully!!!")
        except e:
           print("Could not connect to MongoDB: {}".format(e))
        self.uid_field = 'user_id'

    def get_collection(self):
        steam_db = self.conn.steam
        game_plays = steam_db.game_plays
        return game_plays

    def insert_item(self, item):
        collection = self.get_collection()
        collection.insert(item)

    def insert_items(self, items):
        collection = self.get_collection()
        collection.insert(items)

    def user_exists(self, uid):
        collection = self.get_collection()
        return collection.find({self.uid_field: { "$in": [uid]}}).count() > 0

    def list_items(self):
        collection = self.get_collection()
        cursor = collection.find({}, {
            'game_id': True,
            self.uid_field: True,
            'playtime_forever': True
        })
        for item in cursor:
            item.pop('_id', None)
            print(item)

if __name__ == '__main__':
    db = SteamMongo()
    db.list_items()
