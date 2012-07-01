from __future__ import print_function
from threading import Semaphore, Lock, Thread
from random import random, randint
from time import sleep
import sys
import random
from timeit import Timer

class Lightswitch:
    def __init__(self):
        self.mutex = Lock()
        self.count = 0

    def lock(self, sem):
        with self.mutex:
            self.count += 1
            if self.count == 1:
                sem.acquire()

    def unlock(self, sem):
        with self.mutex:
            self.count -= 1
            if self.count == 0:
                sem.release()

class BaboonCrossing:
    def __init__(self,max_in_rope):
        self.rope = Lock()
        self.turnstile = Lock()
        self.switches = [Lightswitch(), Lightswitch()]
        self.multiplex = Semaphore(max_in_rope)

    def act_as_baboon(self,my_id, init_side, max_crossings):
        side = init_side
        crossings_cnt = max_crossings
        while True:
#            with self.turnstile:
            self.switches[side].lock(self.rope)
            with self.multiplex:
                print('baboon', my_id, 'crossing from', side_names[side], 'cnt',crossings_cnt )
                sleep(self.generate_random_int(my_id,15))  # simulate crossing
                crossings_cnt -=1
            self.switches[side].unlock(self.rope)
            side = 1 - side
            if crossings_cnt == 0:
                break
            sleep(self.generate_random_int(my_id,3))

    def generate_random_int (self,seed,factor):
        rng = random.Random()
        rng.seed(seed)
        #    random_val = rng.randint(1,10)
        random_val = rng.random()
        #    print ('random',random_val)
        return  random_val*factor

    def simulate(self,num_baboons, tot_crossings):
        bthreads = []
        for i in range(num_baboons):
            bid, bside = i, randint(0, 1)
            bthreads.append(Thread(target=self.act_as_baboon, args=[bid, bside, tot_crossings]))
        for t in bthreads:
            t.start()
        for t in bthreads:
            t.join()

side_names  = ['west', 'east']
ROPE_MAX    = 3
NUM_BABOONS = 20
MAX_NUM_OF_CROSSINGS = 2

def totime():
    bsim = BaboonCrossing(ROPE_MAX)
    bsim.simulate(NUM_BABOONS, MAX_NUM_OF_CROSSINGS)
    print('Simulation Over')

if __name__ == '__main__':
    timer = Timer(totime)
    print("Average Time for 10 test: {:0.3f}s".format(timer.timeit(10)/10))
    print('Test Repeat(5,1):',timer.repeat(5, 1))
