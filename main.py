from measure import measure
# metody
from randomtemplate import run_randomtemplate
from random_rightdown import run_rightdown
from minmax import run_minmax
from montecarlo import run_montecarlo


if __name__ == '__main__':
    print("MAIN")
    measure(run_montecarlo, 1000, 10)

