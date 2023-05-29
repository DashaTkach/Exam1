import itertools

import requests as requests
from pprint import pprint


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload(self, href):
        requests.post(href)


if __name__ == '__main__':
    token = ''
    YaUploader = YaUploader(token)
    with open('token.txt', 'r') as f:
        VK_token = f.read().strip()
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': '273656415',
        'album_id': 'profile',
        'extended': 'likes',
        'access_token': VK_token,
        'v': '5.131'
    }
    res = requests.get(URL, params=params).json()
    photos = []
    dict_t = {}
    dict_name = {}
    inf_photo = []
    max_width = 0
    max_height = 0
    for id_of_photo in res['response']['items']:
        for _dict in id_of_photo['sizes']:
            if _dict['width'] > max_width and _dict['height'] > max_height:
                max_width = _dict['width']
                max_height = _dict['height']
            else:
                max_width += _dict['width']
                max_height += _dict['height']
                type_photo = _dict["type"]
        dict_name[f'{id_of_photo["likes"]["count"]}.jpg'] = _dict['url']
        dict_name = dict(itertools.islice(dict_name.items(), 5))
    for photo_name in list(dict_name.keys()):
        for photo_url in list(dict_name.values()):
            result = [f'name of file: {photo_name}, type = {_dict["type"]}']
        pprint(YaUploader.upload(photo_url))
        pprint(result)
