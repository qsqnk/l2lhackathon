import user_repository

user_queue = []


def add_user(user_id: int):
    user_queue.append(user_id)


def listen():
    while len(user_queue) < 2:
        pass

    matched_pairs = []
    for i, user_id_1 in enumerate(user_queue):
        max_score, max_user = None, None
        for _, user_id_2 in enumerate(user_queue[:i + 1]):
            user1, user2 = map(user_repository.get_user, (user_id_1, user_id_2))
            if max_score is None or max_score < user1.match_score(user2):
                max_score, max_user = user1.match_score(user2), user2





