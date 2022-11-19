import logging

import user_repository

user_queue = []


def add_user(user_id: int):
    if user_id not in user_queue:
        user_queue.append(user_id)


def listen():
    while len(user_queue) < 2:
        pass

    for i in range(len(user_queue) - 1):
        user_id_1 = user_queue[i]
        max_user_id = max(
            user_queue[i + 1:],
            key=lambda user_id_2: user_repository.get_user(user_id_1).match_score(
                user_repository.get_user(user_id_2)
            )
        )
        user_repository.update_interlocutor(user_id_1, max_user_id)
        user_repository.update_interlocutor(max_user_id, user_id_1)
