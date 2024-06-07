from vkbottle.user import Message

async def edit_message(message: Message,text: str = '',att: str = ''):
    return await message.ctx_api.messages.edit(peer_id=message.peer_id, message=text,message_id=message.id, keep_forward_messages=True,keep_snippets=True,dont_parse_links=False,attachment=att)