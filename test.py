import os
import json
import datetime
import time
import sched
import pandas as pd
import xml.etree.ElementTree as ET
from pytest import warns

from winsdk.windows.ui.notifications import ToastNotification, ToastNotificationManager

from windows_toasts import ToastActivatedEventArgs, ToastDuration
from windows_toasts.toast_document import ToastDocument
from windows_toasts import WindowsToaster, ToastText1

with open("test.json") as f:
    data=json.loads(f.read())
    for i in data:
        if i['completed'] == False:
            calculated_rem=datetime.timedelta(seconds=i['kalan'])
            print(calculated_rem)
            if calculated_rem < datetime.timedelta(minutes=15):
                wintoaster = WindowsToaster('Ders Başlıyor')
                newToast = ToastText1()
                newToast.SetBody(f'{i["class_name"]}\n{i["class_place"]}\n{i["start_hour"]}:{i["start_min"]}')
                newToast.on_activated = lambda _: print('Toast clicked!')
                wintoaster.show_toast(newToast)

            break #because of the json file is sequential
        else:
            continue 