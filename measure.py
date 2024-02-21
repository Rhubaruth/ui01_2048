from time import process_time

import numpy as np

from game import print_grid
from fitness_function import fitness_function
import copy as cp
from data_format import formatted_data, OUTCOME

def measure(fn, max_turns, num_tests = 3, silent: bool = False):
    best_result = formatted_data(score=-np.Inf, outcome=OUTCOME.Loss)
    best_grid = None
    worst_result = formatted_data(score=np.Inf, outcome=OUTCOME.Win)
    worst_grid = None

    tot_result = formatted_data()
    tot_time = 0
    num_wins = 0
    num_losses = 0
    result: formatted_data
    for n in range(num_tests):
        start = process_time()
        result, grid = fn(max_turns)
        end = process_time()
        tot_time += end - start

        tot_result.Score += result.Score
        tot_result.NumTurns += result.NumTurns

        for key, val in result.DirectionsUsed.items():
            tot_result.DirectionsUsed[key] += val

        # Update BestResult
        if result.Score > best_result.Score and int(result.Outcome) >= int(best_result.Outcome):
            best_result = cp.deepcopy(result)
            best_grid = cp.deepcopy(grid)
        # Update WorstResult
        if result.Score < worst_result.Score and int(result.Outcome) <= int(worst_result.Outcome):
            worst_result = cp.deepcopy(result)
            worst_grid = cp.deepcopy(grid)

        # Count Wins and Losses
        if result.Outcome == OUTCOME.Win:
            num_wins += 1
        elif result.Outcome == OUTCOME.Loss:
            num_losses += 1

        # Debug print
        if not silent:
            print(f"Game{n}: {result.Outcome}")
            print_grid(grid, result.Score)
            print(f"curr time{n}: {end - start}")
            print("-------------------------------------------------------")

    print(f"\nBest solution found in {best_result.NumTurns} turns")
    print(f"outcome: {best_result.Outcome}")
    if best_grid is not None:
        print_grid(best_grid, best_result.Score)
    for key, val in best_result.DirectionsUsed.items():
        print(f"Turns {key}: {val} ({val / best_result.NumTurns * 100:.2f}%)")

    print(f"\nWorst solution found in {worst_result.NumTurns} turns")
    print(f"outcome: {worst_result.Outcome}")
    if worst_grid is not None:
        print_grid(worst_grid, worst_result.Score)
    for key, val in worst_result.DirectionsUsed.items():
        print(f"Turns {key}: {val} ({val / worst_result.NumTurns * 100:.2f}%)")

    print("\nAverage data")
    print(f"avg score: {tot_result.Score / num_tests:.3f}")
    print(f"avg turns: {tot_result.NumTurns / num_tests:.3f} ({tot_result.NumTurns})")
    print(f"avg time: {tot_time / num_tests:.2f}s/game")
    print(f"          {tot_time / tot_result.NumTurns:.2f}s/turn")

    print(f"wins: {num_wins}, losses: {num_losses}")
    print(f"not finished games: {num_tests - num_wins - num_losses}")
    if num_wins + num_losses > 0:
        print(f"winrate (of finished games): {num_wins / (num_wins+num_losses):.2f}")
    print(f"winrate (of all games):      {num_wins / num_tests:.2f}")

    print()
    for key, val in tot_result.DirectionsUsed.items():
        print(f"Turns {key}: {val} ({val / tot_result.NumTurns * 100:.2f}%)")

