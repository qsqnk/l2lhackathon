# it is just mock for hackathon
from typing import Any, Optional, Dict, List
from user import User

user_repository: Dict[int, User] = {}


def get_all():
    return {k: str(v) for k, v in user_repository.items()}


def create_user(user_id: int, username: str) -> None:
    user_repository[user_id] = User(username)


def update_country_from(user_id: int, country_from: str) -> None:
    user_repository[user_id].country_from = country_from.lower()


def update_country_to(user_id: int, country_to: str) -> None:
    user_repository[user_id].country_to = country_to.lower()


def update_job(user_id: int, job: str) -> None:
    user_repository[user_id].job = job.lower()


def update_problems(user_id: int, problems: List[int]) -> None:
    user_repository[user_id].problems = problems


def update_interlocutor(user_id: int, interlocutor: int) -> None:
    user_repository[user_id].interlocutor = interlocutor


def get_user(user_id: int) -> Optional[User]:
    return user_repository[user_id]
