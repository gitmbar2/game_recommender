import requests
import json
import config
import os

# test_app = 340
path_of_exile_id = 238960

class SteamPoweredAPI(object):
    def __init__(self):
        self.key = config.get_key()
        self.test_user = config.get_test_user_id()
        self.base_api_url = "http://api.steampowered.com/"
        self.base_store_api_url = "http://store.steampowered.com/"

    def testing(self):
        gameid = '238960'
        base_url = self.base_api_url
        # path = "ISteamApps/GetAppList/v0002/?format=json"
        # path = "ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=%s&format=json" % gameid
        path = "IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json".format(self.key, self.test_user)
        url = base_url + path

        print('getting url: ', url)
        response = requests.get(url).content
        return response

    def get_user_info(self, user_ids):
        '''JSON - return some very basic information about the user if public'''
        formatted_user_id = [str(user_id) for user_id in user_ids]
        base_url = self.base_api_url
        path = "ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}".format(self.key, formatted_user_id)
        url = base_url + path

        print('getting url: ', url)
        response = requests.get(url).content
        return response

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


''' Testing '''
if __name__ == "__main__":
    api = SteamPoweredAPI()
    test_user = config.get_test_user_id()
    # apps = [270880]

    info = api.testing()
    print(info)
    # users = [test_user]
    # info = api.get_user_info(users)
    #
    # current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # write_to = os.path.join(current_dir, 'data/all_games.json')
    # print(write_to)
    # with open(write_to, 'w') as outfile:
    #     json.dump("".join(str(info).split()), outfile)
