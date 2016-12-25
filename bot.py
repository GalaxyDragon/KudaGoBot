import datetime
import telebot
import re
import API_kuda
import config


class GetInformation:
    Step = 0
    Near = False
    City = None
    Money = False
    Type = None
    coord = [None, None]
    next_link = ""
    def request_(self):
        pass


# не убирать, так удобнее понять из консоли что всё запустилось и всё кошерно
print("Hello, my developer")

# steps:
# 1 - события рядом либо простой поиск
usr_now = GetInformation()
bot = telebot.TeleBot(config.token)


# пока много шлака но оставь, 1 хер допиливать до полного.Если уж совсем
# не имётся, то можешь подчищенный на новую ветку кинуть. Или меня пнуть, чтобы саам чего лишнего не стёр. Как хошь

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@bot.message_handler(commands=["start"])
def img_ids(message):
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=config.main_menu)
    usr_now.Step = 2


@bot.message_handler(content_types=["text"])
def events(message):
    if usr_now.Step == 1:
        usr_now.City = message.text
        usr_now.Step = 2
        bot.send_message(message.chat.id, "Мероприятия рядом?", reply_markup=config.Geolocate)

    if usr_now.Step == 2:
        usr_now.Step = 3
        bot.send_message(message.chat.id, "Пожалуйства, подтвердите геолокацию", reply_markup=config.Geo_Take)

    if usr_now.Step == 3 and config.Type_filtr(message.text):
        usr_now.Type = message.text
        bot.send_message(message.chat.id, "Бесплатные?", reply_markup=config.Y_N)
        usr_now.Step = 4

    if usr_now.Step == 4 and ["Да", "Нет", "Не имеет значения"].count(message.text) == 1:
        usr_now.Step = 5
        usr_now.Money = (message.text == "Да")
        if message.text == "Не имеет значения":
            usr_now.Money = None

        bot.send_message(message.chat.id, "Это всё", reply_markup=config.Ready)

    if usr_now.Step == 5:
        print(usr_now.Step, usr_now.Type, usr_now.City, usr_now.Money, usr_now.Near)

    if usr_now.Step == 8 and ["Ещё", "Всё", "Заново"].count(message.text) == 1:
        a = message.text
        if a == "Ещё":
            answer = API_kuda.get_next_events_geo(float(usr_now.coord[0]), float(usr_now.coord[1]), usr_now.next_link)
            if answer is None:
                answer = "Событий рядом с Вами найти не удалось."
                bot.send_message(message.chat.id, answer,
                                 reply_markup=config.Ready)
            else:
                message_text = answer[1]
                next = answer[0]
                usr_now.next_link = next
                for i in range(len(message_text)):
                    reply_list = message_text[i]
                    reply = "#" + str(i + 1) + "\n" + reply_list["title"] + "\n" \
                            + cleanhtml(reply_list["description"]) + "\n" + "Время начала мероприятия: " + \
                            datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                                '%Y-%m-%d %H:%M') + "\n" + "Время конца мероприятия: " \
                            + datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                        '%Y-%m-%d %H:%M') + "\n" + "Полное описание мероприятия: " + reply_list["site_url"]

                    bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
                bot.send_message(message.chat.id, "Надеемся, что мы смогли Вам помочь!", reply_markup=config.Ending)
        if a == "Всё":
            bot.send_message(message.chat.id, "бла бла бла 5-10")
        if a == "Заново":
            bot.send_message(message.chat.id, "Ну ты и пидр", reply_markup=config.AGAIN)

@bot.message_handler(content_types=['location'])
def location(message):
    a = message.location
    b = str(a).split(":")
    usr_now.coord = [b[1].split(",")[0][1:], b[2][1:-1]]
    print(usr_now.coord)
    usr_now.Step = 8
    bot.send_message(message.chat.id, "Ищем события для Вас...")
    answer = API_kuda.get_events_geo(float(usr_now.coord[0]), float(usr_now.coord[1]))
    bot.send_message(message.chat.id, "Спасибо за ожидаение!")
    if answer is None:
        answer = "Событий рядом с Вами найти не удалось."
        bot.send_message(message.chat.id, answer,
                         reply_markup=config.Ready)
    else:
        message_text = answer[1]
        next = answer[0]
        usr_now.next_link = next
        for i in range(len(message_text)):
            reply_list = message_text[i]
            reply = "#" + str(i + 1) + "\n" + reply_list["title"] + "\n" \
                    + cleanhtml(reply_list["description"]) + "\n" + "Время начала мероприятия: " + \
                    datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                        '%Y-%m-%d %H:%M') + "\n" + "Время конца мероприятия: " \
                    + datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                '%Y-%m-%d %H:%M') + "\n" + "Полное описание мероприятия: " + reply_list["site_url"]

            bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
        bot.send_message(message.chat.id, "Надеемся, что мы смогли Вам помочь!", reply_markup=config.Ending)
    usr_now.Step = 8

if __name__ == '__main__':
    bot.polling(none_stop=True)
