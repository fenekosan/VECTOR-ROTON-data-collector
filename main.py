#!/usr/bin/python3
import requests
import json
import sys

def status_mcast():
    ip_roton = (sys.argv[1]) #ip адрес ротона
    mcast = (sys.argv[2]) #ip мультикаста
    s = requests.Session()
    r = s.post('http://'+ip_roton+'/auth/login', data = {'username':'admin', 'password':'admin'}) #авторизация
    r = s.get('http://'+ip_roton+'/get_tree_structure?version=-1&_=') #запрос страницы с json
    j = json.loads(str(r.text)) #парсер строки в тип json
    for key in j[0][0].keys(): #цикл поиска мультикаста на входе ротона
            if ("mcast_ip_addr") in j[0][0][key]["attributes"] : #отсеивание старых не активных входов, в которых нет адреса мультикаста
                    if (j[0][0][key]["attributes"]["mcast_ip_addr"]["value"]) == mcast: #проверка на содержание мультикаста, который мы ищем
                        conf_id = j[0][0][key]["config_id"] #сохрание id найденного входа, который нужен для поиска выхода
    try: #здесь проверяем удалось ли нам найти мультикаст на входе, а если нет то отдаем состояние 2
        if conf_id == "":
            print ("2")
            sys.exit()
    except NameError:
        print("2")
        sys.exit()
    for confkey in j[0][1].keys(): #цикл поиска состояния на выходе
        if ("src_config_id") in j[0][1][confkey]["attributes"]: #отсеиваем старых не активных выходов
            if str(j[0][1][confkey]["attributes"]["src_config_id"]["value"]) == str(conf_id): #ищем выход, в котором испольузуется нужный мультикаст
                print(str(j[0][1][confkey]["attributes"]["src_error"]["value"])) #пишем состояние канала, если 0 все ок, если 1 значит отсутствует поток на входе
    return 0


def status_base():
    ip_roton = (sys.argv[1])#ip адрес ротона
    s = requests.Session()
    r = s.post('http://' + ip_roton + '/auth/login',
               data={'username': 'admin', 'password': 'admin'})  # авторизация
    r = s.get('http://' + ip_roton + '/info/get_node_attributes?node_id=1&_=')  # запрос страницы с json
    j = json.loads(str(r.text))  # парсер строки в тип json
    print (j["board_temperature"]["value"])  #температура платы
    print (j["mb_cpu_temperature"]["value"]) #температура процессора
    print (j["mb_psu_fault"]["value"])  #состояние питания, если 1 то одно из 2 питаний отсутствует
    print (j["board_uptime"]["value"]) #аптайм системы
    print (j["mb_fan_fault_1"]["value"]) #состояние вентилятора, если 1 вентилятор не работает
    print(j["mb_fan_fault_2"]["value"])
    print(j["mb_fan_fault_3"]["value"])
    print(j["mb_fan_fault_4"]["value"])
    print(j["mb_fan_fault_5"]["value"])
    #print (j["mb_link_up_eth0"]["value"]) #состояние линка eth0
    #print(j["mb_link_up_eth1"]["value"])   #состояние линка eth1
    #print(j["mb_fan_monitored_rpm_1"]["value"]) #скорость вращения вентилятора
    #print(j["mb_fan_monitored_rpm_2"]["value"])
    #print(j["mb_fan_monitored_rpm_3"]["value"])
    #print(j["mb_fan_monitored_rpm_4"]["value"])
    #print(j["mb_fan_monitored_rpm_5"]["value"])
    return 0

if (sys.argv[2]) == "base": #основная логика для выбора функции извлечения данных
    status_base() #извлекает основные данные о состоянии устройства
else:
    status_mcast() #извлекает данные о состоянии потока
