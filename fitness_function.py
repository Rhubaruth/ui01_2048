import numpy as np

def fitness_function(grid: np.array, score: int):
    """
    :param grid: 
    :param score: 
    :return: 
    """
    non_zero = np.count_nonzero(grid)

    return np.sum(grid) / non_zero + score
