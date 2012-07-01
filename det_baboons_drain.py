from __future__ import print_function
from threading import Semaphore, Lock, Thread, Condition
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
        self.mutex = Lock()

        self.max_in_rope = max_in_rope
        self.load = 0
        self.draining = False
        self.condition = Condition()

    def act_as_baboon(self,my_id, init_side, max_crossings):
        side = init_side
        crossings_cnt = max_crossings
        while True:
#            print('Bef Turnstile', my_id,'side',side_names[side])
            #Draining is enabled, so block baboons getting into the rope

            if self.draining == True:
                print('Draining baboon',my_id)
                self.condition.acquire()
                self.condition.wait()
                self.condition.release()

            with self.turnstile:
#                print('After Turnstile', my_id,'side',side_names[side])
                self.switches[side].lock(self.rope)
#                print('After Switch', my_id,'side',side_names[side])
            with self.multiplex:
                with self.mutex:
                    self.load += 1
                    #If Rope load is max, then enable draining
                    if self.load  == self.max_in_rope:
                        self.draining = True
                        print('Draining Enabled after baboon',my_id)

#                print('baboon', my_id, 'crossing from', side_names[side], 'cnt',crossings_cnt, 'load',self.load )
                sleep(self.generate_random_int(my_id,15))  # simulate crossing
                crossings_cnt -=1
                with self.mutex:
                    self.load -= 1
                    #disable draining when last baboon in rope has crossed
                    if self.draining == True and  self.load  == 0:
                        self.draining = False
                        self.condition.acquire()
                        self.condition.notifyAll()
                        self.condition.release()
                        print('Draining Disabled',my_id)

#            print('After Cross', my_id,'side',side_names[side])
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

if __name__ == '__main__':
    timer = Timer(totime)
    print("Average Time for 10 test: {:0.3f}s".format(timer.timeit(10)/10))
    print('Test Repeat(5,1):',timer.repeat(5, 1))
