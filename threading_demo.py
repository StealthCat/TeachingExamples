import threading
import secrets
import random
import time

class RandomPrinter(threading.Thread):

    screenLock = threading.Lock()

    def __init__(self, threadName="Default"):
        threading.Thread.__init__(self, name=threadName)

    def start(self):
        threading.Thread.start(self)

    def run(self):
        self.runTime = random.randint(15,120)

        with RandomPrinter.screenLock:
            time.sleep(0.5)
            print("I am {} and I will run for {} seconds...".format( self.name, self.runTime ))
        
        time.sleep(1)

        self.runCount = 0
        while self.runCount < self.runTime:
            self.runFuzz = secrets.randbelow(10001) / 10000
            time.sleep(self.runFuzz)
            if RandomPrinter.screenLock.acquire(False):
                print("I am {} and my random fuzz was {:.4f} on loop {:04d}".format(self.name, self.runFuzz, self.runCount))
                RandomPrinter.screenLock.release()
            time.sleep(1-self.runFuzz)
            self.runCount += 1

        with RandomPrinter.screenLock:
            print("I am {} and I am done and I did {} loops".format(self.name, self.runCount))
            time.sleep(4)

if __name__ == "__main__":
    workerThreads = [RandomPrinter(threadName=f'RandomPrinter#{i}') for i in range(10)]
    [workerThread.start() for workerThread in workerThreads]
    [workerThread.join() for workerThread in workerThreads]