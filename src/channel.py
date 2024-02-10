import json

from src.youtube import MixinYouTube


class Channel(MixinYouTube):
    """Класс для YouTube-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется по id канала.
        Дальше все данные будут подтягиваться по API.
        """
        super().__init__()
        self.__channel_id = channel_id
        response = self.get_info_about_channel()
        self.title = response['items'][0]['snippet']['title']
        self.description = response['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + response['items'][0]['id']
        self.subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(response['items'][0]['statistics']['videoCount'])
        self.view_count = int(response['items'][0]['statistics']['viewCount'])

    def __str__(self):
        """
        Отображает информацию о канале для пользователей
        :return: <название_канала> (<ссылка_на_канал>)
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """
        Складывает количество подписчиков канала1 и канала2
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """
        Вычитает из количества подписчиков канала1 количество подписчиков канала2
        """
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        """
        Проверяет, является ли количество подписчиков канала1 меньше подписчиков канала2
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """
        Проверяет, является ли количество подписчиков канала1 меньше или равно подписчиков канала2
        """
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        """
        Проверяет, является ли количество подписчиков канала1 больше подписчиков канала2
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """
        Проверяет, является ли количество подписчиков канала1 больше или равно подписчиков канала2
        """
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        """
        Проверяет, является ли количество подписчиков канала1 и канала2 одинаковым
        """
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def get_info_about_channel(self):
        """Получает информацию о канале."""
        youtube = self.get_service()
        return youtube.channels().list(
            id=self.__channel_id,
            part='snippet,statistics'
        ).execute()

    def print_info_about_channel(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.get_info_about_channel()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False, indent=2)
