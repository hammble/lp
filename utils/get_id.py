import vk_api
import re

from vkbottle.user import Message
from config import token

def get_user_id_by_domain(user_domain: str):
    vk = vk_api.VkApi(token=token)
    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})
    if isinstance(obj, list):
        return
    if obj['type'] == 'user':
        return obj["object_id"]

def get_user_id(text):
    result = []
    regex = r"(?:vk\.com\/(?P<user>[\w\.]+))|(?:\[id(?P<user_id>[\d]+)\|)"
    for user_domain, user_id in re.findall(regex, text):
        if user_domain:
            result.append(get_user_id_by_domain(user_domain))
        if user_id:
            result.append(int(user_id))
    _result = []
    for r in result:
        if r is not None:
            _result.append(r)
    return _result

async def user_id_get_mes(message: Message):
    if message.reply_message == None:
        vk_user = message.from_id
    else:
        vk_user = message.reply_message.from_id
    return vk_user

def get_group_id_by_domain(user_domain: str):
    vk = vk_api.VkApi(token=token)
    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})
    if isinstance(obj, list):
        return
    if obj['type'] in ('group', 'page',):
        return obj["object_id"]

def search_group_ids(text: str):
    result = []
    regex = r"(?:vk\.com\/(?P<group>[\w\.]+))|(?:\[club(?P<group_id>[\d]+)\|)"
    for group_domain, group_id in re.findall(regex, text):
        if group_domain:
            result.append(get_group_id_by_domain(group_domain))
        if group_id:
            result.append(int(group_id))
    _result = []
    for r in result:
        if r is not None:
            _result.append(abs(r))
    return _result