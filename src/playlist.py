import datetime

from src.youtube import MixinYouTube
import isodate


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
        self.__video_response = None
        self.__playlist_id = play_list_id
        self.__youtube = self.get_service()
        response = self.__youtube.playlists().list(id=play_list_id,
                                                   part='snippet',
                                                   ).execute()
        self.title = response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={play_list_id}'

    @property
    def total_duration(self):
        """
        Подсчитывает и возвращает суммарную длительность плейлиста
        :return: объект класса datetime.timedelta
        """
        total_duration = datetime.timedelta(0)
        for video in self.get_info_about_videos()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def get_info_about_videos(self):
        """
        Возвращает информацию о видео плейлиста
        :return: dictionary
        """
        if self.__video_response is None:
            playlist_videos = self.__youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
            video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
            self.__video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                                 id=','.join(video_ids)
                                                                 ).execute()
        return self.__video_response

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        :return:
        """
        max_like_count = 0
        video_id = ''
        for video in self.get_info_about_videos()['items']:
            if int(video['statistics']['likeCount']) > max_like_count:
                max_like_count = int(video['statistics']['likeCount'])
                video_id = video['id']
        return f"https://youtu.be/{video_id}"
