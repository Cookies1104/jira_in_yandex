import pandas as pd
import json


data = pd.read_excel('./Excel.xlsx', sheet_name='Your Jira Issues')
data = data.to_json(path_or_buf='issues.json', indent=1, index=False, orient='table', force_ascii=True)
final_storage = []

with open('issues.json') as f:
    new_data = json.load(f)
    for element in new_data['data']:
        description = (
            'Связанные задачи: ' + str(element['Связанные задачи']) + '. Статус: ' + str(element['Статус']) +
            '. Автор: ' + str(element['Автор']) + '. Исполнитель: ' + str(element['Исполнитель']) + '. Story points: ' +
            str(element['Story Points']) + '. Sprint: ' + str(element['Sprint']) + '. Ключ: ' + str(element['Ключ']) +
            '. Ветка: ' + str(element['Ветка']) + '. Версии исправления: ' + str(element['Версии исправления']) +
            '\nОписание:\n' + str(element['Описание'])
        )
        final_data = {}
        final_data['summary'] = element['Pезюме']
        final_data['queue'] = 'DESK'
        final_data['description'] = description
        if element['Тип задачи'].lower() == 'баг':
            final_data['type'] = {'name': 'Ошибка'}
        elif element['Тип задачи'].lower() == 'эпик':
            final_data['type'] = {'name': 'Epic'}
        elif element['Тип задачи'].lower() == 'история':
            final_data['type'] = {'name': 'Story'}
        else:
            final_data['type'] = {'name': 'Задача'}

        if element['Приоритет'].lower() == 'highest':
            final_data['priority'] = {'name': 'Блокер'}
        elif element['Приоритет'].lower() == 'high':
            final_data['priority'] = {'name': 'Критичный'}
        elif element['Приоритет'].lower() == 'medium':
            final_data['priority'] = {'name': 'Средний'}
        elif element['Приоритет'].lower() == 'low':
            final_data['priority'] = {'name': 'Низкий'}
        else:
            final_data['priority'] = {'name': 'Незначительный'}
        final_data['unique'] = element['Ключ']

        final_storage.append(final_data)


