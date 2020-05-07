import vk_api
from vk_api.longpoll import VkLongPoll
from datetime import datetime

class Weather:

    def __init__(self, token):
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()
    def send_main_msg(self, number, event):
       self.vk.messages.send(
            user_id=event.user_id,
            message=(
                    "Привет"
            ),
            random_id=number
        )

    def get_longpoll(self):
        return self.longpoll