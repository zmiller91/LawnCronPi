import os
def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

touch("/home/zmiller/test")