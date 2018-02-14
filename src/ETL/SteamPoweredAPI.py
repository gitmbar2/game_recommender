import requests
import json
import config
import os
from bson import json_util

# test_app = 340
path_of_exile_id = 238960

class SteamPoweredAPI(object):
    '''
    Wrapper around Steam APIs.
    See https://developer.valvesoftware.com/wiki/Steam_Web_API.
    Also has some reformatting methods to standardize results.
    '''
    def __init__(self):
        self.key = config.get_key()
        self.test_user = config.get_test_user_id()
        self.base_api_url = "http://api.steampowered.com/"
        self.base_store_api_url = "http://store.steampowered.com/"

    # write to disk
    def write_games_for_users_to_json(self, user_ids, filepath):
        '''
            Args:
                user_id: list of int or stringified ints
            Returns:
                JSON
                {response: {
                    games: array
                }}
        '''
        formatted_user_ids = [str(user_id) for user_id in user_ids]
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        write_to = os.path.join(current_dir, filepath)
        for formatted_user_id in formatted_user_ids:
            response = self.get_games_for_user(formatted_user_id)
            if response:
                with open(write_to, 'ab') as f:
                    for game in response:
                        f.write(json_util.dumps(game)+'\n')

    # The hours on steam is only logged if you are playing while connected to the steam network.
    # If you are playing while steam is offline or steam somehow loses connection, no hours will be logged.
    def get_games_for_user(self, user_id):
        '''
            Rather than returning empty JSON for no games, returns None
            Args:
                user_id: stringified number (valid steam id seems to be len 17)
            Returns:
                JSON
                {response: {
                    games: array
                }}
                or None
        '''
        if type(user_id) is not str:
            raise TypeError('user id should be in string format')
        path = "IPlayerService/GetOwnedGames/v1/?key={0}&steamid={1}&format=json".format(self.key, user_id)
        url = self.base_api_url + path
        print('getting url: {}'.format(url))

        try:
            response = requests.get(url, timeout=60)
        except Exception as e:
            return None

        print('response code:', response.status_code)
        if response.status_code is not 200:
            return None

        return self.format_games_response(response.json(), user_id)

    def format_games_response(self, response_string, user_id):
        # We want to have either csv or json delimited by line
        # including data: user_id, game_id, playtime
        output = []
        data = response_string['response']
        if not 'games' in data:
            return None
        for game in data['games']:
            output_item = {
                'user_id': user_id,
                'game_id': game['appid'],
                'playtime_forever': game['playtime_forever'],
            }
            output.append(output_item)
        return output

    def get_user_info(self, user_ids):
        '''JSON - return some very basic information about the user if public'''
        formatted_user_ids = [str(user_id) for user_id in user_ids]
        base_url = self.base_api_url
        path = "ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}".format(self.key, formatted_user_ids[0])
        url = base_url + path

        print('getting url: {}'.format(url))
        response = requests.get(url).content
        return response['response']

    def get_app_info(self, app_ids):
        '''
            JSON - return all info about the game
            'is_free' and 'price_overview' are important fields
        '''
        # '&filters=price_overview' can filter for a specific field
        formatted_app_ids = [str(app_id) for app_id in app_ids]
        path = "api/appdetails?appids={0}".format(','.join(formatted_app_ids))
        # path = "appdetails?appids={0}&cc=en_US".format(formatted_app_ids)
        url = self.base_store_api_url + path

        print('getting url: ', url)
        info = requests.get(url).content
        return info

    def get_app_reviews(self, app_ids):
        path = "appreviews/{0}?json=1&filter=recent&start_offset=0&review_type=all&day_range=100&purchase_type=steam&language=all".format(app_ids)
        url = self.base_store_api_url + path

        print('getting url: ', url)
        info = requests.get(url).content
        return info

if __name__ == "__main__":
    api = SteamPoweredAPI()
    test_user = config.get_test_user_id()

    # '76561197984981409' is some random known positive id
    users = [test_user, '76561197984981409']
    info = api.get_games_for_users(users)
    print(info)
