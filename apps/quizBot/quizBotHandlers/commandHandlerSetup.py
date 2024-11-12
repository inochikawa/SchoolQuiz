import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from data.services import QuizService, UserProfileService


class CommandHandlerSetup:
    __quizService: QuizService

    def __init__(self):
        self.__quizService = QuizService()

    async def setupUserProfileOnStartCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        quizzes = self.__quizService.getAll()

        keyboard = [[InlineKeyboardButton(q.topic, callback_data=[123])] for q in quizzes]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
