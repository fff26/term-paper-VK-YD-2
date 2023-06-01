from vk_api_ import VkApi
from yandex_disk_api import YandexDiskApi


vk_save = VkApi()
yd_copy = YandexDiskApi()

vk_save.run()
yd_copy.create_folder()