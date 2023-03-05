"""
adapted from tiny_gp.java
from Riccardo Poli
"""
from ast import keyword
from random import randint, seed, random

ADD = 110
SUB = 111
MUL = 112
DIV = 113

FSET_START = ADD
FSET_END = DIV

MAX_LEN = 10000
POPSIZE = 100000
DEPTH = 5
GENERATIONS = 100
TSIZE = 3

PMUT_PER_NODE = 0.05
CROSSOVER_PROB = 0.9


class TinyGP():

    def __init__(self, keywords_file, fname, s) -> None:
        self.pc = 0
        self.fbestpop = 0.0
        self.favgpop = 0.0

        self.program = []
        self.x = [0 for i in range(FSET_START)]

        self.fitness_cases = 0
        self.var_number = 0
        self.random_number = 0

        self.targets = []
        self.buffer = [0 for _ in range(MAX_LEN)]

        self.keywords_file = keywords_file
        self.keywords_dict = {}
        self.fname = fname
        self.seed = s
        if self.seed >= 0:
            seed(seed)

        self.setup_keywords(self.keywords_file)
        # self.pop = self.create_random_pop(
        #     POPSIZE, DEPTH, self.fitness)

        # for i in range(FSET_START):
        #     self.x[i] = (self.maxrandom - self.minrandom) * \
        #         random() + self.minrandom

    def traverse(self, buffer: list[float], buffer_count: int) -> int:
        if buffer[buffer_count] < FSET_START:
            return buffer_count + 1

        if buffer[buffer_count] == ADD or buffer[buffer_count] == SUB or buffer[buffer_count] == MUL or buffer[buffer_count] == DIV:
            return self.traverse(buffer, self.traverse(buffer, buffer_count + 1))

        return 0

    def setup_keywords(self, keywords_file) -> None:
        with open(file=keywords_file) as file:
            for i, line in enumerate(file.readlines()):
                temp = line.split()
                if temp[1] == "-":
                    continue

                self.keywords_dict[temp[0]] = " ".join(temp[1:])
        print(self.keywords_dict)

    def grow(self, buffer: list[float], pos: int, max: int, depth: int) -> int:

        prim = randint(0, 1)
        if pos >= max:
            return -1

        if pos == 0:
            prim = 1

        if prim == 0 or depth == 0:
            prim = randint(0, self.var_number + self.random_number-1)
            buffer[pos] = prim
            return pos + 1

        else:
            prim = randint(0, FSET_END - FSET_START) + FSET_START
            if prim == ADD or prim == SUB or prim == MUL or prim == DIV:
                buffer[pos] = prim
                return self.grow(buffer, self.grow(buffer, pos+1, max, depth-1), max, depth-1)
        return 0

    def create_random_indiv(self, depth: int):
        len = self.grow(self.buffer, 0, MAX_LEN, depth)

        while len < 0:
            len = self.grow(self.buffer, 0, MAX_LEN, depth)

        ind = self.buffer[0:len]
        return ind

    def create_random_pop(self, n, depth, fitness):
        pop = [0 for i in range(n)]
        for i in range(n):
            pop[i] = self.create_random_indiv(depth)
            fitness[i] = self.fitness_function(pop[i])
            # if fitness[i] == 0:
            # print(i)
        return pop

    def print_params(self) -> None:
        print("-- TINY GP (Python version) --\n")
        print(f"SEED={self.seed}")
        print(f"MAX_LEN={MAX_LEN}")
        print(f"POPSIZE={POPSIZE}")
        print(f"DEPTH={DEPTH}")
        print(f"CROSSOVER_PROB={CROSSOVER_PROB}")
        print(f"PMUT_PER_NODE={PMUT_PER_NODE}")
        print(f"MIN_RANDOM={self.minrandom}")
        print(f"MAX_RANDOM={self.maxrandom}")
        print(f"GENERATIONS={GENERATIONS}")
        print(f"TSIZE={TSIZE}")
        print("----------------------------------")


def main():
    keywords_file = 'keywords.dat'
    problem_file = 'problems/problemC.dat'

    args = input().strip().split()
    s = -1

    if len(args) == 2:
        s = int(args[0])
        fname = args[1]

    if len(args) == 1:
        fname = args[0]

    tiny_gp = TinyGP(keywords_file, problem_file, s)


if __name__ == "__main__":
    main()
