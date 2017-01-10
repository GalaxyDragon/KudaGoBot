import re
import time
import telebot
from sqlalchemy import create_engine
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

bot = telebot.TeleBot(config.token)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@bot.message_handler(commands=["start"])
def img_ids(message):
    usr_id = message.chat.id
    # engine = create_engine("sqlite:///some.db")
    # result = engine.execute(
    #     "select * from "
    #     "employee where user_id = :emp_id",
    #     emp_id=usr_id)
    try:
        engine = create_engine("sqlite:///some.db")
        engine.execute("""insert into employee (user_id) values (:user_id)""", user_id=usr_id)
    except:
        print("юзверь есть")
    engine = create_engine("sqlite:///some.db")
    engine.execute(
        """update employee set user_step = :user_step where user_id = :user_id""",
        user_id=usr_id,
        user_step=1)
    bot.send_message(message.chat.id, "Дратути. Вашу геолокацию плз", reply_markup=config.Geo_Take)


@bot.message_handler(content_types=["text"])
def events(message):
    usr_id = message.chat.id
    do_it = True
    engine = create_engine("sqlite:///some.db")
    try:
        result2 = engine.execute(
            "select * from employee where user_id = :user_id",
            user_id=usr_id)
    except:
        bot.send_message(message.chat.id, "Пожалуйста, начинайте использование с команды /start.")
        do_it = False
    if do_it:
        fet = result2.fetchone()
        step = fet["user_step"]
        if step == 2 and ["Ещё", "Всё", "Заново"].count(message.text) == 1:
            a = message.text
            if a == "Ещё":
                answer = API_kuda.get_next_events_geo(fet["user_len"], fet["user_lon"],
                                                      fet["next_link"])
                if answer is None:
                    answer = "Событий рядом с Вами найти не удалось."
                    bot.send_message(message.chat.id, answer,
                                     reply_markup=config.Ready)
                else:
                    message_text = answer[1]
                    next = answer[0]
                    engine = create_engine("sqlite:///some.db")
                    engine.execute(
                        """update employee set next_link = :next_link where user_id = :user_id""",
                        user_id=usr_id,
                        next_link=next)
                    for i in range(len(message_text)):
                        reply_list = message_text[i]
                        reply = "#" + str(i + 1) + "\n" + reply_list["title"] + "\n" \
                                + cleanhtml(reply_list["description"]) + "\n" + "Полное описание мероприятия: " + reply_list["site_url"]

                        bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
                    bot.send_message(message.chat.id, "Надеемся, что мы смогли Вам помочь!", reply_markup=config.Ending)
                    time.sleep(1)
            if a == "Всё":
                bot.send_message(message.chat.id, "бла бла бла 5-10")
            if a == "Заново":
                bot.send_message(message.chat.id, "Ну ты и мгхазь", reply_markup=config.AGAIN)


@bot.message_handler(content_types=['location'])
def location(message):
    user_location = message.location
    usr_id = message.chat.id

    engine = create_engine("sqlite:///some.db")
    engine.execute(
        """update employee set user_len = (:user_len), user_lon = (:user_lon),
        user_step = (:user_step) where user_id = (:user_id)""",
        user_len=user_location.latitude,
        user_lon=user_location.longitude,
        user_id=usr_id,
        user_step=2)
    bot.send_message(message.chat.id, "Ищем события для Вас...")
    answer = API_kuda.get_events_geo(user_location.latitude, user_location.longitude)
    bot.send_message(message.chat.id, "Спасибо за ожидаение!")
    if answer is None:
        answer = "Событий рядом с Вами найти не удалось."
        bot.send_message(message.chat.id, answer,
                         reply_markup=config.Ready)
    else:
        message_text = answer[1]
        next = answer[0]
        engine = create_engine("sqlite:///some.db")
        engine.execute(
            """update employee set next_link = :next_link where user_id = :user_id""",
            user_id=usr_id,
            next_link=next)
        for i in range(len(message_text)):
            reply_list = message_text[i]
            reply = "#" + str(i + 1) + "\n" + reply_list["title"] + "\n" \
                    + cleanhtml(reply_list["description"]) + "\n" + "Полное описание мероприятия: " + \
                    reply_list["site_url"]

            bot.send_message(message.chat.id, reply, disable_web_page_preview=True)
        bot.send_message(message.chat.id, "Надеемся, что мы смогли Вам помочь!", reply_markup=config.Ending)


if __name__ == '__main__':
    bot.polling(none_stop=True)
