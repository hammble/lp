from vkbottle.user import User
from config import token

user = User(token)

async def get_chat_name_log(chat_id):
    chat_info = await user.api.messages.get_conversations_by_id(peer_ids=chat_id)
    return chat_info.items[0].chat_settings.title