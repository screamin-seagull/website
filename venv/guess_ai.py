import random
from heapq import nlargest


class Guesser:
    def __init__(self, target, mutate, gen_size, repro):
        self.target = target
        self.mutate = mutate
        self.gen_size = gen_size
        self.repro = repro
        self.guesses = []
        self.best_guess = [0]
        self.guess_fitness = {}
        self.repro_list = []
        self.current_gen = 1
        for i in range(self.gen_size):
            rand_guess = random.randint(1, 500)
            self.guesses.insert(i, rand_guess)
        for guess in self.guesses:
            if guess == int(self.target):
                fitness = 1.0
                self.guess_fitness[guess] = fitness
            else:
                fitness = 1/abs((float(self.target) - float(guess)))
                self.guess_fitness[guess] = fitness
        self.repro_list = nlargest(self.repro, self.guess_fitness, key=self.guess_fitness.get)
        self.best_guess = nlargest(1, self.guess_fitness, key=self.guess_fitness.get)

    def get_gen(self):
        return "Generation " + str(self.current_gen) + ": " + ' | '.join(str(i) for i in self.guesses)

    def get_best(self):
        return "Top " + str(self.repro) + " of Generation " + str(self.current_gen) + ": " + str(self.repro_list)

    def next_gen(self):
        self.guesses.clear()
        for i in range(1, int(self.gen_size/self.repro)):
            for r_guess in self.repro_list:
                mutation = int(r_guess) + random.randint(-self.mutate, self.mutate)
                self.guesses.append(mutation)

        self.guess_fitness.clear()
        self.repro_list.clear()
        self.best_guess.clear()
        for guess in self.guesses:
            if guess == int(self.target):
                fitness = 1.0
                self.guess_fitness[guess] = fitness
                self.best_guess.append(guess)
            else:
                fitness = 1/abs((float(self.target) - float(guess)))
                self.guess_fitness[guess] = fitness
        self.repro_list = nlargest(self.repro, self.guess_fitness, key=self.guess_fitness.get)
        if not self.best_guess:
            self.best_guess = nlargest(1, self.guess_fitness, key=self.guess_fitness.get)

        self.current_gen += 1
