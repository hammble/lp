from config import token
from vkbottle.user import User

user = User(token)

async def get_user_name(user_id: int) -> str:
    user_info = await user.api.users.get(user_ids=user_id)
    if user_info:
        first_name = user_info[0].first_name
        last_name = user_info[0].last_name
        return f"[https://vk.com/id{user_id}|{first_name} {last_name}]"
    return f"[id{user_id}|Unknown]"
