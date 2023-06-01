import requests
import configparser
from random import randint
from datetime import datetime
import time
from tqdm import tqdm
from vk_api_ import VkApi


config = configparser.ConfigParser()
config.read("config.ini")
TOKEN_YANDEX = config['YandexDisk']['token']
FOLDER_NAME = f'folder_{datetime.now().date()}_{randint(0, 100)}'


class YandexDiskApi:
    base_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self):
        self.token = TOKEN_YANDEX
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def create_folder(self):
        """
        Метод создает папку на Яндекс.Диске
        """
        url = f'{self.base_url}resources'
        params = {'path': FOLDER_NAME}
        response = requests.put(url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f'Папка "{FOLDER_NAME}" успешно создана на Яндекс.Диске')
        else:
            print(f'Ошибка {response.status_code}: {response.json()["message"]}')
        
        self.upload_photo()
    
    def upload_photo(self):
        """
        Метод загружает изображения на Яндекс.Диск
        """
        example_vk = VkApi()
        dates = example_vk.data_assembly()
        likes = example_vk.return_likes()
        headers = {'Authorization': f'OAuth {TOKEN_YANDEX}'}
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for url_photo in tqdm(dates['url_photos'], desc='Загрузка изображений на Яндекс.Диск'):
            url_index = dates['url_photos'].index(url_photo)
            response = requests.post(upload_url, headers=headers, params={'path': f'/{FOLDER_NAME}/{likes[url_index]}.jpg', 'url': url_photo})
            if response.status_code == 202:
                time.sleep(0.34)
            else:
                print(f'Ошибка загрузки изображения {likes[dates["url_photos"].index(url_photo)]}.jpg на Яндекс.Диск: {response.text}')

if __name__ == "__main__":
    pass