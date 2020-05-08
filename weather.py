import vk_api
from vk_api.longpoll import VkLongPoll
import pyowm

own = pyowm.OWM('3b4aa439966c6a305dd471efd3cabb9f', language='ru')


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

    def check_city(self, event, number):
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                "Введите город\n "
            ),
            random_id=number
        )
        return True

    def info_weather_city(self, number, event, request):
        observation = own.weather_at_place(str(request))
        w = observation.get_weather()
        temperature = w.get_temperature('celsius')['temp']
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                    'Город ' + request.title() + '\n'
                    'Температура ' + str(int(temperature)) + '\n'
            ),
            random_id = number
        )