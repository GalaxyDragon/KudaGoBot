import requests
from flask import json


def get_events_geo(lat, lon, radius=1000):
   #  """
   # :param lat: координата
   # :param lon: другая координата(по-моему первое широта второе долгота, но фигач также, как в телеграмме, они в таком
   # же порядке)
   # :param radius: радиус, в котором будут найдены мероприятия(необязательны параметр), если нет никаких мероприятий в
   # заданном радиусе, то он будет расширен на 1000 метров
   # :return: ссылка на следующую страницу и 5 результатов на текущей странице
   # """
    link = "https://kudago.com/public-api/v1.3/events/?lat=" + str(lat) + "&lon=" + str(lon) + "&radius=" + \
           str(radius) + "&page_size=5&fields=dates,title,description,site_url"
    answer = requests.get(link).text
    answer = json.loads(answer)
    while True:
        if answer["next"] is not None and answer["results"] is not None:
            return answer["next"], answer["results"]
        else:
            radius += 1000
            link = "https://kudago.com/public-api/v1.3/events/?lat=" + str(lat) + "&lon=" + str(lon) + "&radius=" + \
                   str(radius) + "&page_size=5&fields=dates,title,description,site_url"
            answer = requests.get(link).text
            answer = json.loads(answer)


def get_next_events_geo(lat, lon, next_link):
    answer = requests.get(next_link).text
    answer = json.loads(answer)
    radius = next_link.split("=")
    radius = radius[len(radius) - 1]
    while True:
        if answer["next"] is not None and answer["results"] is not None:
            return answer["next"], answer["results"]
        else:
            radius += 1000
            __link = "https://kudago.com/public-api/v1.3/events/?lat=" + str(lat) + "&lon=" + str(lon) + "&radius=" + \
                     str(radius) + "&page_size=5&fields=dates,title,description,site_url"
            answer = requests.get(__link).text
            answer = json.loads(answer)