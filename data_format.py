from enum import Enum


class OUTCOME(Enum):
    Loss = 0
    NotComplete = 1
    Win = 2

class formatted_data:
    Score: int
    Outcome: OUTCOME
    NumTurns: int

    def __init__(self, score: int, outcome: OUTCOME, num_turns: int):
        self.Score = score
        self.Outcome = outcome
        self.NumTurns = num_turns
