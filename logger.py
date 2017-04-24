

def log(message):
    f = open("/tmp/lclog", "a+b")
    f.write(message)
    f.close()