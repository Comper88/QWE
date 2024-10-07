import os
import sys

from types import NoneType
from typing import Any

from rich import console
from rich.table import Table

import json
import toml


# Настройка консоли
CURENT_CMD = console.Console()

# Константы
TYPE_TO_TEXT = {
    str: 'String',
    int: 'Number',
    float: 'Number',
    bool: 'bool',
    list: 'Array',
    NoneType: 'null',
}
BASE_PATH           = os.path.dirname(os.path.abspath(__file__))
BACKUP_PATH         = os.path.join(BASE_PATH, 'backups')
PATH_TO_SETTINGS    = os.path.join(BASE_PATH, '.toml')
PATH_TO_DATABASE    = os.path.join(BASE_PATH, '.json')
EMOJI = [
    '❤ (^ᵥ^)',      # Спасибо!
    '🧪 (Ộ˰0)',     # Возможное решение
    '❌ (>˰<)',     # Ошибка!
    '🛠 ( Ộ˰0)//',   # Чинит!
]


# Константы
HELP_TEXT = '''
[#af00ff]♥ (^ᵥ^)  <- QWERTY (она тебя будет сопроваждать в QWE!)[/]

[violet]Получение данных:[/]
[green]* 11[/]       - [yellow]Список всех категорий[/]
[green]* 12[/]       - [yellow]Зайти в категорию категорий[/]
[green]* 13[/]       - [yellow]Список полей категории[/]

[violet]Запись данных:[/]
[green]* 21[/]       - [yellow]Создать новую категорию[/]
[green]* 22[/]       - [yellow][/]
[green]* 23[/]       - [yellow][/]

[violet]Консоль:[/]
[green]* 31 [/]       - [yellow]Отчистка консоли[/]
[green]* 32 [/]       - [yellow]Выход[/]
[green]* 33 [/]       - [yellow]Помощь[/]
[green]* 34 [/]       - [yellow]Запускает ".json" в VS Code[/]

[violet]Показывает этот текст:[/]
[green]* 33[/]
[green]* /?[/]
[green]* help[/]
'''[1:-1]



# Возвращение к последнему бекакпу
def reloadToBackup():
    from datetime import datetime

    global BACKUP_PATH
    global CURENT_CMD
    global EMOJI

    names = os.listdir(BACKUP_PATH)

    # Если есть бекапы
    if names.__len__():
        dates = [datetime.strptime(name, "%d.%m.%Y") for name in names]
        afterDate = max(dates)
        strAfterDate = afterDate.strftime("%d.%m.%Y")
        pathToAfterFile = os.path.join(BACKUP_PATH, strAfterDate)
        
        with open(pathToAfterFile, 'r', encoding='utf-8') as fromFile:
            with open(PATH_TO_DATABASE, 'w', encoding='utf-8') as toFile:
                toFile.write( fromFile.read() )

    # Если бекапов нет
    else:
        CURENT_CMD.print(
            "[red]Синтуация хуёвая... Бекапов нет, но вы держиетсь[/]\n"
            f"[red]{EMOJI[4]}[/]\n"
            "[red][/]\n"
        )


# Тест проверка наличия .toml
def loadSettings():
    global SETTINGS_QWE
    global CURENT_CMD
    global PATH_TO_SETTINGS
    global EMOJI

    # Попытка найти настройки .toml
    if os.path.exists(PATH_TO_SETTINGS):
        with open(PATH_TO_SETTINGS, 'r', encoding='utf-8') as file:
            SETTINGS_QWE = toml.load(file)
    else:
        CURENT_CMD.print(f'[red]{EMOJI[2]} Ошибка! <- Файл с настройками ".toml" не найден! Поченить? (Y/N <- Y по умолчанию)')

        match input('>> '):
            case 'N' | 'n':
                exit(1)
            
            case _:
                CURENT_CMD.print(f'[yellow]{EMOJI[3]} Исправляю проблему...')

                with open('.toml', 'w', encoding='utf-8') as file:
                    file.write('# Тут будут настройки QWESAS')


# Тест проверка наличия .json
def loadDataBase():
    global SETTINGS_QWE
    global CURENT_CMD
    global PATH_TO_DATABASE
    global EMOJI

    # Попытка найти настройки .json
    if os.path.exists(PATH_TO_DATABASE):
        with open(PATH_TO_DATABASE, 'r', encoding='utf-8') as file:
            SETTINGS_QWE = json.load(file)
    else:
        CURENT_CMD.print(
            f'[red]{EMOJI[2]} Ошибка! <- База данных ".json" не найдена!\n'
            'Отутствие файла означает потерю всех недавно-записанных паролей[/]\n'
            '[yellow]1 - Можно найти уцелевшие пароли в бекапах\n'
            '2 - А можно создать файл\n'
            'q - Отмена[/]\n'
            "Что выбрать? (1/2/q, 1 - по умолчанию, q - выход)"
        )

        match input('>> '):
            case '2':
                CURENT_CMD.print(f'[yellow]{EMOJI[3]} Исправляю проблему...')
                
                with open(PATH_TO_DATABASE, 'w', encoding='utf-8') as file:
                    file.write("{}")
            
            case 'q':
                exit(0)
            
            case _:
                reloadToBackup()


# Вывод списка файлов
def printCategory(dataBase: dict):
    table = Table(border_style='green', caption_style='green', title_justify='left', title_style='green')

    table.add_column('Название категорий')

    for key in dataBase:
        table.add_row(key)

    CURENT_CMD.print(table)


# Зайти в категорию
def changeCategory(dataBase: dict):
    table = Table(border_style='green', caption_style='green', title_justify='left', title_style='green')

    table.add_column('Категории')
    table.add_column('Поля')
    table.add_column('Тип поля')
    table.add_column('Значение поля')

    categorys: list[str] = []
    fields: list[list[str, str, Any]] = []

    # Получение категорий и полей
    for key in dataBase:
        if isinstance(dataBase[key], dict):
            categorys.append(key)
        else:
            t = type(dataBase[key])
            fields.append( (key, TYPE_TO_TEXT[t], dataBase[key]) )
    
    # Вывод
    i = 0
    while 1:
        category = ''
        field = ''

        if len(categorys) > i:
            category = categorys[i]
        
        if len(fields) > i:
            field = fields[i]

        if category == '' and field == '':
            break
        
        if field:
            table.add_row(category, field[0], field[1], str(field[2]))
        else:
            table.add_row(category, '', '', '')

        i += 1

    CURENT_CMD.print(table)


def getDataBaseFile() -> dict:
    with open(PATH_TO_DATABASE, 'r', encoding='utf-8') as file:
        dataBase = json.load(file)

    return dataBase


# Главная
if __name__ == '__main__':
    # Загрузка
    loadSettings()
    loadDataBase()

    # Приглашение
    invitation = '(Система)'

    dataBase = getDataBaseFile()

    while 1:
        CURENT_CMD.print(f'[#34F6C3]{invitation} >> ', end='')
        cmd = input()

        match cmd:
            # Список категорий и полей в текущей директории
            case '11':
                printCategory(dataBase)
            
            # Зайти в категорию
            case '12':
                changeCategory(dataBase)



            # Cls
            case '31':
                os.system('cls')

            # Exit
            case '32':
                exit(0)

            # Help
            case '33' | '/?' | 'help':
                CURENT_CMD.print(HELP_TEXT)

            # VSCODE
            case '34':
                os.system('code ' + PATH_TO_DATABASE)
