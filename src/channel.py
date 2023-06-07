import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """
    Класс для ютуб-канала
    """
    dict_hw_2 = {}

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriberCount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.viewCount = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title}, {self.url}'

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        return int(self.subscriberCount) == int(other.subscriberCount)

    def print_info(self) -> None:
        """
        метод-класса `Channel` выводит в консоль информацию о канале.
        """
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(info)


    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        try:
            channel_id[:2] != 'UC'

        except:
            print('Нельзя менять')

    @classmethod
    def get_service(cls):
        """
        класс-метод `get_service()`, возвращающий объект для работы с YouTube API
        """
        object_get = build('youtube', 'v3', developerKey=api_key)
        return object_get

    def to_json(self, file_name):
        """
        метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        self.dict_hw_2['id'] = self.channel_id
        self.dict_hw_2['title'] = self.title
        self.dict_hw_2['description'] = self.description
        self.dict_hw_2['url'] = self.url
        self.dict_hw_2['subscriberCount'] = self.subscriberCount
        self.dict_hw_2['video_count'] = self.video_count
        self.dict_hw_2['viewCount'] = self.viewCount

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self.dict_hw_2, f, indent=2, ensure_ascii=False)
