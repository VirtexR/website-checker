import csv #pip install csv
import requests #pip install requests
import colorama #pip install colorama
from colorama import Fore, Back, Style
colorama.init()

def checkerror(codeerror):

    print(codeerror)
    if codeerror > 399:
        print(Fore.RED + 'Не найдено :  ' + row[1])
    elif codeerror < 210:
        print(Fore.GREEN + 'ОК:    ' + row[1])
    else:
        print(Fore.RED + 'Не найдена:  ' + row[1])
        return False
    print("=======================================")
    print(Style.RESET_ALL)

with open('data.csv', newline='') as filesite:
    reader = csv.reader(filesite)
    for row in reader:
        try:
            response = requests.get(row[1], timeout=8)
            checkerror(int(response.status_code))
        except:
            print(Fore.RED)
            print("Ошибка! " + row[1])
            print(Style.RESET_ALL)
exitprog = input("Нажмите Enter что бы выйти")
print(exitprog)
