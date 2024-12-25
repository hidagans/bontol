from motor.motor_asyncio import AsyncIOMotorClient

from ubot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.ubot


#from kymang.kymang.database import db
from ubot.core.database.expired import *
from ubot.core.database.notes import *
from ubot.core.database.premium import *
from ubot.core.database.reseller import *
from ubot.core.database.saved import *
from ubot.core.database.userbot import *
from ubot.core.database.bcast import *
from ubot.core.database.gbans import *
from ubot.core.database.permit import *
from ubot.core.database.pref import *
from ubot.core.database.variabel import *
from ubot.core.database.otp import *
from ubot.core.database.jaseb_db import *
#from ubot.core.database.afkdb import *
