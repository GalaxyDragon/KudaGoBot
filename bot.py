import datetime

import telebot
import re
import API_kuda
import config


class inform:
    Step = 0
    Near = False
    City = None
    Money = False
    Type = None
    coord = [None, None]

    def zapros(self):
        pass


# steps:
# 1 - события рядом либо простой поиск
usr_now = inform()
bot = telebot.TeleBot(config.token)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


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

    if usr_now.Step == 2 and (message.text == "Geo" or message.text == "No geo"):
        usr_now.Near = (message.text == "Geo")
        if usr_now.Near:
            usr_now.Step = 3
            bot.send_message(message.chat.id, "Пожалуйства, подтвердите геолокацию", reply_markup=config.Geo_Take)
        else:

            bot.send_message(message.chat.id, "Тип мероприятия", reply_markup=config.Place_Type)
            usr_now.Step = 3

    if usr_now.Step == 3 and config.Type_filtr(message.text):
        usr_now.Type = message.text
        bot.send_message(message.chat.id, "Бесплатные?", reply_markup=config.Y_N)
        usr_now.Step = 4

    if usr_now.Step == 4 and (message.text == "Да" or message.text == "Нет" or message.text == "Не имеет значения"):
        usr_now.Step = 5
        usr_now.Money = (message.text == "Да")
        if message.text == "Не имеет значения":
            usr_now.Money = None

        bot.send_message(message.chat.id, "Это всё", reply_markup=config.Ready)

    if usr_now.Step == 5:
        print(usr_now.Step, usr_now.Type, usr_now.City, usr_now.Money, usr_now.Near)

    if usr_now.Step == 7:
        bot.send_message(message.chat.id, "Ищем события для Вас...")
        answer = API_kuda.get_events_geo(float(55.725979), float(37.464099))
        bot.send_message(message.chat.id, "Спасибо за ожидаение!", reply_markup=config.Ready)
        print(answer)
        if answer is None:
            answer = "Событий рядом с Вами найти не удалось."
            bot.send_message(message.chat.id, answer,
                             reply_markup=config.Ready)
        else:
            message_text = answer[1]
            next = answer[0]
            for i in range(len(message_text)):
                reply_list = message_text[i]
                reply = "#" + str(i + 1) + "\n" + reply_list["title"] + "\n" \
                        + cleanhtml(reply_list["description"]) + "\n" + "Время начала мероприятия: " + "\n" + \
                        datetime.datetime.fromtimestamp(int(reply_list["dates"]["start"])).strftime(
                            '%Y-%m-%d %H:%M') + "Время конца мероприятия: " + "\n" \
                        + cleanhtml(reply_list["description"]) + "\n" + "Время начала мероприятия: " + "\n" + \
                        datetime.datetime.fromtimestamp(int(reply_list["dates"]["end"])).strftime(
                            '%Y-%m-%d %H:%M')


                bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
            bot.send_message(message.chat.id, "Надеемся, что мы смогли Вам помочь!",
                             reply_markup=config.Ready)
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
