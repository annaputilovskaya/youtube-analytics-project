import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key: str = os.getenv('YT_API_KEY')
        self.__channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.channels().list(
            id=self.__channel_id,
            part='snippet,statistics'
        ).execute()
        self.title = response['items'][0]['snippet']['title']
        self.description = response['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + response['items'][0]['id']
        self.subscriber_count = response['items'][0]['statistics']['subscriberCount']
        self.video_count = response['items'][0]['statistics']['videoCount']
        self.view_count = response['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.__channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False, indent=2)




