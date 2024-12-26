import os

from dotenv import load_dotenv

load_dotenv(".env")

DEVS = [6696975845]



API_ID = int(os.getenv("API_ID", "20304260"))

API_HASH = os.getenv("API_HASH", "763e943987ee09ec449ad1611b7f5fc1")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7903768405:AAHFwUgVrnbPbB5y5oAdzjKwI-rFR5VsvoQ")

OWNER_ID = int(os.getenv("OWNER_ID", "6696975845"))

USER_ID = list(map(int, os.getenv("USER_ID", "6696975845").split()))

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1002379610567"))

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1002474246616"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002474246616").split()))

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "sk-b76-2Xm3NudxolduxgQnvFQTmbSjF0MQEVXtP4EfmMT3BlbkFJfk1LYV_1GUrcanMhuvhafaJ2dLs4yYwsgH5aBtaI8A",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL", "mongodb+srv://yxxxgans:KNux8MruL0hlBv50@botme.srpuzxu.mongodb.net/?retryWrites=true&w=majority&appName=botme")
