from __future__ import print_function
import argparse
import logging
from threading import Semaphore, Lock, Thread
from random import random
from time import sleep

#golf function
def golfer(bid, bucket_size):
    global stash, balls_on_field, collect_ball
    bucket = 0
    call_cart = False

    while True:
        with mutex:
            if  call_cart and stash >= bucket_size:
                stash -= bucket_size
                print('Golfer', bid, 'got', bucket_size, 'balls; Stash =', stash)
                call_cart = False
                bucket = bucket_size
            else:
                call_cart = True

        if call_cart:
            print('Golfer', bid, 'calling for bucket')
            with mutex:
                if stash < bucket_size:
                    #print('Enabing collect_ball:',collect_ball,'stash',stash)
                    collect_ball = True

        if bucket > 0:
            for i in range(0, bucket_size):      # for each ball in bucket,
                with mutex:
                    balls_on_field += 1   #   swing
                    bucket -= 1
                    sleep(random())
                    print('Golfer', bid, 'hit ball', i)#, ' stash:', stash, 'field', balls_on_field)

#cart function
def cart():
    global stash, balls_on_field, collect_ball

    while True:
        with mutex:
            if collect_ball == True:
                print('##################################################################')
                print('Stash = ', stash, '; Cart entering field')
                stash += balls_on_field   # collect balls and deposit in stash
                print('Cart done, gathered', balls_on_field, 'balls; Stash', stash)
                print('##################################################################')
                sleep(random())
                balls_on_field = 0
                collect_ball = False

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

    stash_size = args.stash
    golfers = args.golfers
    bucket_size = args.bucket

    #    readSwitch = Lightswitch()
    stashEmpty = Semaphore(0)
    mutex = Lock()
    stash_available = Semaphore(0)
    collect_ball = False

    stash = stash_size
    gthreads = []
    for i in range(golfers):
        gthread = Thread(target=golfer, args=[i, bucket_size])
        gthreads.append(gthread)
        gthread.start()
    cthread = Thread(target=cart, args=[])
    cthread.start()
