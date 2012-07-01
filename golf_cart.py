from __future__ import print_function
import argparse
import logging
from threading import Semaphore, Lock, Thread, Condition
from random import random, randint
from time import sleep
import sys
import random
from timeit import Timer

#golf function
def golfer(bid,bucket_size):
    global stash,balls_on_field,collect_ball
    bucket = 0
    call_cart = False

    while True:
        with mutex:
            if  call_cart and stash >= bucket_size:
                print('Golfer ',bid,'got',bucket_size,'balls; Stash:',stash)
                stash -= bucket_size                # call for bucket
                call_cart = False
                bucket = bucket_size
            else:
                call_cart = True

        if call_cart:
            print('Golfer',bid,'calling for bucket')
            with mutex:
                collect_ball = True
            condition.acquire()
            condition.wait()
            condition.release()

    #            stashEmpty.release()                #Wait for stash to be filled
#            stash_available.acquire()

        if bucket > 0:
            for i in range(0,bucket_size):      # for each ball in bucket,
               with mutex:
                   balls_on_field += 1   #   swing
               if collect_ball == True:
                   condition.acquire()
                   condition.wait()
                   condition.release()
               bucket -=1
#               print('Golfer',bid,'hit ball',i)
               print('Golfer' ,bid, 'hit ball',i,' stash:',stash,'field',balls_on_field)
               sleep(random())

#cart function
def cart():
    global stash, balls_on_field,collect_ball

    while True:
#        stashEmpty.acquire()
        with mutex:
            if collect_ball == True:
               condition.acquire()
               sleep(random())
               stash += balls_on_field   # collect balls and deposit in stash
               condition.notifyAll()
               condition.release()
               collect_ball = False
#            stashEmpty.release()
#            stash_available.acquire()

def program_arguments():
    parser = argparse.ArgumentParser(description='Golf Cart Simulator')
    parser.add_argument('--stash', '-s', type=int, default=20, help='stash size', metavar='stash_size')
    parser.add_argument('--golfers', '-g', type=int, default=3, help='number of golfers', metavar='golf_count')
    parser.add_argument('--bucket', '-b', type=int, default=5, help='balls per bucket', metavar='balls_per_bucket')
    return parser

#global counters
stash = 20 #total number of balls in stash
balls_on_field = 0 #total number of balls in the field

#startup function
if __name__ == '__main__':
    global stash
    parser = program_arguments()
    args = parser.parse_args()
#    simulate(args.stash,args.golfers,args.bucket)

    stash_size = args.stash
    golfers = args.golfers
    bucket_size = args.bucket

#    readSwitch = Lightswitch()
    stashEmpty = Semaphore(0)
    mutex =Lock()
    stash_available = Semaphore(0)
    stop_hitting = False
    collect_ball = True
    condition = Condition()

    stash = stash_size
    gthreads = []
    for i in range(golfers):
        gthread = Thread(target=golfer, args=[i, bucket_size])
        gthreads.append(gthread)
        gthread.start()
    cthread = Thread(target=cart, args=[])
    cthread.start()
