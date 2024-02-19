from time import process_time
from game import print_grid
from fitness_function import fitness_function
import copy as cp
from data_format import formatted_data, OUTCOME

def measure(fn, max_turns, num_tests = 3, silent: bool = False):
    best_result = formatted_data(0, OUTCOME.NotComplete, 0)
    best_grid = None
    tot_result = formatted_data(0, OUTCOME.NotComplete, 0)
    tot_time = 0
    num_wins = 0
    num_losses = 0
    result: formatted_data
    for n in range(num_tests):
        start = process_time()
        result, grid = fn(max_turns)
        tot_result.Score += result.Score
        tot_result.NumTurns += result.NumTurns
        if result.Score > best_result.Score and int(result.Score) > int(best_result.Score):
            if best_result.Outcome != OUTCOME.Win or result.Outcome == OUTCOME.Win:
                best_result = cp.deepcopy(result)
                best_grid = cp.deepcopy(grid)
        if result.Outcome == OUTCOME.Win:
            num_wins += 1
        elif result.Outcome == OUTCOME.Loss:
            num_losses += 1
        if not silent:
            print(f"Game{n}: {result.Outcome}")
            print_grid(grid, result.Score)
            print(f"curr time{n}: {process_time() - start}")
            print("-------------------------------------------------------")
        tot_time += process_time() - start

    print(f"\nBest solution found in {best_result.NumTurns} turns")
    print(f"outcome: {best_result.Outcome}")
    if best_grid is not None:
        print_grid(best_grid, best_result.Score)

    print("\nAverage data")
    print(f"avg score: {tot_result.Score / num_tests}")
    print(f"avg turns: {tot_result.NumTurns / num_tests}")
    print(f"avg time: {tot_time / num_tests:.2f}s/game")
    print(f"          {tot_time / tot_result.NumTurns:.2f}s/turn")
    print(f"wins/finished: {num_wins}/{num_wins+num_losses} = ", end="")
    print(f"{(num_wins/num_wins+num_losses) if num_wins+num_losses != 0 else 0:.3f}")
