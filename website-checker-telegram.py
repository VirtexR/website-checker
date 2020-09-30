import sys
import time
import csv
import requests # pip install requests
import configparser  # pip install configparser
import telebot # pip install pyTelegramBotAPI
import colorama # pip install colorama
from colorama import Fore, Style
colorama.init()

#config = configparser.ConfigParser()  # создаём объекта парсера
#config.read('settings.ini')  # настройки api telegram
#есть ли фаил сеттингс
#   указан ли config['Telegram']['api']
#   указан ли config['Telegram']['telegramUserId']
#   указан ли config['Settings']['sitelist']
#   указан ли config['Settings']['sleeptime']
#есть ли фаил data.csv(config['Settings']['sitelist'])
def stopActions():
    wait = input("Нажми <ENTER> для продолжения...")
    sys.exit(1)

config = configparser.ConfigParser()  # создаём объекта парсера

def checkerror(codeerror):
    print(codeerror)
    if codeerror > 399:
        print(Fore.RED + 'Не найдено :  ' + row[1])
        bot.send_message(config['Telegram']['telegramUserId'], 'Не найдено :  ' + row[1])

    elif codeerror < 210:
        print(Fore.GREEN + 'ОК:    ' + row[1])

    else:
        print(Fore.RED + 'Не найдена:  ' + row[1])
        bot.send_message(config['Telegram']['telegramUserId'], 'Не найдено :  ' + row[1])
        return False
    print("=======================================")
    print(Style.RESET_ALL)

#проверяем есть ли settings.ini
try:
    config.read('settings.ini')
except:
    print('Фаил settings.ini не найден в директории')
    stopActions()

#проверяем есть ли Telegram api
try:
    config['Telegram']['api']
    # проверяем может ли подключиться бот по этому api
    try:
        bot = telebot.TeleBot(config['Telegram']['api'])
    except:
        print('Бот не может подключиться, api не верен')
        stopActions()

except:
    print('telegram api не найден в settings.ini')
    stopActions()


# проверяем пустой ли telegramUserId
try:
    config['Telegram']['telegramUserId']
except:
    print('telegramUserId не найден в settings.ini')
    stopActions()
else:
    bot = telebot.TeleBot(config['Telegram']['api'])
    #bot.send_message(config['Telegram']['telegramUserId'], 'Бот запущен')


try:
    config['Settings']['sitelist']
    print('Открываем: ' + config['Settings']['sitelist'])
except:
    print('Параметр sitelist не найден в settings.ini')
    stopActions()


try:
    if int(config['Settings']['sleeptime']) < 0:
        print('Параметр sleeptime не найден в settings.ini или указан не коректно')
        stopActions()
    else:
        config['Settings']['sleeptime']
except:
    print('Параметр sleeptime не найден в settings.ini или указан не коректно')
    stopActions()


while True:
    try:
        with open(config['Settings']['sitelist'], newline='') as filesite:
            reader = csv.reader(filesite)
            for row in reader:
                try:
                    response = requests.get(row[1], timeout=8)  #таймер ожидания ответа от страницы 8 сек
                    checkerror(int(response.status_code))
                except:
                    print(Fore.RED)
                    print('Ошибка! ' + row[1])
                    print('=======================================')
                    print(Style.RESET_ALL)
                    #если бот не может отправить сообщение
                    try:
                        bot.send_message(config['Telegram']['telegramUserId'], 'Ошибка!  ' + row[1])
                    except telebot.apihelper.ApiTelegramException:
                        print('Ошибка!  ' + row[1])
                        print('Бот не может отправить сообщение, возможно api указан не верно или сервис не доступен')
                        print('=======================================')
                    print(Style.RESET_ALL)

        time.sleep(int(config['Settings']['sleeptime'])) #таймер сна в сеундах после заного пойдет сканировать сайты
    except FileNotFoundError:
        print(config['Settings']['sitelist'] + ' Фаил не найден')
        stopActions()

bot.polling(none_stop=True, interval=0)
