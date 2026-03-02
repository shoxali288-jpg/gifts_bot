import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin Telegram ID (to receive payment confirmations)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Your bank card for P2P transfers

CARD_NUMBER = os.getenv("CARD_NUMBER", "8800 4122 3547 5880")

# Gifts Catalog
GIFTS = [
    {"id": 1, "name": "Basic Gift", "price": 100, "stars": 50},
    {"id": 2, "name": "Premium Gift", "price": 500, "stars": 250},
    {"id": 3, "name": "Epic Gift", "price": 1000, "stars": 500},
]
