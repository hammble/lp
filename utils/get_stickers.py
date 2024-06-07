import requests

async def stick(uid: int, tok: str):
    url = 'https://api.vk.com/method/gifts.getCatalog?v=5.131&user_id={}&access_token={}'.format(uid, tok)
    stickers = requests.get(url, headers={
        "user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; Unuty_lp; 1; ru; 123x123)"}).json()
    stickers = stickers['response']
 
    url_f = 'https://api.vk.com/method/gifts.getCatalog?v=5.131&user_id=627689528&access_token={}'.format(tok)
    stickers_filter = requests.get(url_f, headers={
        "user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; Unuty_lp; 1; ru; 123x123)"}).json()
    stickers_filter = stickers_filter['response'][1]['items'][2:]
 
    sticker_list = [
        f"{i['sticker_pack']['title']}"
        for i in stickers[1]['items']
        if 'disabled' in i
    ]
 
    sum_price_golosa = sum(
        d['price'] for d in stickers_filter if d['sticker_pack']['title'] in sticker_list)
 
    sum_stick_price_golosa = str(sum_price_golosa)  # цена в голосах
    sum_stick_price_rub = str(sum_price_golosa * 7)  # цена в рублях
    count = str(len(sticker_list))  # количество стикер паков
 
    if count == 0:
        out_message = ".\n🥺 Платных стикерпаков у пользователя нет."
        return out_message
    else:
        text = f"💰 Стоимость в голосах: {sum_stick_price_golosa}\n" \
        f"🎁 Количество стикер паков: {count}\n" \
        f"💵 Стоимость в рублях: {sum_stick_price_rub}₽\n\n"
        return text + ", ".join(sticker_list)