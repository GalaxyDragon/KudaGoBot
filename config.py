from telebot import types

token = '276811217:AAGiU92RPaTzIgfypmvoRrT1PsiIspRk0jE'
main_menu = types.ReplyKeyboardMarkup()
main_menu.row('Окай')
Geolocate = types.ReplyKeyboardMarkup()
Geolocate.one_time_keyboard = True
Geolocate.row("Geo", "No geo")
Geo = types.KeyboardButton
Geo.request_location = True
Geo.text = "Okey"

Geo_Take = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
Geo_Take.add(button_geo)

AGAIN = types.ReplyKeyboardMarkup()
AGAIN.row("/start")

Ending = types.ReplyKeyboardMarkup()
Ending.row("Ещё")
Ending.row("Всё", "Заново")

Place_Type = types.ReplyKeyboardMarkup()
Place_Type.row("Рестораны", "Бары", "Клубы", "Антикафе")
Place_Type.row("Квесты", "Интересные места")
Place_Type.row("Магазины", "Учебки", "Отели", "Музеи")
Y_N = types.ReplyKeyboardMarkup()
Y_N.row("Да", "Нет")
Y_N.row("Не имеет значения")
Ready = types.ReplyKeyboardMarkup()
Ready.one_time_keyboard = True
Ready.row("Ready")


def Type_filtr(word):
    a = ["Рестораны", "Бары", "Клубы", "Антикафе", "Квесты", "Музеи", "Интересные места", "Магазины", "Учебки", "Отели"]
    if a.count(word) == 1:
        return True
    else:
        return False
