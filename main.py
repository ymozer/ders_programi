import os
import json
import datetime
import time
import pandas as pd
import xml.etree.ElementTree as ET
from pytest import warns

from winsdk.windows.ui.notifications import ToastNotification, ToastNotificationManager

from windows_toasts import ToastActivatedEventArgs, ToastDuration
from windows_toasts.toast_document import ToastDocument
from windows_toasts import WindowsToaster, ToastText1


time_dict={
    0 : "Pazartesi",
    1 : "Salı",
    2 : "Çarşamba",
    3 : "Perşembe",
    4 : "Cuma",
    5 : "Cumartesi",
    6 : "Pazar"
}

def datettime():
    now_seconds=time.time()
    now=get_time()
    now_split=now.strip().split()
    print(now_split)
    print(time_struct)
    all_classes=semester_setup()
    
    for i in all_classes:  
        print(i['Başlangıç Saati'])

def get_time():
    time_struct=time.gmtime()
    day=time_struct.tm_mday
    month=time_struct.tm_mon
    year=time_struct.tm_year
    week_day=time_struct.tm_wday
    hour=time_struct.tm_hour
    minute=time_struct.tm_min
    seconds=time_struct.tm_sec
    return (f"{time_dict[week_day]} {day}.{month}.{year} {hour+3}:{minute}::{seconds}")

def toast():
    
    wintoaster = WindowsToaster('Ders Başlıyor')
    newToast = ToastText1()
    newToast.SetBody('CSE254')
    newToast.on_activated = lambda _: print('Toast clicked!')
    wintoaster.show_toast(newToast)

def semester_setup():
    '''
    13 Şubat 2023 - 28 Mayıs 2023
    '''
    #(year, month, day,* hour, minute, second,* weekday, day of the year, daylight saving)
    #https://asd.gsfc.nasa.gov/Craig.Markwardt/doy2023.html
    week=datetime.timedelta(weeks=1)
    semester_end = (2023, 5, 30, 0, 0, 0, 1, 150, 0)
    semester_start = (2023, 2, 13, 0, 0, 0, 0, 44, 0)
    
    # convert time_tuple to seconds since epoch
    semester_end_seconds= time.mktime(semester_end)
    semester_start_seconds = time.mktime(semester_start)


    all_classes=[]
    xml_list=parse_xml()
    count=0

    #hafta
    for i in range(int(semester_start_seconds),int(semester_end_seconds), int(week.total_seconds())):
        count2=0

        # hafta içersindeki ders sayısı-Gün rastgele seçilmiş. param fark etmez.
        for j in xml_list['Gün']:
            seconds=datetime.timedelta(seconds=i).total_seconds() # pazartesi saniye sayısı
            count=count+1
            # pazartesiye günleri ekle. aynı haftada 1den fazla eklenmemeli.
            a=0
            match j:
                case 'Pazartesi':
                    a=0
                case 'Salı':
                    a=1
                case 'Çarşamba':
                    a=2
                case 'Perşembe':
                    a=3
                case 'Cuma':
                    a=4
                case 'Cumartesi':
                    a=5
                case 'Pazar':
                    a=6
            
            seconds=seconds+a*60*60*24

            # pazartesiye saatleri ekle
            seconds=seconds+(60*60*int(xml_list['Başlangıç Saati'][count2][0:2]))
            # pazartesiye dakikaları ekle
            seconds=seconds+(60*int(xml_list['Başlangıç Saati'][count2][3:5]))
            tarih_struct=time.localtime(seconds)
            tarih=f"{tarih_struct.tm_mday}/{tarih_struct.tm_mon}/{tarih_struct.tm_year} {tarih_struct.tm_hour}:{tarih_struct.tm_min}"
            test={
                "id": count,
                "Başlangıç Saati": xml_list['Başlangıç Saati'][count2],
                "Bitiş Saati": xml_list['Bitiş Saati'][count2],
                "Gün": xml_list['Gün'][count2],
                "Tarih": tarih,
                "Ders Kodu-Adı": xml_list['Ders'][count2],
                "Derslik": xml_list['Derslik'][count2],
                "Tamamlandı mı?": False
            }
            all_classes.append(test)
            count2=count2+1

    json_object = json.dumps(all_classes, indent = 4,ensure_ascii=False).encode('utf8') 
    with open('test.json','w',encoding='utf-8') as f:
        f.write(json_object.decode())
    return all_classes

def parse_xml():
    xml_str=''

    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    tree = ET.parse("DersProgramiOgrenci.xml")
    root = tree.getroot()      
    root.attrib.pop("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
    root.attrib.pop("Name")

    with open("DersProgramiOgrenci_new.xml", 'wb') as f:
        tree.write(f, encoding='utf-8')

    with open("DersProgramiOgrenci_new.xml", 'r+',encoding='utf-8') as f:
        xml_str=f.read()
        xml_str=xml_str.replace('ns0:','')
    
    with open("DersProgramiOgrenci_new.xml", 'w+',encoding='utf-8') as f:
        f.write(xml_str)

    test={
        'Gün': [],
        'Başlangıç Saati': [],
        'Bitiş Saati': [],
        'Ders': [],
        'Derslik': []
    }

    tree = ET.parse("DersProgramiOgrenci_new.xml")
    root = tree.getroot()      

    for i in range(1,8):
        for j in root.findall(f".//*[@GunAd='{time_dict[i-1]}']/Details3_Collection/Details3"):
            test['Gün'].append(time_dict[i-1])
            test['Başlangıç Saati'].append(j.attrib['Textbox13'])
            test['Bitiş Saati'].append(j.attrib['Textbox15'])
            test['Ders'].append(j.attrib['AdSoyad2'])
            test['Derslik'].append(j.attrib['MekanParentKodAd'])
    #json_object = json.dumps(test, indent = 4,ensure_ascii=False).encode('utf8') 
    #print(json_object.decode())
    return test



if __name__=="__main__":
    semester_setup()
    print(get_time())
    datettime()
    #toast()

