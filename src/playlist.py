import os
import datetime

from googleapiclient.discovery import build
from src.video import Video


class PlayList:
    """
    Класс, который создаёт
    объект на основе YouTube-плейлиста
    """
    API_KEY = os.getenv("API_KEY")
    YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        self._playlist_id = playlist_id

        data = self.__load_pl_data()
        self.title = data['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self._playlist_id}'

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._playlist_id}')"

    def __str__(self):
        return f'{self.url}'

    def __load_pl_data(self):
        """
        Загружает данные о плейлисте
        """
        data = PlayList.YOUTUBE.playlists().list(
            part='snippet',
            id=self._playlist_id,
        ).execute()
        return data

    def __load_video_data(self):
        """
        Загружает данные о видеороликах
        в плейлисте
        """
        playlist_videos = PlayList.YOUTUBE.playlistItems().list(
            playlistId=self._playlist_id,
            part='contentDetails, id, snippet, status',
            maxResults=50,
        ).execute()
        return playlist_videos

    @property
    def total_duration(self):
        """
        Метод считает продолжительность плейлиста
        выводя его как аттрибут класса
        """
        hours = 0
        minutes = 0
        seconds = 0
        playlist_videos = self.__load_video_data()
        for video in range(0, len(playlist_videos['items'])):
            video_id = playlist_videos['items'][video]['contentDetails']['videoId']
            video_in_pl = Video(video_id)
            duration = datetime.datetime.strptime(video_in_pl.duration, "PT%HH%MM%SS")
            hours += duration.hour
            minutes += duration.minute
            seconds += duration.second

        playlist_duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return playlist_duration

    def show_best_video(self):
        """
        Метод возвращает cсылку на самое популярное
        по просмотрам видео, находящиесе в плейлисте
        """
        playlist_videos = self.__load_video_data()
        best_video_url = None
        best_views = 0
        for video in range(0, len(playlist_videos['items'])):
            video_id = playlist_videos['items'][video]['contentDetails']['videoId']
            video_in_pl = Video(video_id)
            if best_views < video_in_pl.view_count:
                best_video_url = video_in_pl.url
                best_views = video_in_pl.view_count

        return best_video_url
