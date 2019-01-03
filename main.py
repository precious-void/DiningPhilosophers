from threading import Thread, Lock
import time
import random
import logging


global numPhil, timeout, counter, forks

logger = logging.getLogger('PhilosophsLogger')
logging.basicConfig(level=logging.DEBUG)

numPhil = 5
timeout = 30
debug = True

logger.propagate = debug
counter = [0 for i in range(numPhil)]
forks = [Lock() for i in range(numPhil)]


class Philosopher(Thread):
    def __init__(self, name, index, left, right):
        super(Philosopher, self).__init__()
        self.index = index
        self.name = name
        self.left = left
        self.right = right
        logger.debug('Появился философ {} номер {}'.format(name, index))

    # Start eating
    def run(self):
        if forks[max(self.left, self.right)].acquire():
            logger.debug('Философ {} номер {} взял левую вилку'.format(self.name, self.index))
            time.sleep(random.randint(1, 10)/100)

            if forks[min(self.left, self.right)].acquire():
                logger.debug('Философ {} номер {} взял правую вилку и начал есть'.format(self.name, self.index))

                time.sleep(random.randint(1, 10)/10)
                logger.debug('Философ {} номер {} поел'.format(self.name, self.index))

                forks[self.left].release()
                forks[self.right].release()

                counter[self.index - 1] += 1
            else:
                forks[max(self.left, self.right)].release()

            time.sleep(random.randint(1, 10)/10)
        
        self.run()

def start_play(numPhil):
    random.seed(507129)
    
    phil = []
    for i in range(1, numPhil+1):
        phil.append(Philosopher('Phil'+str(i), i, i%5, (i+1)%5))

    for i in phil: i.start()
        
    for i in phil: i.join(timeout)
    
    
if __name__ == '__main__':
    try:
        print('Debug: %s' % str(debug))
        t = Thread(target=start_play, args=(numPhil, ))
        t.daemon = True
        t.start()
        t.join(timeout)
    finally:
        logger.debug('Finished')
        print('Timeout: %d seconds' % timeout)
        print('Number of Philosophs: %d' % numPhil)
        print(counter)
