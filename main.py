import json
import vk_api
import time
import loguru
import datetime
import asyncio

from termcolor import colored

from vkbottle import VKAPIError
from vkbottle.user import User, Message
from vkbottle.api import API
from vkbottle.tools import DocMessagesUploader

from collections import OrderedDict

from config import file_name
from config import file_name2

from from_log.get_chat_name import get_chat_name_log
from from_log.get_user_name import get_user_name_log

from other_text.start_text import message_text

from scripts.dd_script import DD_SCRIPT

from utils.edit_mes import edit_message
from utils.get_id import get_user_id, user_id_get_mes, search_group_ids
from utils.get_stickers import stick
from utils.get_user_name import get_user_name
from utils.get_vk_reg import data_reg

from json_utils.txt_temp import *
from json_utils.audio_temp import audio_messages, save_audio_messages, load_audio_messages
from json_utils.ignore import save_ignored_users, add_ignore, remove_ignore, load_ignored_users
from json_utils.dov import save_dov_users, add_dov, remove_dov, load_dov_users

with open(file_name, "r") as fh:
    token = json.load(fh)

with open(file_name2, "r") as fh:
    prefixes = json.load(fh)

loguru.logger.disable("vkbottle")

user = User(token)
api = API(token)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
user_info = vk.users.get()
user_id = user_info[0]['id']
owners = [user_id]

timers = {}
timer_counter = 0

vk.messages.send(user_id=user_id, random_id=0, message=message_text)

@user.on.message(text=[f'{prefix}очистить шабы' for prefix in prefixes])
async def reset_templates(message: Message):
    if message.from_id not in owners:
        return
    try:
        with open(TEMPLATES_FILE, 'r') as f:
            templates = json.load(f)
    except FileNotFoundError:
        await edit_message(message, "📝 Файл шаблонов не существует.")
        return
    if not templates:
        await edit_message(message, "📝 Нет шаблонов для удаления.")
        return
    num_templates_before = len(templates)
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump({}, f)
    await edit_message(message, f"♻ Успешно удалено {num_templates_before} шаблонов.")

@user.on.message(text=[f'{prefix}хелп' for prefix in prefixes])
async def dadacmds(message: Message):
    if message.from_id not in owners:
        return
    await edit_message(message, '⚙ Введите номер страницы.\n📝 Всего страниц: 4')

@user.on.message(text=[f'{prefix}хелп 1' for prefix in prefixes])
async def list_cmd(message: Message):
    if message.from_id not in owners:
        return
    text = [
'📝 Страница 1/4.\n\n'

'▹ +|-админ\n'
'╰ ставит/убирает админку в чате\n\n'

'▹ пинг\n'
'╰ проверка работоспособности\n\n'

'▹ +|-гп (группа/реплай)\n'
'╰ подписка/отписка от группы\n\n'

'▹ +|-лайк (человек/реплай)\n'
'╰ ставит/Убирает лайк на аву\n\n'

'▹ добавить (человек/реплай)\n'
'╰ добавляет в чат\n\n'

'▹ кик (человек/реплай)\n'
'╰ исключает из чата\n\n'

'▹ выйти\n'
'╰ покидает чат\n\n'

'▹ +|-др (человек/реплай)\n'
'╰ добавляет/удаляет из друзей\n\n'

'▹ +|-чс (человек/реплай)\n'
'╰ добавляет/удаляет из списка чс\n\n'

'▹ влс (человек/реплай)\n'
'[Текст]\n'
'╰ отправляет смс в диалог\n\n'
    ]
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}хелп 2' for prefix in prefixes])
async def list_cmd(message: Message):
    if message.from_id not in owners:
        return
    text = [
'📝 Страница 2/4.\n\n'

'▹ +|-игнор (человек/реплай)\n'
'╰ добавляет/удаляет из списка игнора\n\n'

'▹ игноры\n'
'╰ выводит список игнорируемых\n\n'

'▹ +|-дов (человек/реплай)\n'
'╰ добавляет/удаляет из списка доверенных\n\n'

'▹ /скажи (текст)\n'
'╰ повторяет текст (только доверенным)\n\n'

'▹ довы\n'
'╰ выводит список доверенных\n\n'

'▹ реши (пример)\n'
'╰ решает заданный пример\n\n'

'▹ погода (город)\n'
'╰ показывает погоду в городе\n\n'

'▹ инфо\n'
'╰ выводит информацию о профиле пользователя\n\n'

'▹ ид (человек/реплай)\n'
'╰ показывает ID человека\n\n'

'▹ рег (человек/реплай)\n'
'╰ показывает дату регистрации страницы, свою или человека\n\n'
    ]
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}хелп 3' for prefix in prefixes])
async def list_cmd(message: Message):
    if message.from_id not in owners:
        return
    text = [
'📝 Страница 3/4.\n\n'

'▹ +|-шаб (имя)\n'
'[Текст] (при +)\n'
'╰ добавляет/удаляет шаблон\n\n'

'▹ ~шаб (имя)\n'
'[Новый текст]\n'
'╰ изменяет созданный шаблон\n\n'

'▹ шаб (имя)\n'
'╰ показывает текст шаблона\n\n'

'▹ шабы\n'
'╰ выводит список шаблонов\n\n'

'▹ +таймер (время)\n'
'[текст]\n'
'╰ устанавливает таймер\n\n'

'▹ -таймер (номер)\n'
'╰ удаляет установленный таймер\n\n'

'▹ таймеры\n'
'╰ выводит список активных таймеров\n\n'

'▹ Дд (число)\n'
'╰ удаляет свои смс. Без указания числа - последние 2\n\n'

'▹ статус (текст)\n'
'╰ устанавливает статус в профиль\n\n'

'▹ очистить шабы\n'
'╰ очищает все шаблоны\n\n'

    ]
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}хелп 4' for prefix in prefixes])
async def list_cmd(message: Message):
    if message.from_id not in owners:
        return
    text = [
'📝 Страница 4/4.\n\n'
'▹ очистить таймеры\n'
'╰ очищает все таймеры\n\n'

'▹ стоп\n'
'╰ принудительное завершение работы бота\n\n'

'▹ хелп (номер)\n'
'╰ список команд по страницам\n\n'

'▹ группы (человек/реплай)\n'
'╰ список групп пользователя (не советую использовать во избежание флуда)\n\n'

'▹ стики (человек/реплай)\n'
'╰ список стикеров пользователя (не советую использовать во избежание флуда)\n\n'

'▹ +|-гс (имя) (реплай)\n'
'╰ создать головой шаблон с указанным именем\n\n'

'▹ гсы\n'
'╰ список голосовых шаблонов\n\n'

'▹ гс (имя)\n'
'╰ список голосовых шаблонов пользователя'

'▹ +реакция (реплай) (1-16)\n'
'╰ поставит реакцию на сообщение'

'▹ -реакция (реплай)\n'
'╰ удалит реакцию с сообщения'

'▹ логи\n'
'╰ отправит файл с логгами'
    ]
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}+лайк' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    name = await get_user_name(user_id)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.add(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                    type='photo')
    await edit_message(message, f"✅ Поставил лайк для {name}.")

@user.on.message(text=[f'{prefix}-лайк' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    name = await get_user_name(user_id)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.delete(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']),
                                       type='photo')
    await edit_message(message, f"✅ Удалил лайк для {name}.")

@user.on.message(text=[f'{prefix}+лайк <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    name = await get_user_name(user_id)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.add(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']), type='photo')
    await edit_message(message, f"✅ Поставил лайк для {name}.")

@user.on.message(text=[f'{prefix}-лайк <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    name = await get_user_name(user_id)
    spisok = []
    uss = await message.ctx_api.request("users.get", {"user_ids": user_id, "fields": "has_photo, photo_id"})
    print(uss)
    ussssss = uss['response'][0]['photo_id']
    spisok.append({
        "item_id": ussssss.split("_")[1],
        "owner_id": ussssss.split("_")[0],
        "access_key": None,
        "type": "photo",
        "name": "аву"
    })
    await message.ctx_api.likes.delete(owner_id=int(spisok[0]["owner_id"]), item_id=int(spisok[0]['item_id']), type='photo')
    await edit_message(message, f"✅ Удалил лайк для {name}.")

@user.on.message(text=[f'{prefix}+гп' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    gp_id = await user_id_get_mes(message)
    group = await message.ctx_api.request('groups.join', {'group_id': abs(gp_id)})
    await edit_message(message, f'✅ Вы вступили в группу')

@user.on.message(text=[f'{prefix}+гп <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    gp_id = search_group_ids(url)[0]
    group = await message.ctx_api.request('groups.join', {'group_id': abs(gp_id)})
    await edit_message(message, f'✅ Вы вступили в группу')

@user.on.message(text=[f'{prefix}-гп' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    gp_id = await user_id_get_mes(message)
    group = await message.ctx_api.request('groups.leave', {'group_id': abs(gp_id)})
    await edit_message(message, f'✅ Вы покинули группу.')

@user.on.message(text=[f'{prefix}-гп <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    gp_id = search_group_ids(url)[0]
    group = await message.ctx_api.request('groups.leave', {'group_id': abs(gp_id)})
    await edit_message(message, f'✅ Вы покинули группу.')

@user.on.message(text=[f'{prefix}рег' for prefix in prefixes])
async def regg(message: Message):
  if message.from_id not in owners:
        return
  user_id = await user_id_get_mes(message)
  await edit_message(message, data_reg(user_id))

@user.on.message(text=[f'{prefix}рег <link>' for prefix in prefixes])
async def piska(message: Message, link: str):
  if message.from_id not in owners:
        return
  user_id = get_user_id(link)[0]
  await edit_message(message, data_reg(user_id))

@user.on.message(text=[f'{prefix}статус <text>' for prefix in prefixes])
async def greeting(message: Message, text: str):
    if message.from_id not in owners:
        return
    await message.ctx_api.status.set(text)
    await edit_message(message, f"✅ Изменил статус на: <<{text}>>")

@user.on.message(text=[f'{prefix}ид' for prefix in prefixes])
async def getid(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    await edit_message(message, f'🆔 [id{user_id}|Пользователя]: {user_id}')

@user.on.message(text=[f'{prefix}ид <link>' for prefix in prefixes])
async def ejdj(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    await edit_message(message, f'🆔 [id{user_id}|Пользователя]: {user_id}')

@user.on.message(text=[f'{prefix}пинг' for prefix in prefixes])
async def ping(message: Message):
    if message.from_id not in owners:
        return
    delta = round(time.time() - message.date, 2)
    text = f'🏓 Понг! Задержка: {delta}с.'
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}+др' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message=message)
    if user_id == message.from_id:
        await edit_message(message, "❌ Не добавляйте себя в друзья!")
        return
    await message.ctx_api.friends.add(user_id)
    name = await get_user_name(user_id)
    text = f'✅ {name} добавлен в друзья.'
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}+др <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, "❌ Не добавляйте себя в друзья!")
        return
    await message.ctx_api.friends.add(user_id)
    name = await get_user_name(user_id)
    text = f'✅ {name} добавлен в друзья.'
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}-др' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message=message)
    if user_id == message.from_id:
        await edit_message(message, "❌ Не удаляйте себя из друзей!")
        return
    await message.ctx_api.friends.delete(user_id)
    name = await get_user_name(user_id)
    text = f'✅ {name} удалён из друзей.'
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}-др <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, "❌ Не удаляйте себя из друзей!")
        return
    await message.ctx_api.friends.delete(user_id)
    name = await get_user_name(user_id)
    text = f'✅ {name} удалён из друзей.'
    await edit_message(message, text)

@user.on.message(text=[f'{prefix}добавить' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    try:
        user_id = await user_id_get_mes(message)
        if user_id == message.from_id:
            await edit_message(message, "❌ Не добавляйте себя в чат!")
            return
        await message.ctx_api.request("messages.addChatUser", {"user_id": user_id,"chat_id": message.peer_id - 2000000000})
        text = '✅ Добавлен в чат.'
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")

@user.on.message(text=[f'{prefix}добавить <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    try:
        user_id = get_user_id(url)[0]
        if user_id == message.from_id:
            await edit_message(message, "❌ Не добавляйте себя в чат!")
            return
        await message.ctx_api.request("messages.addChatUser", {"user_id": user_id,"chat_id": message.peer_id - 2000000000})
        text = '✅ Добавлен в чат.'
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")

@user.on.message(text=[f'{prefix}+админ' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    try:
        user_id = await user_id_get_mes(message)
        if user_id == message.from_id:
            await edit_message(message, "❌ Не добавляйте себя в админы!")
            return
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "admin"})
        text = f"✅ [id{user_id}|Права администратора выданы.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')

@user.on.message(text=[f'{prefix}+админ <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    try:
        user_id = get_user_id(url)[0]
        if user_id == message.from_id:
            await edit_message(message, "❌ Не добавляйте себя в админы!")
            return
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "admin"})
        text = f"✅ [id{user_id}|Права администратора выданы.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')

@user.on.message(text=[f'{prefix}-админ' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    try:
        user_id = await user_id_get_mes(message)
        if user_id == message.from_id:
            await edit_message(message, "❌ Не удаляйте себя из админов!")
            return
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "member"})
        text = f"✅ С [id{user_id}|Права администратора сняты.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")

@user.on.message(text=[f'{prefix}-админ <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    try:
        user_id = get_user_id(url)[0]
        if user_id == message.from_id:
            await edit_message(message, "❌ Не удаляйте себя из админов!")
            return
        await message.ctx_api.request("messages.setMemberRole",
                                      {"peer_id": message.peer_id, "member_id": user_id, "role": "member"})
        text = f"✅ С [id{user_id}|Права администратора сняты.]"
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f"Ошибка: {ex}")

@user.on.message(text=[f'{prefix}кик' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    try:
        user_id = await user_id_get_mes(message)
        if user_id == message.from_id:
            await edit_message(message, "❌ Не кикайте себя!")
            return
        await message.ctx_api.request("messages.removeChatUser", {"member_id": user_id,
                                                                  "chat_id": message.peer_id - 2000000000})
        text = f"✅ Исключен с беседы."
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')

@user.on.message(text=[f'{prefix}кик <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    try:
        user_id = get_user_id(url)[0]
        if user_id == message.from_id:
            await edit_message(message, "❌ Не кикайте себя!")
            return
        await message.ctx_api.request("messages.removeChatUser", {"member_id": user_id,"chat_id": message.peer_id - 2000000000})
        text = f"✅ Исключен с беседы."
        await edit_message(message, text)
    except Exception as ex:
        await edit_message(message, f'Ошибка: {ex}')

@user.on.message(text=[f'{prefix}выйти' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    text = f"✅ Покинул беседу"
    await edit_message(message, text)
    await message.ctx_api.request("messages.removeChatUser", {"member_id": message.from_id,"chat_id": message.peer_id - 2000000000})

@user.on.message(text=[f'{prefix}+чс' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, "❌ Не добавляйте себя в чс!")
        return
    name = await get_user_name(user_id)
    await message.ctx_api.account.ban(user_id)
    await edit_message(message, f'✅ {name} добавлен в ЧС')

@user.on.message(text=[f'{prefix}+чс <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, "❌ Не добавляйте себя в чс!")
        return
    name = await get_user_name(user_id)
    await message.ctx_api.account.ban(user_id)
    await edit_message(message, f'✅ {name} добавлен в ЧС')

@user.on.message(text=[f'{prefix}-чс' for prefix in prefixes])
async def greeting(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    if user_id == message.from_id:
        await edit_message(message, "❌ Не удаляйте себя из ЧС!")
        return
    name = await get_user_name(user_id)
    await message.ctx_api.account.unban(user_id)
    await edit_message(message, f'✅ {name} удален из ЧС')

@user.on.message(text=[f'{prefix}-чс <url>' for prefix in prefixes])
async def greeting(message: Message, url: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    if user_id == message.from_id:
        await edit_message(message, "❌ Не удаляйте себя из ЧС!")
        return
    name = await get_user_name(user_id)
    await message.ctx_api.account.unban(user_id)
    await edit_message(message, f'✅ {name} удален из ЧС')

@user.on.message(text=[f'{prefix}влс\n<text>' for prefix in prefixes])
async def greeting(message: Message, text: str):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    await message.ctx_api.request("messages.send", {"peer_id": user_id, "message": text, "random_id": 0})
    tt = '✅ Сообщение отправлено.'
    await edit_message(message, tt)

@user.on.message(text=[f'{prefix}влс <url>\n<text>' for prefix in prefixes])
async def greeting(message: Message, url: str, text: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(url)[0]
    await message.ctx_api.request("messages.send", {"peer_id": user_id, "message": text, "random_id": 0})
    tt = '✅ Сообщение отправлено.'
    await edit_message(message, tt)

@user.on.message(text=[f'{prefix}+шаб <name>\n<text>' for prefix in prefixes])
async def add_template(message: Message, name: str, text: str):
    if message.from_id not in owners:
        return
    else:
        with open(TEMPLATES_FILE, 'r') as f:
            templates = json.load(f)
        templates[name] = text
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(templates, f)
        await edit_message(message=message, text=f"✅ Шаблон «{name}» создан.")

@user.on.message(text=[f'{prefix}-шаб <name>' for prefix in prefixes])
async def delete_template(message: Message, name: str):
    if message.from_id not in owners:
        return
    else:
        with open(TEMPLATES_FILE, 'r') as f:
            templates = json.load(f)
        if name in templates:
            del templates[name]
            with open(TEMPLATES_FILE, 'w') as f:
                json.dump(templates, f)
            await edit_message(message=message, text=f"✅ Шаблон «{name}» удален.")
        else:
            await edit_message(message=message, text=f"❌ Шаблон «{name}» не найден.")

@user.on.message(text=[f'{prefix}~шаб <name>\n<new_text>' for prefix in prefixes])
async def edit_template(message: Message, name: str, new_text: str):
    if message.from_id not in owners:
        return
    else:
        with open(TEMPLATES_FILE, 'r') as f:
            templates = json.load(f)
        if name in templates:
            templates[name] = new_text
            with open(TEMPLATES_FILE, 'w') as f:
                json.dump(templates, f)
            await edit_message(message=message, text=f"✅ Текст шаблона «{name}» изменен.")
        else:
            await edit_message(message=message, text=f"❌ Шаблон «{name}» не найден.")

@user.on.message(text=[f'{prefix}шабы' for prefix in prefixes])
async def list_templates(message: Message):
    if message.from_id not in owners:
        return
    else:
        with open(TEMPLATES_FILE, 'r') as f:
            template_names = json.load(f, object_pairs_hook=OrderedDict)
        if template_names:
            template_list = "\n".join(f"{i+1}. {name}" for i, name in enumerate(template_names))
            await edit_message(message=message, text=f"📖 Список шаблонов:\n{template_list}")
        else:
            await edit_message(message=message, text="📖 Список шаблонов пуст.")

@user.on.message(text=[f'{prefix}шаб <name>' for prefix in prefixes])
async def use_template(message: Message, name: str):
    if message.from_id not in owners:
        return
    else:
        with open(TEMPLATES_FILE, 'r') as f:
            templates = json.load(f)

        if name in templates:
            template_text = templates[name]
            await edit_message(message=message, text=f"{template_text}")
        else:
            await edit_message(message=message, text=f"❌ Шаблон «{name}» не найден.")

@user.on.message(text=[f'{prefix}реши <equation>' for prefix in prefixes])
async def solve_equation(message: Message, equation: str):
    if message.from_id not in owners:
        return
    try:
        result = eval(equation)
        await edit_message(message, text=f"📝 Результат: {result}")
    except Exception as e:
        error_message = f"⚠ Произошла неизвестная ошибка."
        await edit_message(message, error_message)

@user.on.message(text=[f'{prefix}+таймер <minutes:int>\n<text>' for prefix in prefixes])
async def set_timer(message: Message, minutes: int, text: str):
    if message.from_id not in owners:
        return
    try:
        global timer_counter
        response = "⌚ Таймер установлен!"
        await edit_message(message, response)
        timer_counter += 1
        timer_id = timer_counter
        timers[timer_id] = {
            'minutes': minutes,
            'text': text,
            'user_id': message.from_id,
            'start_time': datetime.datetime.now()
        }

        await asyncio.sleep(minutes * 60)
        if timer_id in timers:
            await message.answer(text)
            timers.pop(timer_id)
        for idx, timer_info in list(timers.items()):
            if idx > timer_id:
                timers[idx - 1] = timers.pop(idx)
    except Exception as e:
        print(f"Ошибка при установке таймера: {e}")

@user.on.message(text=[f'{prefix}очистить таймеры' for prefix in prefixes])
async def clear_timers(message: Message):
    if message.from_id not in owners:
        return
    global timers
    if not timers:
        await edit_message(message, "📝 Список таймеров пуст.")
    else:
        timers = {}
        await edit_message(message, "✅ Список таймеров успешно очищен.")

@user.on.message(text=[f'{prefix}таймеры' for prefix in prefixes])
async def list_timers(message: Message):
    if not timers:
        await edit_message(message, text="⌚ Нет активных таймеров.")
        return
    response = "⌚ Список активных таймеров:\n"
    for timer_id, timer_info in timers.items():
        response += f"{timer_id}. {timer_info['text']} -> {timer_info['minutes']} минуток\n"
    await edit_message(message, response)

@user.on.message(text=[f'{prefix}-таймер <timer_id:int>' for prefix in prefixes])
async def remove_timer(message: Message, timer_id: int):
    if message.from_id not in owners:
        return
    global timers, timer_counter
    if timer_id in timers:
        timers.pop(timer_id)
        await edit_message(message, text=f"✅ Таймер с ID «{timer_id}» удален.")
    else:
        await edit_message(message, text=f"❌ Таймер с ID «{timer_id}» не найден.")
    for idx, timer_info in timers.items():
        if idx > timer_id:
            timers[idx - 1] = timers.pop(idx)
    if not timers:
        timer_counter = 0

@user.on.message(text=['/скажи <text>', '/Скажи <text>'])
async def dovtext(message: Message, text: str):
    dov_users = load_dov_users()
    if message.from_id in dov_users:
        await message.answer(f'{text}')

@user.on.message(text=[f'{prefix}инфо' for prefix in prefixes])
async def infolp(message: Message):
    if message.from_id not in owners:
        return
    user_id = message.from_id
    name = await get_user_name(user_id)
    dov = load_dov_users()
    dov_count = len(dov)
    ignored_users = load_ignored_users()
    ignored_count = len(ignored_users)
    timer_count = len(timers)
    with open(TEMPLATES_FILE, 'r') as f:
        templates = json.load(f)
    templates_count = len(templates)
    if prefixes:
        prefixes_list = ", ".join(prefixes)
        prefixes_info = f"📖 Префиксы команд: {prefixes_list}\n"
    else:
      prefixes_info = "❌ Нет добавленных префиксов\n"
    text = [
        f'👤 Пользователь {name}\n'
        f'⚙ Префикс повторялки: /скажи\n'
        f'⚙ Префикс удалялки: Дд\n'
        f'📘 Таймеров: {timer_count}\n'
        f'📘 Доверенных: {dov_count}\n'
        f'📘 Игнорируемых: {ignored_count}\n'
        f'📘 Шаблонов: {templates_count}\n'
        f'{prefixes_info}'
    ]
    await edit_message(message, text)

@user.on.message(text=['дд', 'Дд <count:int>', 'Дд', 'дд <count:int>'])
async def greeting(message: Message, count: int = 2):
    if message.from_id not in owners:
        return
    ct = count + 1
    await message.ctx_api.execute(DD_SCRIPT % (ct,message.peer_id,message.from_id,int(datetime.datetime.now().timestamp())))

@user.on.message(text=[f'{prefix}группы' for prefix in prefixes])
async def groups(message: Message):
    if message.from_id in owners:
        try:
            user_id = await user_id_get_mes(message)
            groups = await api.groups.get(user_id=user_id)
            group_ids = groups.items
            group_list = ""
            for index, group_id in enumerate(group_ids, start=1):
                group_info_list = await api.groups.get_by_id(group_id)
                if group_info_list:
                    group_info = group_info_list[0]
                    group_list += f"{index}. [club{group_info.id}|{group_info.name}]\n"
        except VKAPIError[30]:
            await edit_message(message, text='⚠ Ограничение приватности профиля.')
            return
        await edit_message(message, text=f'{group_list}')

@user.on.message(text=[f'{prefix}группы <link>' for prefix in prefixes])
async def groups(message: Message, link: str):
    if message.from_id in owners:
        try:
            user_id = get_user_id(link)[0]
            groups = await api.groups.get(user_id=user_id)
            group_ids = groups.items
            group_list = ""
            for index, group_id in enumerate(group_ids, start=1):
                group_info_list = await api.groups.get_by_id(group_id)
                if group_info_list:
                    group_info = group_info_list[0]
                    group_list += f"{index}. [club{group_info.id}|{group_info.name}]\n"
        except VKAPIError[30]:
            await edit_message(message, text='⚠ Ограничение приватности профиля.')
            return
        await edit_message(message, text=f'{group_list}')

@user.on.message(text=[f'{prefix}+игнор' for prefix in prefixes])
async def idsfdsgvds_add(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя добавить самого себя.')
        return
    ignored_users = load_ignored_users()
    if user_id in ignored_users:
        await edit_message(message, f'⚠ {username} уже присутствует в игнор-листе.')
        return
    await edit_message(message, f'✅ {username} добавлен в игнор-лист.')
    add_ignore(user_id)

@user.on.message(text=[f'{prefix}-игнор' for prefix in prefixes])
async def iqwedfv_remove(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя удалить самого себя.')
        return
    ignored_users = load_ignored_users()
    if user_id not in ignored_users:
        await edit_message(message, f'⚠ {username} отсутствует в игнор-листе.')
        return
    await edit_message(message, f'✅ {username} удалён из игнор-листа.')
    remove_ignore(user_id)

@user.on.message(text=[f'{prefix}+игнор <link>' for prefix in prefixes])
async def iwd3df_add(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя добавить самого себя.')
        return
    ignored_users = load_ignored_users()
    if user_id in ignored_users:
        await edit_message(message, f'⚠ {username} уже присутствует в игнор-листе.')
        return
    await edit_message(message, f'✅ {username} добавлен в игнор-лист.')
    add_ignore(user_id)

@user.on.message(text=[f'{prefix}-игнор <link>' for prefix in prefixes])
async def idgfdg_remove(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя удалить самого себя.')
        return
    ignored_users = load_ignored_users()
    if user_id not in ignored_users:
        await edit_message(message, f'⚠ {username} отсутствует в игнор-листе.')
        return
    await edit_message(message, f'✅ {username} удалён из игнор-листа.')
    remove_ignore(user_id)

@user.on.message(text=[f'{prefix}+дов' for prefix in prefixes])
async def idov_add(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя добавить самого себя.')
        return
    dov_users = load_dov_users()
    if user_id in dov_users:
        await edit_message(message, f'⚠ {username} уже присутствует в доверенных.')
        return
    await edit_message(message, f'✅ {username} добавлен в доверенные.')
    add_dov(user_id)

@user.on.message(text=[f'{prefix}-дов' for prefix in prefixes])
async def idovdfd_remove(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя удалить самого себя.')
        return
    dov_users = load_dov_users()
    username = await get_user_name(user_id)
    if user_id not in dov_users:
        await edit_message(message, f'⚠ {username} отсутствует в доверенных.')
        return
    await edit_message(message, f'✅ {username} удалён из доверенных.')
    remove_dov(user_id)

@user.on.message(text=[f'{prefix}+дов <link>' for prefix in prefixes])
async def iddd_add(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    username = await get_user_name(user_id)
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя добавить самого себя.')
        return
    dov_users = load_dov_users()
    if user_id in dov_users:
        await edit_message(message, f'⚠ {username} уже присутствует в доверенных.')
        return
    await edit_message(message, f'✅ {username} добавлен в доверенные.')
    add_dov(user_id)

@user.on.message(text=[f'{prefix}-дов <link>' for prefix in prefixes])
async def isdsds_remove(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    if message.from_id == user_id:
        await edit_message(message, '⚠ Нельзя удалить самого себя.')
        return
    dov_users = load_dov_users()
    username = await get_user_name(user_id)
    if user_id not in dov_users:
        await edit_message(message, f'⚠ {username} отсутствует в доверенных.')
        return
    await edit_message(message, f'✅ {username} удалён из доверенных.')
    remove_dov(user_id)

@user.on.message(text=[f'{prefix}игноры' for prefix in prefixes])
async def ignorspis(message: Message):
    if message.from_id not in owners:
        return
    ignored_users = load_ignored_users()
    users_list = ""
    for i, user_id in enumerate(ignored_users, 1):
        username = await get_user_name(user_id)
        users_list += f"{i}. {username}\n"
    await edit_message(message, users_list)

@user.on.message(text=[f'{prefix}довы' for prefix in prefixes])
async def dovsspis(message: Message):
    if message.from_id not in owners:
        return
    dov_users = load_dov_users()
    users_list = ""
    for i, user_id in enumerate(dov_users, 1):
        username = await get_user_name(user_id)
        users_list += f"{i}. {username}\n"
    await edit_message(message, users_list)

@user.on.message(text=[f'{prefix}стики <link>' for prefix in prefixes])
async def handle_stickers(message: Message, link: str):
    if message.from_id not in owners:
        return
    user_id = get_user_id(link)[0]
    access_token = token
    response_message = await stick(user_id, access_token)
    await edit_message(message, f"{response_message}")

@user.on.message(text=[f'{prefix}стики' for prefix in prefixes])
async def handle_stickers(message: Message):
    if message.from_id not in owners:
        return
    user_id = await user_id_get_mes(message)
    access_token = token
    response_message = await stick(user_id, access_token)
    await edit_message(message, f"{response_message}")

@user.on.message(text=[f'{prefix}+гс <name>' for prefix in prefixes])
async def gs(e: Message, name: str):
    if e.from_id not in owners:
        return
    if len(name)>20:
        await edit_message(e, '⚠ Максимальная длина названия 20 символов.')
        return
    load_audio_messages()
    if name in audio_messages:
        await edit_message(e, f'⚠ Голосовой шаблон <<{name}>> уже существует.')
        return
    payload = e.reply_message.text if e.reply_message else None
    attachments = e.reply_message.attachments if e.reply_message else e.attachments
    if not payload and not attachments:
        await edit_message(e, text='⚠ Для создания шаблона необходим текст или вложение')
        return
    audio_links = []
    for att in attachments:
        if att.audio_message is not None:
            if att.audio_message.access_key is None:
                audio_links.append(f'audio_message{att.audio_message.owner_id}_{att.audio_message.id}')
            else:
                audio_links.append(f'audio_message{att.audio_message.owner_id}_{att.audio_message.id}_{att.audio_message.access_key}')

    audio_messages[name] = audio_links
    save_audio_messages()
    await edit_message(e, f'✅ Голосовой шаблон <<{name}>> создан.')

@user.on.message(text=[f'{prefix}гс <name>' for prefix in prefixes])
async def send_gs(e: Message, name: str):
    if e.from_id not in owners:
        return
    load_audio_messages()
    if name in audio_messages:
        for audio_link in audio_messages[name]:
            await e.ctx_api.execute(DD_SCRIPT % (1,e.peer_id,e.from_id,int(datetime.datetime.now().timestamp())))
            await e.answer(attachment=audio_link)
    else:
        await edit_message(e, '⚠ Такого голосового шаблона не существует.')

@user.on.message(text=[f'{prefix}гсы' for prefix in prefixes])
async def list_templates(e: Message):
    load_audio_messages()
    if not audio_messages:
        await edit_message(e, "⚠ Список голосовых шаблонов пуст.")
        return
    templates_list = "\n".join([f"{index + 1}. {template}" for index, template in enumerate(audio_messages.keys())])
    await edit_message(e, f"📖 Список голосовых шаблонов:\n{templates_list}")

@user.on.message(text=[f'{prefix}-гс <name>' for prefix in prefixes])
async def delete_template(e: Message, name: str):
    if e.from_id not in owners:
        return
    load_audio_messages()
    if name in audio_messages:
        del audio_messages[name]
        save_audio_messages()
        await edit_message(e, f'✅ Голосовой шаблон <<{name}>> удален.')
    else:
        await edit_message(e, f'⚠ Голосового шаблона <<{name}>> не существует.')

@user.on.message(text=[f'{prefix}+реакция <reaction_id:int>' for prefix in prefixes])
async def send_rec(message: Message, reaction_id: int):
    if message.from_id not in owners:
        return
    if reaction_id > 16:
        await edit_message(message, '⚠ Максимальное значение <<reaction_id>>: 16.')
        return
    await message.ctx_api.request(
        "messages.sendReaction",
        {
            "peer_id": message.peer_id,
            "cmid": message.reply_message.conversation_message_id if message.reply_message else message.conversation_message_id,
            "reaction_id": reaction_id
        }
    )
    await edit_message(message, '✅ Реакция установлена.')

@user.on.message(text=[f'{prefix}-реакция' for prefix in prefixes])
async def delete_rec(message: Message):
    if message.from_id not in owners:
        return
    await message.ctx_api.request(
        "messages.deleteReaction",
        {
            "peer_id": message.peer_id,
            "cmid": message.reply_message.conversation_message_id
        }
    )

    await edit_message(message, '✅ Реакция удалена.')

doc_uploader = DocMessagesUploader(user.api)

@user.on.message(text=[f'{prefix}логи' for prefix in prefixes])
async def setlogs(message: Message):
    if message.from_id not in owners:
        return
    doc = await doc_uploader.upload(
        title=f'logs.txt',
        file_source='logs.txt',
        peer_id=message.peer_id,
    )
    await user.api.messages.send(user_id=message.from_id, random_id=0, attachment=doc)
    with open('logs.txt', 'w'):
        pass
    await edit_message(message, '✅ Файл был отправлен к себе в лс. Предварительно очищен от содержимого.')

@user.on.message()
async def log_message(message: Message):
    ignored_users = load_ignored_users()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    text = message.text.replace('\n', ' ') if message.text else ""
    if not text:
        if message.attachments:
            attachment_type = message.attachments[0].type.value
            replacer = {
                'audio_message': '• голосовое сообщение',
                'audio': '• аудиозапись',
                'sticker': '• стикер',
                'photo': '• фотография',
                'video': '• видео',
                'doc': '• документ',
                'graffiti': '• граффити',
                'link': '• ссылка'
            }
            text = replacer.get(attachment_type, attachment_type)
        else:
            text = "• пересланные сообщения"

    prep_time = colored(f"[{current_time}]", 'blue')
    prep_time2 = f"[{current_time}]"

    mark = ''

    user_ask = colored(await get_user_name_log(message.from_id), 'red')
    user_ask2 = await get_user_name_log(message.from_id)

    prep_text = ": " + colored(text, 'cyan')
    prep_text2 = ": " + text

    if message.peer_id > 2000000000:
        conversation = colored(await get_chat_name_log(message.peer_id), 'green')
        conversation2 = await get_chat_name_log(message.peer_id)

    else:
        conversation = colored(await get_user_name_log(message.peer_id), 'green')
        conversation2 = await get_user_name_log(message.peer_id)

        mark = "[ЛС]"

    info_conversation = f"[{conversation}/{user_ask}]{prep_text}"
    info_conversation2 = f"[{conversation2}/{user_ask2}]{prep_text2}"

    print(prep_time, mark, info_conversation)

    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write(prep_time2 + mark + info_conversation2 + '\n')

    if message.from_id in ignored_users:
        await user.api.messages.delete(message_ids=message.id)

user.run_forever()