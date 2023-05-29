import requests as requests


class YaUploader:

    def init(self, token: str):
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
        p = requests.get(name_of_file)
        files = {'file': p.content}
        requests.put(href, files=files)


if __name__ == '__main__':
    token = ''
    YaUploader = YaUploader(token)
    VK_token = ''
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

    for id_of_photo in res['response']['items']:
        for _dict in id_of_photo['sizes']:
            photos.append([_dict, id_of_photo["likes"]["count"], id_of_photo["date"]])

    res_sorted = sorted(photos, key=lambda x: x[0]['width'] * x[0]['height'], reverse=True)
    bigger_photo = []
    for i in range(5):
        bigger_photo.append(res_sorted[i])

    list_to_load = []
    names = []

    for i in range(5):
        now_name = bigger_photo[i][1]
        for j in range(5):
            if i != j and now_name == bigger_photo[j][1]:
                if i < j:
                    bigger_photo[j][1] = str(bigger_photo[j][1]) + "-" + str(bigger_photo[j][2])
                else:
                    bigger_photo[i][1] = str(bigger_photo[i][1]) + "-" + str(bigger_photo[i][2])

    print("[")
    for i in range(5):
        print('{' + '\n"file_name" : "' + str(bigger_photo[i][1]) + '.jpg"' + '\n"size" : "' + str(
            bigger_photo[i][0]["type"]) + '"\n},')
    print("]")

    for i in range(5):
        YaUploader.upload(str(bigger_photo[i][1]) + ".jpg", str(bigger_photo[i][0]["url"]))
