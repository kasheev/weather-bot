import vk_api
from vk_api.longpoll import VkEventType
import random
import weather


token = '8e394514295399d4cd6d3175dac80d4268ed1065d6bc68d74d3b73b5e5ee3b98d9c7fead5fb88354b11c5'
weather_bot = weather.Weather(token)

def send_messages():
    c_box = False  # флаги переключения
    coord_box = False
    for event in weather_bot.get_longpoll().listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                number = random.getrandbits(64)
            print("Send new message:" + str(event.user_id))
            if request == "привет":
                weather_bot.send_main_msg(number, event)

def main():
    send_messages()

if __name__ == '__main__':
    main()