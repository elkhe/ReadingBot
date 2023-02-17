import telebot

from app import config


TOKEN = config.TOKEN


bot = telebot.TeleBot(TOKEN)