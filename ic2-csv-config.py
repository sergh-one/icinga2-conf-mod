#!/usr/bin/python3

import csv
import re

list_dicts = []
with open('checks.csv') as f:
    reader = csv.DictReader(f)
    for dict in reader:
        if dict['Перенесено?'] == 'FALSE':
            list_dicts.append(dict)

list_objects = []
with open('manager.conf', 'r+') as conf:
    content = conf.read()
    for dict in list_dicts:
        check_name = dict['Чек']
        re_pattern = re.compile('^.+' + check_name + '.+\{(\n.+)+\n\}$', flags=re.MULTILINE)
        match = re.search(re_pattern, content)
        list_objects.append(match)
        if match != None:
            print(match.group())
