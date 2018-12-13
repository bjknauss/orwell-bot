from dynaconf import settings
from orwell.bot import bot

if __name__ == '__main__':
    bot.run(settings.TOKEN)
