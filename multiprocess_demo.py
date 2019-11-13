import multiprocessing
import secrets
import random
import time


class RandomPrinter(multiprocessing.Process):

    def __init__(self, processName="Default", screenLock=None):
        multiprocessing.Process.__init__(self, name=processName)
        self.screenLock = screenLock

    def start(self):
        multiprocessing.Process.start(self)

    def run(self):
        self.runTime = random.randint(15,120)

        with self.screenLock:
            time.sleep(0.5)
            print("I am {} and I will run for {} seconds...".format( self.name, self.runTime ))
        
        time.sleep(1)

        self.runCount = 0
        while self.runCount < self.runTime:
            self.runFuzz = secrets.randbelow(10001) / 10000
            time.sleep(self.runFuzz)
            if self.screenLock.acquire(False):
                print("I am {} and my random fuzz was {:.4f} on loop {:04d}".format(self.name, self.runFuzz, self.runCount))
                self.screenLock.release()
            time.sleep(1-self.runFuzz)
            self.runCount += 1

        with self.screenLock:
            print("I am {} and I am done and I did {} loops".format(self.name, self.runCount))
            time.sleep(4)

if __name__ == "__main__":
    screenLock = multiprocessing.Lock()
    
    workerProcesses = [RandomPrinter(processName=f'RandomPrinter#{i}', screenLock=screenLock) for i in range(10)]
    [workerProcess.start() for workerProcess in workerProcesses]
    [workerProcess.join() for workerProcess in workerProcesses]