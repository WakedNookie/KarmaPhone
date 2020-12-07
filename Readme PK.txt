Подключить пакеты Python3:
json
datetime
urllib
bs4
requests
re
pandas
numpy
time

Файлы:
PhoneKarma_Parcer.py - основной файл парсера. Запускается командой python3 PK_ParcerByCode.py XXX, 
где XXX - трехзначный код, начинающийся с 9. парсит все данные о номерах с запрошенным кодом. 

Isheyka_DB.py - модуль подключения базы данных

PhoneKarmaDB.db - база данных SQlite. В ней хранятся индивидуальные ссылки для парсинга Ищейки

Текущий принцип работы:
Запускается командой python3 PK_ParcerByCode.py XXX, где XXX - трехзначный код, начинающийся с 9.
