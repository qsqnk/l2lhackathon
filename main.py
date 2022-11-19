import logging
import threading

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PollAnswerHandler,
    filters,
)
from handlers import *
from bot_states import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    TOKEN = "5825509581:AAFV8VUD8lEyBKvaoqBKZX_5dGLiqczpJMc"
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", suggest_fill_information)],
        states={
            START_FILL_INFO: [
                MessageHandler(filters.Text(["Start filling the information"]), suggest_choose_country_from)
            ],
            WAITING_FOR_COUNTRY_FROM: [
                MessageHandler(filters.ALL, save_choose_country_from)
            ],
            WAITING_FOR_COUNTRY_TO: [
                MessageHandler(filters.ALL, save_choose_country_to)
            ],
            WAITING_FOR_WORK_FIELD: [
                MessageHandler(filters.ALL, save_work_field),
            ],
            WAITING_FOR_PROBLEMS: [
                PollAnswerHandler(save_problems),
            ],
            INFO_CHOSEN: [
                MessageHandler(filters.Text(["Find interlocutor"]), add_to_queue),
            ],
            CHATTING: [
                MessageHandler(filters.ALL, chatting_message)
            ]
        },
        per_chat=False,
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    threading.Thread(target=user_queue.listen).start()
    application.run_polling()


if __name__ == "__main__":
    main()
