#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import argparse

# читаем csv и записываем список словарей для последующей сверки
def get_from_csv(full_path):
    list_dicts = []
    with open(full_path) as f:
        reader = csv.DictReader(f)
        for dict in reader:
            if re.search('FALSE|ЛОЖЬ', dict['Перенесено?']) and dict['Хост'] != '':
                list_dicts.append(dict)
    return list_dicts

# читаем основной файл конфигурации с которого нужно перенести хосты, проходимся по нему 
# регулярными выражениями со значениями из словарей выше, после результат пишем в файл.
list_objects = []
with open('manager.conf', 'r+') as conf:
    content = conf.read()
    content_origin = content
    for dict in list_dicts:
        check_name = dict['Чек']
        re_pattern = re.compile('^.+\"' + check_name + '\".+\{(.+\n|\n.+)*?\}', flags=re.MULTILINE)
        match = re.search(re_pattern, content)
        if match != None:
            list_objects.append(match.group(0))
            content = re.sub(re_pattern, '', content)
    content = re.sub('(?<=^\n)\n', '', content, flags=re.MULTILINE)
    # conf.seek(0)
    # conf.truncate()
    # conf.write(content)
    
# Цикл по каждому полученному объекту изменяем в нем хост назначения.
    list_objects_with_changed_host = []
    for ic2_object in list_objects:
        for dict in list_dicts:
            check_name = dict['Чек']
            check_host = dict['Хост']
            re_pattern = re.compile('^.+\"' + check_name + '\".+\{(.+\n|\n.+)*?\}', flags=re.MULTILINE)
            match_check = re.search(re_pattern, ic2_object)
            if match_check != None:
                re_pattern = re.compile('(?<=host_name = \")\w+')
                ic2_mod_object = (re.sub(re_pattern, check_host, ic2_object))
                list_objects_with_changed_host.append(ic2_mod_object)
                continue
    


    
# Проверяем каждый объект - хост назначения также становится файлом конфига, куда требуется записать объекты.
def object_to_file(ic2_object):
    match = re.search('(?<=host_name = \")\w+', ic2_object)
    with open(match.group(0) + ".conf", 'a+') as config:
        config.seek(0)
        content = config.read()
        re_pattern = re.compile(re.escape(ic2_object), flags=re.MULTILINE)
        match = re.search(re_pattern, content)
        if match != None:
            print(match, ": already present in file")
        else:
            config.write(ic2_object + '\n\n')


def set_args():
    parser = argparse.ArgumentParser(description='Transfer icinga2 checks from one config to others by get destination form csv file')
    parser.add_argument('--csv', type=str, required=True, help='Path to csv icinga2 checks transfer file')
    parser.add_argument('--from', type=str, required=True, help='The name or full path of config which from we a transfer icinga2 checks')
    arguments = parser.parse_args()
    return(arguments)
            
for ic2_object in list_objects_with_changed_host:
    object_to_file(ic2_object)

args = set_args()
CSV_DICTS = get_from_csv(args.csv)
