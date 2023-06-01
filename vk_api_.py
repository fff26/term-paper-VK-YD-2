import requests
import configparser
import json


config = configparser.ConfigParser()
config.read("config.ini")
API_TOKEN_VK = config["VK"]["api_token"]


class VkApi:
    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self):
        self.api_token = API_TOKEN_VK
        self.user_id = None

    def get_user_id(self, screen_name):
        """
        Метод получает id пользователя по его screen_name
        """
        method = 'utils.resolveScreenName'
        url = f'{self.BASE_URL}{method}'
        params = {'screen_name': screen_name, 'access_token': self.api_token, 'v': '5.131'}
        response = requests.get(url, params=params)
        data = response.json()
        if 'response' not in data:
            print(f'Ошибка получения данных: {data.get("error", {}).get("error_msg", "неизвестная ошибка")}')
            return None
        else:
            return data['response']['object_id']

    def get_user_id_once(self):
        """
        Метод запрашивает id или screen_name пользователя у пользователя, если они еще не были введены
        """
        if self.user_id:
            return self.user_id
        else:
            name = input('Введите id или screen_name пользователя ВК:\n')
            self.user_id = name
            if name.isdigit():
                self.user_id = name
            else:
                self.user_id = self.get_user_id(name)
            return self.user_id

    def get_photo_data(self):
        """
        Метод получает данные о изображениях пользователя ВК и возвращает элементы 
        """
        user_id = self.get_user_id_once()
        count = input('Введите число сохраняемых изображений (по умолчанию 5): ')
        count = int(count) if count.isdigit() else 5
        method = 'photos.get'
        url = f'{self.BASE_URL}{method}'
        params = {'owner_id': user_id, 'album_id': 'profile', 'rev': 0, 'extended': 1, 'photo_sizes': 1, 'access_token': self.api_token, 'v': '5.131', 'count': count}
        response = requests.get(url, params=params)
        data = response.json()
        if 'response' not in data:
            print(f'Ошибка получения данных: {data.get("error", {}).get("error_msg", "неизвестная ошибка")}')
            return None
        else:
            return data['response']['items']

    def data_assembly(self):
        """
        Метод формирует имена файлов и список данных изображений
        """
        user_id = self.get_user_id_once()
        data = self.get_photo_data()

        list_url_photos, list_likes = [], []
        list_dates, list_sizes = [], []

        for info in data:
            list_url_photos.append(info['sizes'][-1]['url'])
            list_likes.append(info['likes']['count'])
            list_dates.append(info['date'])
            list_sizes.append(info['sizes'][-1]['type'])
        for i in range(len(list_likes)):
            if list_likes.count(list_likes[i]) > 1:
                index = list_likes.index(list_likes[i], i+1)
                list_likes[i] = str(list_likes[i]) + '_' + str(list_dates[index])
        lists_dates = {'url_photos': list_url_photos, 'likes': list_likes, 'dates': list_dates, 'sizes': list_sizes}
        return lists_dates

    def json_saving(self):
        """
        Метод записывает json-файлы данных на локальный диск
        """
        data = self.data_assembly()
        like = data['likes']
        size = data['sizes']
        json_list = []
        numberer = 0
        for i in range(len(like)):
            json_dict = {}
            json_dict['file_name'] = f'{like[i]}.jpg'
            json_dict['size'] = size[i]
            json_list.append(json_dict)
            with open(f'image_{numberer}.json', 'w') as file:
                json.dump(json_list, file, indent=2)
            json_dict.clear()
            json_list.clear()
            numberer += 1
        print('Данные успешно сохранены в файл json-файлы')
        return like
        
    def download_photos(self):
        """
        Метод загружает изображения на локальный диск
        """
        data = self.data_assembly()
        urls = data['url_photos']
        names = data['likes']
        for url, name in zip(urls, names):
            response = requests.get(url)
            with open(f'{name}.jpg', 'wb') as file:
                file.write(response.content)
        print('Изображения успешно загружены на ПК')

    def return_likes(self):
        data = self.data_assembly()
        return data['likes']
        
    def run(self):
        """
        Метод запускает выполнение программы
        """
        self.json_saving()
        self.download_photos()

if __name__ == '__main__':
    pass