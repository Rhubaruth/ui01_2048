from game import *
from fitness_function import fitness_function

def run_randomtemplate():
    #Random direction solver
    grid, score = new_game()
    has_win: bool = False
    i: int = 0
    for i in range(1000):
        direction = np.random.choice(('left','right','up','down'))
        try:
            grid, score = play_2048(grid, direction, score)
        except RuntimeError as inst:
            if str(inst)== "GO":
                print("GAME OVER in ",(i+1)," moves")
            elif str(inst)== "WIN":
                print("WIN in ",(i+1)," moves")
                has_win = True 
            break
    print_grid(grid, score)
    print(f"fitness: {fitness_function(grid, score)}")
    return {
        "score": score,
        "has_win": has_win,
        "num_turns:": i+1,
    }