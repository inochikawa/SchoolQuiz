import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, Bot, MenuButton, MenuButtonCommands
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from data.models import UserProfile
from data.services import UserProfileService, GradeYearService


class QuizBotClient:
    _application: Application
    _telegramToken: str
    _userProfileService: UserProfileService
    _gradeYearService: GradeYearService

    def __init__(self):
        self._telegramToken = os.environ["TELEGRAM_TOKEN"]
        self._userProfileService = UserProfileService()
        self._gradeYearService = GradeYearService()
        self._setupTelegramApp()

    def start(self):
        self._application.run_polling(allowed_updates=Update.ALL_TYPES)

    def _setupTelegramApp(self) -> None:
        self._application = Application.builder().token(self._telegramToken).build()

        self._application.add_handler(ConversationHandler(
            entry_points=[CommandHandler("start", self._startCommandHandler)],
            states={
                QuizBotGlobalState.ASK_FOR_GRADE_YEAR_ID: [MessageHandler(filters=filters.TEXT, callback=self._selectGradeYearIdCommandHandler)]
            },
            fallbacks=[CommandHandler("start", self._startCommandHandler)]
        ))

        self._application.add_handler(CommandHandler("quiz", callback=self._selectQuizIdCommandHandler))

    async def _startCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.get_bot().set_chat_menu_button(menu_button=MenuButtonCommands())

        userInfo = update.message.from_user
        userId = str(userInfo.id)

        userProfile = self._userProfileService.searchById(userId)

        if userProfile is None:
            userProfile = UserProfile(id=userId, firstName=userInfo.first_name, lastName=userInfo.last_name, gradeYearId="")

        if userProfile.gradeYearId == "":
            replyText = f"Привіт, {userProfile.firstName}!\nВкажи будь ласка свій клас, щоб я міг зрозуміти, які тести тобі можна запропонувати"
            gradeYears = self._gradeYearService.getAll()

            buttons = [[KeyboardButton(text=x.code) for x in gradeYears]]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

            await update.message.reply_text(text=replyText, reply_markup=keyboard)

            context.user_data["profile"] = userProfile

            return QuizBotGlobalState.ASK_FOR_GRADE_YEAR_ID

        return QuizBotGlobalState.ASK_FOR_QUIZ_ID

    async def _selectGradeYearIdCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = context.user_data["profile"]

        gradeYear = self._gradeYearService.searchByCode(update.effective_message.text, academicYear=None)

        userProfile.gradeYearId = gradeYear.id
        self._userProfileService.save(userProfile)

        await update.effective_message.reply_text(text=f"Прекрасно, Дякую!\nТвій клас: {gradeYear.code} у навчальному році {gradeYear.academicYear}-{gradeYear.academicYear + 1}.")

        return QuizBotGlobalState.ASK_FOR_QUIZ_ID

    async def _selectQuizIdCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.effective_message.reply_text("Я бачу тебе цікавить щось цікаве")


class QuizBotGlobalState:
    ASK_FOR_GRADE_YEAR_ID = 1
    ASK_FOR_QUIZ_ID = 2
