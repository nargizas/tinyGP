"""
adapted from tiny_gp.java
from Riccardo Poli
"""
from random import randint, seed, random

ADD = 110
SUB = 111
MUL = 112
DIV = 113

FSET_START = ADD
FSET_END = DIV

MAX_LEN = 10000
POPSIZE = 10000
DEPTH = 5
GENERATIONS = 100
TSIZE = 2

PMUT_PER_NODE = 0.05
CROSSOVER_PROB = 0.9


class TinyGP():

    def __init__(self, fname, s) -> None:
        self.fset_start = FSET_START
        self.fset_end = FSET_END

        self.max_len = MAX_LEN
        self.popsize = POPSIZE
        self.depth = DEPTH
        self.generations = GENERATIONS
        self.tsize = TSIZE

        self.pmut_per_node = PMUT_PER_NODE
        self.crossover_prob = CROSSOVER_PROB

        self.pc = 0
        self.fbestpop = 0.0
        self.favgpop = 0.0

        self.program = []
        self.x = [0 for i in range(self.fset_start)]

        self.fitness_cases = 0
        self.var_number = 0
        self.random_number = 0

        self.targets = []
        self.buffer = [0 for _ in range(self.max_len)]

        self.fname = fname
        self.seed = s
        if self.seed >= 0:
            seed(seed)

        self.minrandom = 0
        self.maxrandom = 0
        self.fitness = [0.0 for _ in range(self.popsize)]
        self.setup_fitness(self.fname)
        # print(f"var_number {self.var_number}")
        # print(f"random_number {self.random_number}")
        # print(f"maxrandom {self.maxrandom}")
        # print(f"minrandom {self.minrandom}")
        self.pop = self.create_random_pop(
            self.popsize, self.depth, self.fitness)

        # print(f"population {self.pop}")
        # print(f"fitness {self.fitness}")

        for i in range(self.fset_start):
            self.x[i] = (self.maxrandom - self.minrandom) * \
                random() + self.minrandom
        # print(f"x {self.x}")
        # print(f"fitness {self.fitness}")
        # print(f"targets {self.targets}")

    def run(self) -> float:

        # print(f"current pc {self.pc}")
        primitive = self.program[self.pc]
        self.pc += 1
        # print(f"primitive {primitive}")
        if primitive < self.fset_start:
            # print(f"here")
            # print(self.x[primitive])
            return self.x[primitive]
        if primitive == ADD:
            # print("add")
            return self.run() + self.run()
        if primitive == SUB:
            # print("sub")
            return self.run() - self.run()
        if primitive == MUL:
            # print("mul")
            return self.run() * self.run()
        if primitive == DIV:
            # print("div")
            num = self.run()
            den = self.run()
            # print(den)
            if abs(den) <= 0.001:
                return num
            else:
                return num / den
        print("ERROR in run")
        return 0.0

    def traverse(self, buffer: list[float], buffer_count: int) -> int:
        # print(f"buffer {buffer}")
        # print(f"buffer[{buffer_count}] {buffer[buffer_count]}")
        if buffer[buffer_count] < self.fset_start:
            return buffer_count + 1

        if buffer[buffer_count] == ADD or buffer[buffer_count] == SUB or buffer[buffer_count] == MUL or buffer[buffer_count] == DIV:
            return self.traverse(buffer, self.traverse(buffer, buffer_count + 1))

        return 0

    def setup_fitness(self, fname: str) -> None:
        with open(file=fname) as file:
            for i, line in enumerate(file.readlines()):
                if i == 0:
                    # print(line)
                    self.var_number, self.random_number, self.minrandom, self.maxrandom, self.fitness_cases = [
                        int(x) for x in line.split()]
                    self.targets = [
                        [0 for _ in range(self.var_number+1)] for _ in range(self.fitness_cases)]
                    if (self.var_number + self.random_number) >= self.fset_start:
                        print("too many variables and constants")
                else:
                    if i > self.fitness_cases:
                        print("too many testcases")
                        exit(1)
                    for j in range(self.var_number+1):
                        self.targets[i-1][j] = float(line.split()[j])

    def fitness_function(self, prog: list[float]):
        fit = 0.0
        len = self.traverse(prog, 0)
        for i in range(self.fitness_cases):
            for j in range(self.var_number):
                self.x[j] = self.targets[i][j]
            self.program = prog
            self.pc = 0
            result = self.run()
            fit += abs(result - self.targets[i][self.var_number])
        return (-1)*fit

    def grow(self, buffer: list[float], pos: int, max: int, depth: int) -> int:
        # print("\n")
        # print(f"pos {pos}")
        prim = randint(0, 1)
        # print(f"prim1: {prim}")
        if pos >= max:
            return -1

        if pos == 0:
            prim = 1
        # print(f"prim2: {prim}")

        if prim == 0 or depth == 0:
            # print(f"here")
            prim = randint(0, self.var_number + self.random_number-1)
            buffer[pos] = prim
            return pos + 1

        else:
            # print(f"here2")
            prim = randint(0, FSET_END - FSET_START) + FSET_START
            # print(prim)
            if prim == ADD or prim == SUB or prim == MUL or prim == DIV:
                # print(f"here3")
                buffer[pos] = prim
                return self.grow(buffer, self.grow(buffer, pos+1, max, depth-1), max, depth-1)

        return 0

    def print_indiv(self, buffer: list[str], buffer_counter: int) -> int:
        a1 = 0
        a2 = 0
        if buffer[buffer_counter] < self.fset_start:
            if buffer[buffer_counter] < self.var_number:
                print(f"X{buffer[buffer_counter] + 1 } ", end="")
            else:
                print(self.x[buffer[buffer_counter]], end="")
            return buffer_counter+1

        if buffer[buffer_counter] == ADD:
            print("(", end="")
            a1 = self.print_indiv(buffer, buffer_counter + 1)
            print(" + ", end="")
        if buffer[buffer_counter] == SUB:
            print("(", end="")
            a1 = self.print_indiv(buffer, buffer_counter + 1)
            print(" - ", end="")
        if buffer[buffer_counter] == MUL:
            print("(", end="")
            a1 = self.print_indiv(buffer, buffer_counter + 1)
            print(" * ", end="")
        if buffer[buffer_counter] == DIV:
            print("(", end="")
            a1 = self.print_indiv(buffer, buffer_counter + 1)
            print(" / ", end="")

        a2 = self.print_indiv(buffer, a1)
        print(")", end="")
        return a2

    def create_random_indiv(self, depth: int):
        len = self.grow(self.buffer, 0, self.max_len, depth)
        # print(f"len: {len}")

        while len < 0:
            len = self.grow(self.buffer, 0, self.max_len, depth)

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
        print(f"MAX_LEN={self.max_len}")
        print(f"POPSIZE={self.popsize}")
        print(f"DEPTH={self.depth}")
        print(f"CROSSOVER_PROB={self.crossover_prob}")
        print(f"PMUT_PER_NODE={self.pmut_per_node}")
        print(f"MIN_RANDOM={self.minrandom}")
        print(f"MAX_RANDOM={self.maxrandom}")
        print(f"GENERATIONS={self.generations}")
        print(f"TSIZE={self.tsize}")
        print("----------------------------------")

    def stats(self, fitness: list[float], pop: list[list[int]], gen: int):
        best = randint(0, self.popsize-1)
        # print(f"best {best}")
        node_count = 0
        self.fbestpop = self.fitness[best]
        # print(f"fbestpop {self.fbestpop}")
        self.favgpop = 0.0

        for i in range(self.popsize):
            node_count += self.traverse(self.pop[i], 0)
            # print(f"node_count {node_count}")
            self.favgpop += self.fitness[i]
            # print(f"favgpop {self.favgpop}")
            if self.fitness[i] > self.fbestpop:
                best = i
                # print(f"fitness {self.fitness[i]}")
                # print(f"fbestpop {self.fbestpop}")
                self.fbestpop = self.fitness[i]

        self.avg_len = node_count / self.popsize
        self.favgpop /= self.popsize
        print(
            f"Generation={gen} Avg Fitness={(-1)*self.favgpop} Best Fitness={(-1)*self.fbestpop} Avg Size={self.avg_len}\nBest Individual: ")
        self.print_indiv(self.pop[best], 0)
        print("\n", flush=True)

    def tournament(self, fitness, tsize):
        best = randint(0, self.popsize)
        fbest = -1.0e34
        for i in range(tsize):
            competitor = randint(0, self.popsize-1)
            if (fitness[competitor] > fbest):
                fbest = fitness[competitor]
                best = competitor

        return best

    def negative_tournament(self, fitness, tsize):
        worst = randint(0, self.popsize-1)
        fworst = 1.0e34
        for i in range(tsize):
            competitor = randint(0, self.popsize-1)
            if (fitness[competitor] < fworst):
                fworst = fitness[competitor]
                worst = competitor

        return worst

    def crossover(self, parent1: list[float], parent2: list[float]):

        len1 = self.traverse(parent1, 0)

        len2 = self.traverse(parent2, 0)

        xo1start = randint(0, len1-1)
        xo1end = self.traverse(parent1, xo1start)

        xo2start = randint(0, len2-1)
        xo2end = self.traverse(parent2, xo2start)

        lenoff = xo1start + (xo2end - xo2start) + (len1-xo1end)

        offspring = [0 for i in range(lenoff)]
        offspring[0:xo1start] = parent1[0:xo1start]
        offspring[xo1start: xo1start +
                  (xo2end - xo2start)] = parent2[xo2start: xo2end]
        offspring[xo1start + (xo2end - xo2start)
                              : lenoff] = parent1[xo1end: len1]

        return offspring

    def mutation(self, parent: list[str], pmut: float):
        len = self.traverse(parent, 0)
        parentcopy = parent[:]
        for i in range(len):
            if (random() < pmut):
                mutsite = i
                if (parentcopy[mutsite] < self.fset_start):
                    parentcopy[mutsite] = randint(0,
                                                  self.var_number+self.random_number-1)
                else:
                    if parentcopy[mutsite] == ADD or parentcopy[mutsite] == SUB or parentcopy[mutsite] == MUL or parentcopy[mutsite] == DIV:
                        parentcopy[mutsite] = randint(0, self.fset_end -
                                                      self.fset_start) + self.fset_start

        return parentcopy

    def evolve(self):
        self.print_params()
        self.stats(self.fitness, self.pop, 0)

        for gen in range(1, self.generations):
            if self.fbestpop > -1e-5:
                print("PROBLEM SOLVED\n")
                exit(0)

            for indivs in range(self.popsize):
                if random() < self.crossover_prob:
                    parent1 = self.tournament(self.fitness, self.tsize)
                    parent2 = self.tournament(self.fitness, self.tsize)
                    newind = self.crossover(
                        self.pop[parent1], self.pop[parent2])
                else:
                    parent = self.tournament(self.fitness, self.tsize)
                    newind = self.mutation(
                        self.pop[parent], self.pmut_per_node)

                newfit = self.fitness_function(newind)
                offspring = self.negative_tournament(self.fitness, self.tsize)
                self.pop[offspring] = newind
                self.fitness[offspring] = newfit

            self.stats(self.fitness, self.pop, gen)

        print("PROBLEM NOT SOLVED")
        exit(1)


def main():
    fname = 'problem.dat'

    args = input().strip().split()
    s = -1

    if len(args) == 2:
        s = int(args[0])
        fname = args[1]

    if len(args) == 1:
        fname = args[0]

    tiny_gp = TinyGP(fname, s)
    tiny_gp.evolve()


if __name__ == "__main__":
    main()
