import os
import datetime
from googleapiclient.discovery import build


class Video:
    API_KEY = os.getenv("API_KEY")
    YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id):
        self.video_id = video_id

        data = self.get_data()
        try:
            self.title = data['items'][0]['snippet']['title']
            self.url = f'https://youtu.be/{self.video_id}'
            self.view_count = int(data['items'][0]['statistics']['viewCount'])
            self.like_count = int(data['items'][0]['statistics']['likeCount'])
            self.duration = self.get_duration()

        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
            self.duration = None

    def __str__(self):
        return f'{self.title}'

    def get_data(self):
        data = Video.YOUTUBE.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()

        return data

    def get_duration(self):
        """
        Возвращает продолжительность видео
        в формате PT_H_M_S, независимо на сколько
        времени видео (короткое или большое)
        """
        data = self.get_data()
        duration = list(data['items'][0]['contentDetails']['duration'])

        if 'H' not in duration:
            duration.insert(2, '0')
            duration.insert(3, 'H')
        if 'M' not in duration:
            duration.insert(duration.index('H') + 1, '0')
            duration.insert(duration.index('H') + 2, 'M')
        if 'S' not in duration:
            duration.insert(duration.index('M') + 1, '0')
            duration.insert(duration.index('M') + 2, 'S')

        return ''.join(duration)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.title} ({self.playlist_id})'