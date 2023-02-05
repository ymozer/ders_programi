import os
import time
import pandas as pd
import xml.etree.ElementTree as ET
from pytest import warns

from winsdk.windows.ui.notifications import ToastNotification, ToastNotificationManager

from windows_toasts import ToastActivatedEventArgs, ToastDuration
from windows_toasts.toast_document import ToastDocument


def toast():
    from windows_toasts import WindowsToaster, ToastText1
    wintoaster = WindowsToaster('Ders Başlıyor')
    newToast = ToastText1()
    newToast.SetBody('CSE254')
    newToast.on_activated = lambda _: print('Toast clicked!')
    wintoaster.show_toast(newToast)

def parse_xml():
    xml_str=''

    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    tree = ET.parse("../DersProgramiOgrenci.xml")
    root = tree.getroot()      
    root.attrib.pop("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
    root.attrib.pop("Name")

    with open("../DersProgramiOgrenci_new.xml", 'wb') as f:
        tree.write(f, encoding='utf-8')

    with open("../DersProgramiOgrenci_new.xml", 'r+',encoding='utf-8') as f:
        xml_str=f.read()
        xml_str=xml_str.replace('ns0:','')
    
    with open("../DersProgramiOgrenci_new.xml", 'w+',encoding='utf-8') as f:
        f.write(xml_str)


if __name__=="__main__":
    parse_xml()
    toast()
