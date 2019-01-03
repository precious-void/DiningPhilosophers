from threading import Thread

class PhilHelpers:
    def left(self, index, numPhil):
        return (index if index > 0 else numPhil) - 1

    def right(self, index, numPhil):
        index += 1
        return index if index < numPhil else 0

class Philosophers(object):
    in_canteen = False
    numPhil = 5
    mutex = [False for i in range(numPhil)]
    status = [0 for i in range(numPhil)]
    semaphor = [False for i in range(numPhil)]

    def left(self, index):
        return PhilHelpers.left(self, index, self.numPhil)

    def right(self, index):
        return PhilHelpers.right(self, index, self.numPhil)

    def neighbour(self, index, step):
        assert(step >= 0 & step < self.numPhil)
        index += step
        if (index >= self.numPhil):
            index -= self.numPhil
        return index

    def tryChangeStatus(self, index, target, step):
        assert(self.status[index] != target)
        if (self.status[index] == target + 1):
            n = self.neighbour(index, step)
            assert(self.status[n] != target + 1); 
            if (self.status[n] != target):
                self.status[index] = target
                if (self.status[n] > target):
                    self.tryChangeStatus(n, target + 1, step)
                return True
        return False

    def __init__(self, name, seat_number, status):
        self.name = name
        self.seat_number = seat_number
        self.t = Thread(target=self, args=(name, seat_number))


    def eat(self, index):
        assert(self.status[index] == 0)
        maxNeighborStatus = max(self.status[self.left(index)], self.status[self.right(index)])
        self.status[index] = maxNeighborStatus + 1
        for i in range(self.numPhil):
            assert(self.status[i] >= 0 & self.status[i] <= self.numPhil)

        if (maxNeighborStatus > 0):
            self.status[index] = 2
            print('Философ {} ждёт и хочет есть'.format(index))


    def stop_eat(self, index):
        stepFirst = 1
        firstNeighbor = self.neighbour(index, 1)
        secondNeighbor = self.neighbour(index, self.numPhil - 1)
        assert(self.status[index] == 1)
        self.status[index] = 0
        if (self.status[firstNeighbor] > self.status[secondNeighbor]):
            firstNeighbor, secondNeighbor = secondNeighbor, firstNeighbor
            stepFirst = self.numPhil - stepFirst
        
        firstWillEat = self.tryChangeStatus(firstNeighbor, 1, stepFirst)
        secondWillEat = self.tryChangeStatus(secondNeighbor, 1, self.numPhil - stepFirst)

        for i in range(self.numPhil):
            assert(self.status[i] & self.status[i] <= self.numPhil)

        if (firstWillEat):
            m_sema[firstNeighbor].signal()
        if (secondWillEat):
            m_sema[secondNeighbor].signal()

        print("Я, {}, закончил есть!".format(self.name))