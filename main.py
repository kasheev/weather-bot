import vk_api
from vk_api.longpoll import VkEventType
import random
import weather

token = open('token.txt','r')
weather_bot = weather.Weather(token.read())


def send_messages():
    """отравка сообщения"""
    c_box = False #флаг переключения
    for event in weather_bot.get_longpoll().listen(): #цикл обработки события пользователя
        if event.type == VkEventType.MESSAGE_NEW: #обработка нового ответа
            if event.to_me:
                request = event.text.lower() #преобразуем в текст, где все буквы в нижнем регистре
                number = random.getrandbits(64) #случайное числло для message
            print("Send new message:" + str(event.user_id)) #вывод информации о новом событии в консоль

            if request:
                c_box = weather_bot.check_city(request) # с помощью флага обрабатываю сообщение(город или нет)
                if c_box: # если True
                    weather_bot.info_weather_city(number, event, request) # функция возвращает информацию погоды в городе
                else:
                    weather_bot.answer(event, number) #функция выводит сообщение об ошибке


def main():
    send_messages()


if __name__ == '__main__': #точка входа в программу
    main()
