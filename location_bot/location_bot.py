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


usr_now = GetInformation()
bot = telebot.TeleBot(config.token)


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@bot.message_handler(commands=["start"])
def img_ids(message):
    bot.send_message(message.chat.id, "Привет")
    usr_now.Step = 2


@bot.message_handler(content_types=["text"])
def events(message):
    pass


@bot.message_handler(content_types=['location'])
def location(message):
    a = message.location
    b = str(a).split(":")
    usr_now.coord = [b[1].split(",")[0][1:], b[2][1:-1]]
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
                    + clean_html(reply_list["description"]) + "\n" + "Время начала мероприятия: " + \
                    datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                        '%Y-%m-%d %H:%M') + "\n" + "Время конца мероприятия: " \
                    + datetime.datetime.fromtimestamp(int(reply_list["dates"][0]["start"])).strftime(
                '%Y-%m-%d %H:%M') + "\n" + "Полное описание мероприятия: " + reply_list["site_url"]

            bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
        bot.send_message(message.chat.id, "Надеюсь, что смог Вам помочь!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
