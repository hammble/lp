import os
import json

TEMPLATES_FILE = 'temps.json'

if not os.path.exists(TEMPLATES_FILE):
    with open(TEMPLATES_FILE, 'w') as f:
        json.dump({}, f)