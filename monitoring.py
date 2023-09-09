#-*- coding: utf-8 -*- 
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime
import psutil
from gpiozero import CPUTemperature

#path 담긴 파일
from myPath import myPath

now = datetime.now()
weekday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
#경고 끄기
import warnings
warnings.filterwarnings('ignore')

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
# JSON Key File Path
json_key_path = myPath["jsonPath"]

credential = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
gc = gspread.authorize(credential)

#Google Sheet URL
spreadsheet_url = myPath["sheetUrl"]
doc = gc.open_by_url(spreadsheet_url)

#요일별로 다른 시트 사용
sheet = doc.worksheet(weekday[now.weekday()])

#A2 ~ A(n+2): 00시00분부터 23:59까지 기록.
#0시 00분 = A2이므로 line = Hour*60 + Minute + 2
#B열=CPU, C열=RAM, D열=TEMP

cpu_usage = psutil.cpu_percent()
ram_usage = psutil.virtual_memory().percent
temp = round(CPUTemperature().temperature,1)

line = str(now.hour*60 + now.minute + 2)

#00시 00분에 sheet clear후 다시 만들기
if line=="2":
    sheet.batch_clear(["A2:D1500"])
    sheet.update("E5",[[now.strftime("%Y/%m/%d")]])

sheet.update("A"+line,[[now.strftime("%H:%M"),cpu_usage,ram_usage,temp]])