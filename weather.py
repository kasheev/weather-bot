import vk_api
from vk_api.longpoll import VkLongPoll
import pyowm
import math
import json

own = pyowm.OWM('3b4aa439966c6a305dd471efd3cabb9f', language= 'ru')


class Weather:

    def __init__(self, token):
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def get_longpoll(self):
        return self.longpoll

    def check_city(self, request):
        try:
            om = own.weather_at_place(request)
            return True
        except Exception:
            return False

    def answer(self,event,number):
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                    'Вы ошиблись\n'
            ),
            random_id=number
        )

    def effective_temperature(self, temperature, weather):
        wind = weather.get_wind()['speed']
        humindity = weather.get_humidity()
        e = (humindity / 100) * 6.105 * math.exp(17.27 * temperature / (237.7 + temperature))
        AT = int(temperature + 0.348 * e - 0.7 * wind - 4.25) + 1
        return AT

    def what_to_wear(self,segment,status):
        status = status.lower()
        with open("weather.json", "r", encoding='utf-8') as read_file:  # считываем данные из файла
            data = json.load(read_file)
            try:
                string = data['погода'][status]
                return string
            except KeyError:
                string = data['температура'][str(segment)]
                return string

    def info_weather_city(self, number, event, request):
        observation = own.weather_at_place(str(request))
        weather = observation.get_weather()
        temperature = weather.get_temperature('celsius')['temp']
        status = weather.get_detailed_status()
        effective_temp = self.effective_temperature(temperature,weather)
        segment = math.ceil(effective_temp/10)
        advice = self.what_to_wear(segment,status)
        self.vk.messages.send(
            user_id=event.user_id,
            message=(
                    'Город ' + request.title() + '\n'
                    'Температура ' + str(int(temperature)) + ' С°\n'
                    'Ощущается как ' + str(effective_temp) + ' С°\n'
                    'Погода ' + status + ' \n'
                    'Cоветую тебе ' + str(advice) + ' \n'
            ),
            random_id = number
        )

