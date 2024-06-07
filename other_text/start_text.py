import json
from config import file_name2

with open(file_name2, "r") as fh:
    prefixes = json.load(fh)

message_text = f"✅ Бот успешно запущен.\n📘 Версия: 0.0.6\n⚙ Команды: (префикс) хелп\n📝 Префиксы: {', '.join(prefixes)}"