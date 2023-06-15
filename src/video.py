import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

class Video:
    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        video = self.__get_service()
        self.title = video['items'][0]['snippet']['title']
        self.description = video['items'][0]['snippet']['description']
        self.url = video['items'][0]['snippet']['thumbnails']["default"]['url']
        self.like_count = int(video['items'][0]['statistics']['likeCount'])
        self.viewCount = int(video['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_id}')"

    def __get_service(self):
        '''
        Возвращает данные о видео в формате словаря
        :return: данные о канале
        '''
        video = youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()

        return video

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.title}'