import asyncio
import threading

import telegram
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PollAnswerHandler,
    filters, BaseHandler,
)

from config import TOKEN
from handlers import *
from bot_states import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
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
            CHATTING: [
                MessageHandler(filters.Text(["Find interlocutor"]), add_to_queue),
                MessageHandler(filters.Text(["Stop chatting"]), stop_chatting),
                MessageHandler(filters.Text(["Next interlocutor"]), next_interlocutor),
                MessageHandler(filters.Text(["Exchange contacts"]), exchange_contacts),
                MessageHandler(filters.Text(["Agree exchange"]), agree_exchange),
                MessageHandler(filters.Text(["Disagree exchange"]), disagree_exchange),
                MessageHandler(filters.Text(["Stop searching"]), stop_searching),
                MessageHandler(
                    filters.ALL & ~filters.Text(
                        ["Stop searching",
                         "Find interlocutor",
                         "Stop chatting",
                         "Next interlocutor",
                         "Exchange contacts",
                         "Agree exchange",
                         "Disagree exchange"]
                    ), chatting_message
                )
            ]
        },
        per_chat=False,
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    threading.Thread(target=lambda: asyncio.run(user_queue.listen())).start()
    application.run_polling()


if __name__ == "__main__":
    main()
