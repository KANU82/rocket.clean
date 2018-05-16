#!/usr/bin/python3
import fileinput
from rocketchat.api import RocketChatAPI
from pathlib import Path
from dateutil import parser
from datetime import datetime
import pytz
import sys

config_file = Path("/etc/rocketsend/rocket.conf")
if config_file.is_file():
    conf_file=open("/etc/rocketsend/rocket.conf",'r')
    for line in conf_file.read().split('\n'):
        if line.startswith('USER'):
            if line.count('=')>0:
                user = line.split('=')[1].strip().replace('"','')

        if line.startswith('PASSWORD'):
            if line.count('=')>0:
                password = line.split('=')[1].strip().replace('"','')  

        if line.startswith('CLEAN_HISTORY_GROUP_CHAT'):
            if line.count('=')>0:
                chats = line.split('=')[1].strip().replace('"','') 

        if line.startswith('CHAT_URL'):
            if line.count('=')>0:
                chat_url = line.split('=')[1].strip().replace('"','') 

    conf_file.close()

api = RocketChatAPI(settings={'username': user, 'password': password, 'domain': chat_url})
room_id = ''

for chat in chats.split(','):
    for room in api.get_private_rooms():
        if room['name'] == chat.strip():
            room_id = room['id']
            count=0
            for message in api.get_private_room_history(room_id,oldest='2016-05-30T13:42:25.304Z',count=2000)['messages']:
                    count = count + 1
                    message_ts = parser.parse(message['ts'])
                    utc=pytz.UTC
                    older_than = int((utc.localize(datetime.now()) - message_ts).total_seconds()/3600)
                    if older_than > 24:
                        # Удаляем сообщения старше 24-х часов
                        message_id = message['_id']
                        api.delete_private_room_message(room_id,message_id=message_id)

