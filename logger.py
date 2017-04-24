from datetime import datetime

def log(file, message):
    f = open("/tmp/lclog", "a+b")
    f.write("{0}\t{1}\t{2}\n".format(str(datetime.now()), file, message))
    f.close()