import vk_api
from vk_api.longpoll import VkLongPoll
import pyowm
import math
import json

own = pyowm.OWM('3b4aa439966c6a305dd471efd3cabb9f', language='ru')


class Weather:

    def __init__(self, token):
        """конструктор"""
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def get_longpoll(self):
      """получаю лонгпулл"""
        return self.longpoll

    def check_city(self, request):
        """функиця для проверки города"""
        try:
            om = own.weather_at_place(request)#передаю в функцию сообщение пользователя
            return True
        except Exception: #если города нет, то выкидывает ошибку
            return False

    def answer(self, event, number):
        """выводит сообщение пользователю, если город введен неверно или произошла ошибка"""
        self.vk.messages.send(#формирую сообщение
            user_id=event.user_id,
            message=( #
                'Что-то пошло не так...\n'
                'Для того чтобы узнать погоду, напишите в чат интересующий вас город.\n'
                'Например: Санкт-Петербург\n'
            ),
            random_id=number
        )

    def effective_temperature(self, temperature, weather):# передаю погоду и температуру
        """считаю тепмерутуру 'по ощущениям'"""
        wind = weather.get_wind()['speed'] #получаю скорость ветра
        humindity = weather.get_humidity() #получаю влажность
        e = (humindity / 100) * 6.105 * math.exp(17.27 * temperature / (237.7 + temperature)) #высчитываю коэф. e
        AT = int(temperature + 0.348 * e - 0.7 * wind - 4.25) + 1 #высчитываю температуру 'по ощущениям'
        return AT #возвращаю темпертару 'по ощущениям'

    def what_to_wear(self, segment, status):# передаю сегмент и погоду
        '''выбор того, что надеть'''
        status = status.lower() #получаем какая сейчас погода
        if segment < -3: #обработка критических температур по ощущениям t < -30
            return 'надеть всё или остаться дома. На улице ооочень холодно'
        elif segment > 3: # t > +30
            return 'надеть майку и шорты, ибо очень жарко'
        try: #проеврка на открытие файла
            with open("weather.json", "r", encoding='utf-8') as read_file:  # считываем данные из файла
                data = json.load(read_file)
                try:
                    string = data['погода'][status] #обрабатываем критическую погоду:дождь, гроза
                    return string #возвращаем что надеть
                except KeyError:
                    string = data['температура'][str(segment)] #обрабатываем температуру
                    return string #возвращаем что надеть
        except FileNotFoundError:
            return '¯\_(ツ)_/¯' #если везде ошибки

    def info_weather_city(self, number, event, request):
        """отправка сообщения о погоде"""
        observation = own.weather_at_place(str(request))#получаем информацию о городе, который интересует
        weather = observation.get_weather()#получаем погоду
        temperature = weather.get_temperature('celsius')['temp'] #получаем температуру в цельсиях
        status = weather.get_detailed_status() #получаем погоду
        effective_temp = self.effective_temperature(temperature, weather)#получаем погоду по ощущениям
        segment = math.ceil(effective_temp / 10) #делаем сегменты, для того чтобы опредлять, что надеть
        advice = self.what_to_wear(segment, status)#получаем совет
        self.vk.messages.send( #отправвяю сообщение
            user_id=event.user_id,
            message=(
                    'Город: ' + request.title() + '\n'
                    'Температура: ' + str(int(temperature)) + ' С°\n'
                    'Ощущается как: ' + str(effective_temp) + ' С°\n'
                    'Сейчас: ' + status + ' \n'
                    'Cоветую тебе ' + str(advice) + ' \n'
            ),
            random_id=number
        )