from read_excel import final_storage
from time import sleep

from yandex_tracker_client import TrackerClient

token = 'Your yandex api token'
org_id = 'Your organization id'

client = TrackerClient(token=token, org_id=org_id)

element = final_storage[0]

for element in final_storage:
    try:
        client.issues.create(summary=element['summary'],
                             queue=element['queue'],
                             unique=element['unique'],
                             type=element['type'],
                             priority=element['priority'],
                             description=element['description']
                             )
        sleep(1)
    except:
        print(f'{element["unique"]} \n создать не получилось')


