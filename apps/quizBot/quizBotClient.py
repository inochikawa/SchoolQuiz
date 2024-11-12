import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


class QuizBotClient:
    __application: Application
    __telegramToken: str

    def __init__(self):
        self.__telegramToken = os.environ["TELEGRAM_TOKEN"]
        self.__application = Application.builder().token(self.__telegramToken).build()

    def start(self):
        self.__application.run_polling(allowed_updates=Update.ALL_TYPES)


    def __setupTelegramApp(self, app: Application) -> Application:
        
        
