from threading import Thread, Lock, BoundedSemaphore
import time

global numPhil, timeout, counter, semaphore 

numPhil = 5
timeout = 100
counter = [0 for i in range(numPhil)]
semaphore = BoundedSemaphore(numPhil - 2)


class Philosopher(Thread):

    def __init__(self, name, index, left, right):
        super(Philosopher, self).__init__()
        self.index = index
        self.name = name
        self.left = left
        self.right = right
        print('Появился философ {} номер {}'.format(name, index))

    # Start eating
    def run(self):
        semaphore.acquire()

        self.left.acquire()
        # print('Философ {} номер {} взял левую вилку'.format(self.name, self.index))
        time.sleep(0.05)

        self.right.acquire()
        # print('Философ {} номер {} взял правую вилку и начал есть'.format(self.name, self.index))

        time.sleep(1)
        # print('Философ {} номер {} поел'.format(self.name, self.index))

        self.left.release()
        self.right.release()
        semaphore.release()
        time.sleep(1)
        counter[self.index - 1] += 1

        self.run()

def start_play(numPhil):
    
    forks = [Lock() for i in range(numPhil)]
    
    phil = []
    for i in range(1, numPhil+1):
        phil.append(Philosopher('Phil'+str(i), i, forks[i-2], forks[i-1]))

    for i in phil:
        i.start()
        
    for i in phil:
        i.join(timeout)
    
    
if __name__ == '__main__':
    try:
        t = Thread(target=start_play, args=(numPhil, ))
        t.daemon = True
        t.start()
        t.join(timeout)

    finally:
        print('finished')
        print(counter)
    # k = 0
    # numPhil = 5
    # lock = BoundedSemaphore(1)
    # while (k < 3):
    #     t = Thread(target=start_play, args=(numPhil, lock))
    #     t.start()
    #     t.join()
    #     k+=1
