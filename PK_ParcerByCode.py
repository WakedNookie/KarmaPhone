#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Set-Location -Path "E:\_WORK\PhoneKarma\Python\_VM" -PassThru
# python PK_ParcerByCode.py

# Known issues: 
# 1. 'charmap' codec can't encode character '\xb2' in position 5: character maps to <undefined>
# 2. \n corrently saved in JSON

import sys
import json
import datetime
from datetime import date, timedelta
import urllib
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import time
import traceback

from PK_DB import PK_DB

# Initialize DB
db = PK_DB('PhoneKarmaDB.db')

Number = ''
Source = ''
Status = ''
Statuses = {
    "Positive": 0,
    "Neutral": 0,
    "Negative": 0
        }
Comments = {}
obtdata = pd.DataFrame(columns = ['Number','Source','Status','Statuses','Comments'])
jsondata = {}

#URL для парсинга:
sources = [
    'nbt.ru',
    'ish.com',
    'testsite.ru',
    'testsite2.ru'
]

def PhoneParser(phone):
	start = datetime.datetime.now()
	print(start.strftime("%Y.%m.%d %H:%M:%S"), ' All set up, start async parcing all known resources: ')
	for s in sources:
	    print(s)
	print('.............')
	phoneslist = [i for i in range(int(phonecode)*10000000,(((int(phonecode)+1)*10000000)-1))]
	# print(phoneslist)
	for phone in phoneslist:
		print(phone)
		for s in sources:
		    time.sleep(3)
		    Number = phone
		    if (s == 'nbt.ru'):
		        try:
		            Statuses = {
		                "Positive": 0,
		                "Neutral": 0,
		                "Negative": 0
		                    }
		            Comments = {}
		            jsondata = {}
		            Source = 'nbt.ru'
		            nbtURL = 'https://www.neberitrubku.ru/nomer-telefona/8%s/' % (phone) #получаем URL для парсинга
		            # print(nbtURL)
		            req = urllib.request.Request(nbtURL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
		            page = urllib.request.urlopen(req)
		            # page = urllib.request.urlopen (URL) #скачиваем страницу
		            soup = BeautifulSoup (page, 'html.parser') #загружаем скачанную страницу в суп
		            if soup.find('div', {'class': 'score negative'}) != None:
		                Status = "Negative"
		            elif soup.find('div', {'class': 'score positive'}) != None:
		                Status = "Positive"
		            elif soup.find('div', {'class': 'score neutral'}) != None:
		                Status = "Neutral"
		            elif soup.find('div', {'class': 'score unknown'}) != None:
		                Status = "Unknown"
		            else:
		                Status = "Error"

		            if Status == ("Negative" or "Positive" or "Neutral"):
		                statblock = soup.find('div', {'class': 'ratings'})
		                for tag in statblock.find_all("li"): # Для каждой строки li class
		                    if  re.findall(r'[а-я]+', tag.text)[0] == 'положительная':
		                        Statuses.update({"Positive": int(re.findall(r'\d+', tag.text)[0])})
		                    elif re.findall(r'[а-я]+', tag.text)[0] == 'нейтральная':
		                        Statuses.update({"Neutral": int(re.findall(r'\d+', tag.text)[0])})
		                    elif re.findall(r'[а-я]+', tag.text)[0] == 'отрицательная':
		                        Statuses.update({"Negative": int(re.findall(r'\d+', tag.text)[0])})
		            
		                reviewsblock = soup.find('div', {'class': 'containerReviews'})
		                
		                for review in reviewsblock.select("div[class=review]"): # Для каждого отзыва
		                    if review.find('div', {'class': 'score negative'}) != None:
		                        RStatus = "Negative"
		                    elif review.find('div', {'class': 'score positive'}) != None:
		                        RStatus = "Positive"
		                    elif review.find('div', {'class': 'score neutral'}) != None:
		                        RStatus = "Neutral"
		                    elif review.find('div', {'class': 'score unknown'}) != None:
		                        RStatus = "Unknown"
		                    else:
		                        RStatus = "Error"

		                    RType = review.find('span', {'itemprop': 'name'}).text
		                    RComment = review.find('span', {'itemprop': 'description'}).text

		                    Comments.update({str(review["data-reviewid"]): {"Status": RStatus, "Type": RType,"Comment": RComment}}) #вот эту строку наполняем
		                print(Comments)
		           
		            jsondata.update({'Number': Number, 'Source': Source, 'Status': Status, 'Statuses': Statuses, 'Comments': Comments})

		            filetime = datetime.datetime.now()
		            with open(str(Number) + "_" + str(Source) + ".json", "w", encoding='utf8') as write_file:
		                json.dump(jsondata, write_file, ensure_ascii=False)
		        # except Exception as e:
		        #     print(getattr(e, 'message', repr(e)))
		        #     print(getattr(e, 'message', str(e)))
		        except:
		        	print(traceback.format_exc())

		    if (s == 'ish.com'):
		        try:
		            Statuses = {
		                "Positive": 0,
		                "Neutral": 0,
		                "Negative": 0
		                    }
		            Comments = {}
		            jsondata = {}
		            Source = 'ish.com'
		            ishPhone = "7"+str(phone)
		            # print(ishPhone)
		            iURL = db.get_URL(ishPhone)
		            # print(iURL)
		            ishURL = 'https://xn--80ajiff1g.com/%s%s' % (iURL[0],ishPhone) #получаем URL для парсинга
		            # print(ishURL)
		            req = urllib.request.Request(ishURL, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
		            ishPage = urllib.request.urlopen(req)
		            # ishPage = urllib.request.urlopen (ishURL) #скачиваем страницу
		            ishSoup = BeautifulSoup (ishPage, 'html.parser') #загружаем скачанную страницу в суп

		            # print((ishSoup.find('th', text='Общий рейтинг').parent.td.text))
		            if str(ishSoup.find('th', text='Общий рейтинг').parent.td.text) == "Неизвестно":
		                ishStatus = "Unknown"
		            elif int(ishSoup.find('th', text='Общий рейтинг').parent.td.text) < 0:
		                ishStatus = "Negative"
		            elif int(ishSoup.find('th', text='Общий рейтинг').parent.td.text) > 0:
		                ishStatus = "Positive"
		            elif int(ishSoup.find('th', text='Общий рейтинг').parent.td.text) == 0:
		                ishStatus = "Neutral"
		            else:
		                ishStatus = "Error"
		            # print(ishStatus)
		            if ishStatus == ("Negative" or "Positive" or "Neutral"):
		            	ishNegRCnt = 0
		            	ishPosRCnt = 0
		            	ishNeuRCnt = 0
		            	ishCommCnt = 0
		            	for ishComment in ishSoup.select("div[class=comment]"):
		            		# print(ishComment.find('div', {'class': 'rating'}).text[15:])
		            		if int(ishComment.find('div', {'class': 'rating'}).text[15:]) < 0:
		            			ishRStatus = "Negative"
		            			ishNegRCnt = ishNegRCnt + 1
		            		elif int(ishComment.find('div', {'class': 'rating'}).text[15:]) > 0:
		            			ishRStatus = "Positive"
		            			ishPosRCnt = ishPosRCnt + 1
		            		elif int(ishComment.find('div', {'class': 'rating'}).text[15:]) == 0:
		            			ishRStatus = "Neutral"
		            			ishNeuRCnt = ishNeuRCnt + 1
		            		else:
		            			ishRStatus = "Error"
		            		# print(ishRStatus)

		            		ishRType = ishComment.find('div', {'class': 'type'}).text[12:]
		            		ishRComment = ishComment.find('div', {'class': 'text'}).text[12:]
		            		# print(ishRType, ishRComment)
		            		Statuses.update({"Negative": ishNegRCnt,
		            			"Positive": ishPosRCnt,
		            			"Neutral": ishNeuRCnt
		            			})

		            		Comments.update({ishCommCnt: {"Status": ishRStatus, "Type": ishRType,"Comment": ishRComment}})
		            		ishCommCnt = ishCommCnt + 1
		            	print(Comments)
		           
		            jsondata.update({'Number': Number, 'Source': Source, 'Status': Status, 'Statuses': Statuses, 'Comments': Comments})

		            filetime = datetime.datetime.now()
		            with open(str(Number) + "_" + str(Source) + ".json", "w", encoding='utf8') as write_file:
		                json.dump(jsondata, write_file, ensure_ascii=False)

		        # except Exception as e:
		        #     print(getattr(e, 'message', repr(e)))
		        #     print(getattr(e, 'message', str(e)))
		        except:
		        	print(traceback.format_exc())



		finish = datetime.datetime.now()
		print('----======:::::::======----')
		print(finish.strftime("%Y.%m.%d %H:%M:%S"), "Number ", phone, " parsed.")
		# return 

# try:
# 	while True:
phonecode = (sys.argv[1])
		# phone = input("Enter 10 digit phone number in format '9XXYYYZZZZ' to check: ") or "AAA"
		# print(len(str(phone)), phone[0])
if len(str(phonecode)) == 3 and phonecode[0] == "9" and phonecode.isdigit():
	PhoneParser(phonecode)
elif phonecode[0] != "9":
	print("Try another CODE that starts with 9 and its format is '9XX'")
elif len(str(phonecode)) != 3:
	print("Try another CODE that has 3 digits and its format is '9XX'")
elif phonecode.isdigit() == False:
	print("CODE can contain only digits. Enter 3 digit phone CODE in format '9XX'")
else:
	print("Unknown error. Please, try again.")
# except KeyboardInterrupt:
# 	pass

