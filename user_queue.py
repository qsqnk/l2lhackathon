import logging
import threading
import time

from telegram import ReplyKeyboardMarkup

import user_repository

user_queue = []


def add_user(user_id: int):
    threading.Thread(target=lambda: add_delayed(user_id)).start()


def add_delayed(user_id: int) -> None:
    time.sleep(15)
    if user_id not in user_queue:
        user_queue.append(user_id)


async def listen():
    from bot import bot
    while True:
        if len(user_queue) < 2:
            time.sleep(1)

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
