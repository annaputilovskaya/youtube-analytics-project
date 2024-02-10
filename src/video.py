from src.channel import MixinYouTube


class Video(MixinYouTube):
    """Класс для видео с YouTube"""
    def __init__(self, video_id):
        """
        Экземпляр инициализируется по id видео.
        Дальше все данные будут подтягиваться по API.
        """
        self.video_id = video_id
        video_response = self.get_info_about_video()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.video_url = f'https: // www.youtube.com / watch?v = {self.video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        Отображает информацию о видео для пользователей
        :return: <название_видео>
        """
        return self.video_title

    def get_info_about_video(self):
        """Получает информацию о видео"""
        youtube = self.get_service()
        return youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()


class PLVideo(Video):
    """Класс для видео в плейлисте"""
    def __init__(self, video_id, playlist_id):
        """
        Экземпляр инициализируется по id видео и id канала.
        Дальше все данные будут подтягиваться по API.
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
