import threading
import time

from telegram import ReplyKeyboardMarkup

import user_repository

temp = []
user_queue = []


def add_user(user_id: int):
    threading.Thread(target=lambda: add_delayed(user_id)).start()


def add_delayed(user_id: int) -> None:
    temp.append(user_id)
    time.sleep(5)
    if user_id not in user_queue and user_id in temp:
        user_queue.append(user_id)


def remove_user(user_id: int) -> None:
    temp.remove(user_id)


async def listen():
    from bot import bot
    while True:
        if len(user_queue) < 2:
            time.sleep(5)

        passed = set()

        for i in range(len(user_queue) - 1):
            user_id = user_queue[i]
            max_user_id = max(
                [id for id in user_queue[i + 1:] if id not in passed],
                key=lambda user_id_2: user_repository.get_user(user_id).match_score(
                    user_repository.get_user(user_id_2)
                )
            )
            user_repository.update_interlocutor(user_id, max_user_id)
            user_repository.update_interlocutor(max_user_id, user_id)
            for id in (user_id, max_user_id):
                user_queue.remove(id)
                passed.add(id)
                await bot.send_message(
                    id,
                    "Interlocutor is found. Have a nice chat!",
                    reply_markup=ReplyKeyboardMarkup([["Stop chatting", "Next interlocutor", "Exchange contacts"]],
                                                     one_time_keyboard=True),
                )
