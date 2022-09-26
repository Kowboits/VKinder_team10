mport vk_api
import requests
from pprint import pprint
from config import access_token
import os
from vk_api.utils import get_random_id


class VKphoto:
    url = 'https://api.vk.com/method/'

    def __init__(self):
        self.params = {
            'access_token': access_token,
            'v': '5.131'
        }

    def get_photos(self, finde_user_id):  # Функция получает ID искомого человека, возвращает список сортированных фото
        user_phot_list = []
        owner_id1 = finde_user_id
        url_get_photos = self.url + "photos.get"
        params_get_photos = {
            'owner_id': owner_id1,
            'album_id': 'profile',
            'extended': '1',
            # 'photo_sizes': '0',
            'count': '2'
        }
        res1 = requests.get(url_get_photos, params={**self.params, **params_get_photos})
        user_phot_list.append(sort_photo(res1.json()))
        # print (f'$$$$$$$$${user_phot_list}')
        return user_phot_list

    def get_users(self, city_id):             # Функция получает ID города пользователя и возвращает список ID искомых пользователей
        url_get_photos = self.url + "users.search"
        params_get_photos = {
            'count': '2',
            'fields': 'photo',
            'age_from': '16',
            'age_to': '45',
            'city': city_id,
            'sex': '1',
            # 'status': '1'
        }

        res = requests.get(url_get_photos, params={**self.params, **params_get_photos})
        pprint(res.json())
        list_users = res.json()['response']['items']
        list_id = []

        for i in list_users:
            if i['photo'] != 'https://vk.com/images/camera_50.png' and i['can_access_closed'] != False and i['is_closed'] != True:
                list_id.append(i['id'])
                # user_name = i['first_name']+' '+ i['last_name']
            else:
                pass
        return  list_id

VKphoto = VKphoto()


def sort_photo(res1):       #Функция сортирует полученный список фото
    neded_photo = {}
    neded_photo_list = []
    for photo in res1['response']['items']:
        key = photo['likes']['count']
        value = photo['sizes'][-1]['url']
        if key not in neded_photo.keys() and value not in neded_photo.values():
            pprint(value)
            neded_photo[key] = value
            neded_photo_list.append(write_photos(value))
        else:
            pass
    # pprint(neded_photo_list)
    return neded_photo_list


def write_photos(url1):                    # Функция принимает ссылку на фото и записывает его на сервер(комп) и возвращает путь до фото.
    BASE_PATH = os.getcwd()
    DIR_NAME = 'photos'
    file_path = os.path.join(BASE_PATH, DIR_NAME)
    url = url1
    file_name = os.path.join(file_path, f'{get_random_id()}.jpg')
    r = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(r.content)
    return file_name


