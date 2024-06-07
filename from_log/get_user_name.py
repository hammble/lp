import json

from vkbottle.user import User
from config import token

user = User(token)

async def get_user_name_log(user_id):
    user_info = await user.api.users.get(user_ids=user_id)
    return f"{user_info[0].first_name} {user_info[0].last_name}"