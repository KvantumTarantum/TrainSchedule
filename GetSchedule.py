from bs4 import BeautifulSoup
import requests
import sqlite3
import config


def make_station_url(sid=1, sid2=0, lng=''):  # Function for make url to parse
    return 'http://swrailway.gov.ua/timetable/eltrain3-5/?sid={}&sid2={}&startPicker2=&dateR=0&lng={}'\
        .format(sid, sid2, lng)


def print_data(station_name):
    conn = sqlite3.connect(config.stations_database)
    cursor = conn.cursor()
    cursor.execute('SELECT station_id FROM stations WHERE name_ru="%s"' % (station_name))
    station_id = cursor.fetchone()
    if station_id is None:
        return 'Нема такої станції, дебіл'
    else:
        station_id = station_id[0]
    cursor.close()
    conn.close()
    r = requests.get(make_station_url(station_id))
    soup = BeautifulSoup(r.text, 'lxml')
    result = soup.find('table', class_='td_center').find_all('tr', height='20')[2:]
    message = ''
    splitted_message = []
    for schedule_array in result:
        i = schedule_array.text.strip().split('\n')
        message += 'Поїзд: ' + i[0] + '\n' + 'Обіг: ' + i[1] + '\n' + 'Маршрут: ' + i[2] + '\n' + \
                   'Прибуття: ' + i[3] + '\n' + 'Відправлення: ' + i[4] + '\n\n'
        if len(message) > 2700:
            splitted_message.append(message)
            message = ''
    splitted_message.append(message)
    return splitted_message


if __name__ == '__main__':
    print_data(265)
