import os
from googleapiclient.discovery import build


class MixinYouTube:
    """Вспомогательный класс для работы с YouTube API"""
    def __init__(self):
        pass

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)