from app.tg_bot import bot
from app.api.active_list import handlers
from app.api.general import handlers
from app.api.notes import handlers

try:
    bot.polling()
except Exception as err:
    print(f"{err.__class__} ::: {err}")