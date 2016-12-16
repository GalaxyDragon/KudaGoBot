import config
import os
import time
import telebot, json
from telebot import types
import API_kuda

class inform:
    Step = 0
    Near = False
    City = None
    Money = False
    Type = None
    coord = [None,None]
    def zapros(self):
        pass
# steps:
# 1 - события рядом либо простой поиск
usr_now = inform()
bot = telebot.TeleBot(config.token)
f = open('text.txt')
print("S...S...Senpai?")
print(f.read())

@bot.message_handler(commands=["start"])
def img_ids(message):
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=config.main_menu)
    usr_now.Step = 1


@bot.message_handler(content_types=["text"])
def meropriyatiya(message):
    if usr_now.Step == 1:
        usr_now.City = message.text
        usr_now.Step = 2
        bot.send_message(message.chat.id, "Мероприятия рядом?", reply_markup=config.Geolocate)



    if usr_now.Step == 2 and( message.text == "Geo" or message.text == "No geo") :
        usr_now.Near = (message.text == "Geo")
        if usr_now.Near:
            usr_now.Step = 3
            bot.send_message(message.chat.id, "Пожалуйства, подтвердите геолокацию", reply_markup=config.Geo_Take)
        else:

            bot.send_message(message.chat.id, "Тип мероприятия", reply_markup=config.Place_Type)
            usr_now.Step = 3
            time.sleep(2)
    if usr_now.Step == 3 and config.Type_filtr(message.text):
        usr_now.Type = message.text
        bot.send_message(message.chat.id, "Бесплатные?",reply_markup=config.Y_N)
        usr_now.Step = 4
        time.sleep(2)
    if usr_now.Step == 4 and (message.text == "Да" or message.text == "Нет" or message.text == "Не имеет значения"):
        usr_now.Step = 5
        usr_now.Money = (message.text == "Да")
        if message.text == "Не имеет значения":
            usr_now.Money = None
        bot.send_message(message.chat.id, "Это всё",reply_markup=config.Ready)
        time.sleep(2)
    if usr_now.Step == 5:
        print(usr_now.Step, usr_now.Type, usr_now.City, usr_now.Money, usr_now.Near)
    if usr_now.Step == 7:
        bot.send_message(message.chat.id, "Подождите, формируется список мест...")
        Answer = API_kuda.get_events_geo(float(usr_now.coord[0]),float(usr_now.coord[0]))
        bot.send_message(message.chat.id," Всё бля, ты герой. Дождался. " +  Answer[1][0]["title"], reply_markup=config.Ready)
        usr_now.Step = 8

@bot.message_handler(content_types=['location'])
def location(message):
    # bot.send_message(message.chat.id, 'Предлагаем посмотреть следующие события ')
    a = message.location
    b = str(a).split(":")
    usr_now.coord = [b[1].split(",")[0][1:], b[2][1:-1]]
    usr_now.Step = 7
    bot.send_message(message.chat.id, "Это всё", reply_markup=config.Ready)
if __name__ == '__main__':
    bot.polling(none_stop=True)