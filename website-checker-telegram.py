import time
import csv
import requests # pip install requests
import configparser  # pip install configparser
import telebot # pip install pyTelegramBotAPI
import colorama # pip install colorama
from colorama import Fore, Style
colorama.init()

config = configparser.ConfigParser()  # создаём объекта парсера
config.read('settings.ini')  # настройки api telegram

bot = telebot.TeleBot(config['Telegram']['api'])  # настройки api нашего БОТА telegram
bot.send_message(config['Telegram']['telegramUserId'], 'Бот запущен') # оповещаем что запустили бота можно и удалить
while True:
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

    with open('data.csv', newline='') as filesite:
        reader = csv.reader(filesite)
        for row in reader:
            try:
                response = requests.get(row[1], timeout=8)  #таймер ожидания ответа от страницы 8 сек
                checkerror(int(response.status_code))
            except:
                print(Fore.RED)
                print("Ошибка! " + row[1])
                bot.send_message(config['Telegram']['telegramUserId'], 'Ошибка!  ' + row[1])
                print(Style.RESET_ALL)

    time.sleep(int(config['Settings']['sleeptime'])) #таймер сна в сеундах после заного пойдет сканировать сайты
bot.polling(none_stop=True, interval=0)
