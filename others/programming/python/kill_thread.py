import time
import threading

class MyThread(threading.Thread):

        def __init__(self, val):

                self.__val = val
                yhreading.Thread.__init__(self)
                self.stop = False


        def run(self):

                while not self.stop:
                        write_file = open("/tmp/tmp.txt", "a")
                        write_file.write("self.__val")
                        write_file.close()
                        time.sleep(2)


if __name__ == "__main__":
        th = MyThread("Deneme Icerik")
        th.start()
        th.stop = True
