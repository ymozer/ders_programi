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


time_dict = {
    0: "Pazartesi",
    1: "Salı",
    2: "Çarşamba",
    3: "Perşembe",
    4: "Cuma",
    5: "Cumartesi",
    6: "Pazar"
}

time_dict2 = {
    "Pazartesi": 0,
    "Salı": 1,
    "Çarşamba": 2,
    "Perşembe": 3,
    "Cuma": 4,
    "Cumartesi": 5,
    "Pazar": 6
}

def notify():
    '''
    Generate json file with time_till_class() method and read it periodically
    if smallest remaing time of a class that is not 
        completed smaller than specified time:

        then notify user with TOAST.  
    '''
    calculated_rem=datetime.timedelta()
    with open("test.json", "r+",encoding="utf-8") as f:
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
    
   
    
    

def time_till_class():
    now = get_time()
    now_seconds = time.time()
    now_split = now.strip().split()
    all_classes = semester_setup()  # data array
    new_all_classes = []
    for i in all_classes:
        class_info = {
            "id_class": int(i["id"]),
            "class_name": i["Ders Kodu-Adı"],
            "class_place": i["Derslik"],
            "start_hour": int(i["Başlangıç Saati"][0:2]),
            "start_min": int(i["Başlangıç Saati"][3:5]),
            "end_hour": int(i["Bitiş Saati"][0:2]),
            "end_min": int(i["Bitiş Saati"][3:5]),
            "year": int(i["Tarih"][2]),
            "month": int(i["Tarih"][1]),
            "day": int(i["Tarih"][0]),
            "day_verbal": i["Gün"],
            "completed": i["Tamamlandı mı?"],
            "kalan": i["Kalan Zaman"],
        }
        tuplle = (class_info["year"], class_info["month"], class_info["day"], class_info["start_hour"],
                  class_info["start_min"], 0, time_dict2[class_info["day_verbal"]], -1, 0)
        all_classes_struct = time.mktime(tuplle)
        remaining_time = datetime.timedelta(
            seconds=all_classes_struct-now_seconds)
        class_info["kalan"] = remaining_time.total_seconds()
        # Find out if class done 
        if all_classes_struct > now_seconds:
            class_info["completed"] = False
        else:
            class_info["completed"] = True

        new_all_classes.append(class_info)
        json_object = json.dumps(
            new_all_classes, indent=2, ensure_ascii=False).encode('utf8')
        with open('test.json', 'w', encoding='utf-8') as f:
            f.write(json_object.decode())
    return remaining_time


def get_time():
    time_struct = time.gmtime()
    day = time_struct.tm_mday
    month = time_struct.tm_mon
    year = time_struct.tm_year
    week_day = time_struct.tm_wday
    hour = time_struct.tm_hour
    minute = time_struct.tm_min
    seconds = time_struct.tm_sec
    return (f"{time_dict[week_day]} {day}.{month}.{year} {hour+3}:{minute}::{seconds}")


def semester_setup():
    '''
    13 Şubat 2023 - 28 Mayıs 2023
    '''
    # (year, month, day,* hour, minute, second,* weekday, day of the year, daylight saving)
    # https://asd.gsfc.nasa.gov/Craig.Markwardt/doy2023.html
    week = datetime.timedelta(weeks=1)
    semester_end = (2023, 5, 30, 0, 0, 0, 1, 150, 0)
    semester_start = (2023, 2, 13, 0, 0, 0, 0, 44, 0)

    # convert time_tuple to seconds since epoch
    semester_end_seconds = time.mktime(semester_end)
    semester_start_seconds = time.mktime(semester_start)

    all_classes = []
    xml_list = parse_xml()
    count = 0

    # hafta
    for i in range(int(semester_start_seconds), int(semester_end_seconds), int(week.total_seconds())):
        count2 = 0

        # hafta içersindeki ders sayısı-Gün rastgele seçilmiş. param fark etmez.
        for j in xml_list['Gün']:
            seconds = datetime.timedelta(
                seconds=i).total_seconds()  # pazartesi saniye sayısı
            count = count+1
            # pazartesiye günleri ekle. aynı haftada 1den fazla eklenmemeli.

            seconds = seconds+time_dict2[j]*60*60*24

            # pazartesiye saatleri ekle
            seconds = seconds + \
                (60*60*int(xml_list['Başlangıç Saati'][count2][0:2]))
            # pazartesiye dakikaları ekle
            seconds = seconds + \
                (60*int(xml_list['Başlangıç Saati'][count2][3:5]))
            tarih_struct = time.localtime(seconds)
            tarih = (tarih_struct.tm_mday, tarih_struct.tm_mon,
                     tarih_struct.tm_year, tarih_struct.tm_hour, tarih_struct.tm_min)
            test = {
                "id": count,
                "Başlangıç Saati": xml_list['Başlangıç Saati'][count2],
                "Bitiş Saati": xml_list['Bitiş Saati'][count2],
                "Gün": xml_list['Gün'][count2],
                "Tarih": tarih,
                "Ders Kodu-Adı": xml_list['Ders'][count2],
                "Derslik": xml_list['Derslik'][count2],
                "Kalan Zaman": 0.0,
                "Tamamlandı mı?": 'False'
            }
            all_classes.append(test)
            count2 = count2+1
    return all_classes


def parse_xml():
    xml_str = ''

    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    tree = ET.parse("DersProgramiOgrenci.xml")
    root = tree.getroot()
    root.attrib.pop(
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
    root.attrib.pop("Name")

    with open("DersProgramiOgrenci_new.xml", 'wb') as f:
        tree.write(f, encoding='utf-8')

    with open("DersProgramiOgrenci_new.xml", 'r+', encoding='utf-8') as f:
        xml_str = f.read()
        xml_str = xml_str.replace('ns0:', '')

    with open("DersProgramiOgrenci_new.xml", 'w+', encoding='utf-8') as f:
        f.write(xml_str)

    test = {
        'Gün': [],
        'Başlangıç Saati': [],
        'Bitiş Saati': [],
        'Ders': [],
        'Derslik': []
    }

    tree = ET.parse("DersProgramiOgrenci_new.xml")
    root = tree.getroot()

    for i in range(1, 8):
        for j in root.findall(f".//*[@GunAd='{time_dict[i-1]}']/Details3_Collection/Details3"):
            test['Gün'].append(time_dict[i-1])
            test['Başlangıç Saati'].append(j.attrib['Textbox13'])
            test['Bitiş Saati'].append(j.attrib['Textbox15'])
            test['Ders'].append(j.attrib['AdSoyad2'])
            test['Derslik'].append(j.attrib['MekanParentKodAd'])
    return test


if __name__ == "__main__":
    semester_setup()
    s = sched.scheduler()
    while True:
        print("Parse Event Start Time : ", get_time(), "\n")
        event1 = s.enter(60*5, 1, time_till_class, argument=())
        print("Parse Event Created : \n", event1)
        s.run()
        print("Parse Event End Time : ", get_time())        
        
        print("Toast Event Start Time : ", get_time(), "\n")
        event2 = s.enter(1, 1, time_till_class, argument=())
        print("Toast Event Created : \n", event1)
        s.run()
        print("Toast Event End Time : ", get_time())
