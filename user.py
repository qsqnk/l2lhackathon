from typing import List

COUNTRY_FROM_MUL = 50
COUNTRY_TO_MUL = 100
JOB_MUL = 4
PROBLEM_MUL = 2


class User:

    def __init__(self, username: str):
        self.username = username
        self.country_from = None
        self.country_to = None
        self.job = None
        self.problems = None
        self.interlocutor = None

    def match_score(self, other: "User") -> int:
        problem_matches = set(self.problems).intersection(set(other.problems))
        return (
                (self.country_from == other.country_from) * COUNTRY_FROM_MUL +
                (self.country_to == other.country_to) * COUNTRY_TO_MUL +
                (self.job == other.job) * JOB_MUL +
                len(problem_matches) * PROBLEM_MUL
        )

    def __str__(self):
        return f"User(from: {self.country_from}, to: {self.country_to}, job: {self.job}, problems: {self.problems}"
