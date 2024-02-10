import json

from src.youtube import MixinYouTube


class PlayList(MixinYouTube):
    """
    Класс для плейлиста с YouTube-канала
    """

    def __init__(self, play_list_id):
        """
        Экземпляр инициализируется id плейлиста.
        Дальше все данные будут подтягиваться по API.
        """
        super().__init__()
        self.play_list_id = play_list_id
        response = self.get_service().playlists().list(id=self.play_list_id,
                                                       part='snippet',
                                                       ).execute()
        self.title = response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.play_list_id}'

