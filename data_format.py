from enum import IntEnum


class OUTCOME(IntEnum):
    Loss = 0
    NotComplete = 1
    Win = 2

class formatted_data:
    Score: int
    Outcome: OUTCOME
    NumTurns: int

    def __init__(self, score: int = 0, outcome: OUTCOME = OUTCOME.NotComplete, num_turns: int = 0):
        self.Score = score
        self.Outcome = outcome
        self.NumTurns = num_turns

        # right, down, left, up
        self.DirectionsUsed = {
            'up': 0,
            'down': 0,
            'right': 0,
            'left': 0,
        }
