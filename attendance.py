import pyttsx3 as textSpeach
from datetime import date
from datetime import datetime
today = date.today()
now = datetime.now()
import gspread
engine = textSpeach.init()

def MarkAttendence(name):
    date = today.strftime('%m/%d/%Y').replace('/0', '/')
    if (date[0] == '0'):
        date = date[1:]
    time = now.strftime('%H:%M:%S')
    sheetname=(name.lower())
    print(sheetname)
    statment = str('welcome to work' + name)
    engine.say(statment)
    engine.runAndWait()
    sa = gspread.service_account("attservice.json")
    sh = sa.open("attendance")
    wks = sh.worksheet(sheetname)
    namecell = wks.find(date)
    if wks.cell(namecell.row, 2).value == '0':
        wks.update_cell(namecell.row,2, time)
    else:
        wks.update_cell(namecell.row,3, time)





