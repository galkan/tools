import os
import fcntl

class Lock:
    
    def __init__(self, filename):
        self.filename = filename
        # This will create it if it does not exist already
        self.handle = open(filename, 'w')
    
    # Bitwise OR fcntl.LOCK_NB if you need a non-blocking lock 
    def acquire(self):
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        
    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)
        
    def __del__(self):
        self.handle.close()

# Usage
try:
    lock = Lock("/tmp/lock_name.tmp")
    lock.acquire()
    # Do important stuff that needs to be synchronized
    .
    .
    .
finally: 
    lock.release()
