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

    def link_for_upload(self, file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path, name_of_file):
        href = self.link_for_upload(file_path=file_path).get("href", "")
        requests.put(href, data=open(name_of_file, 'rb'))


if __name__ == '__main__':
    token = 'Впишите свой токен я Яндекс Полигона'
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
        dict_t[_dict['url']] = [_dict['width'], _dict['height']]
        files = sorted(dict_t, key=dict_t.get, reverse=True)[:5]
        for url in files:
            with open(f'{id_of_photo["likes"]["count"]}.txt', 'w') as photo:
                photo.write(_dict['url'])
        pprint(
            YaUploader.upload(f'{id_of_photo["likes"]["count"]}.txt', f'{id_of_photo["likes"]["count"]}.txt'))
        result = [f'{id_of_photo["likes"]["count"]}.txt', f'{id_of_photo["likes"]["count"]}.jpg',
                  f'type = {_dict["type"]}']
        pprint(result)
