from datetime import datetime
from colorama import Fore, init
import threading

init()

mutex = threading.Lock()

class SimpleLogger:
    def __init__(self):
        pass
    def timestamp(self):
        return str(datetime.now())[:-3]
    def yellow(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.YELLOW + str(message) + Fore.RESET)
        mutex.release()
    def green(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.LIGHTGREEN_EX + str(message) + Fore.RESET)
        mutex.release()
    def red(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.RED + str(message) + Fore.RESET)
        mutex.release()
    def pink(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.LIGHTRED_EX + str(message) + Fore.RESET)
        mutex.release()
    def grey(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.LIGHTBLACK_EX + str(message) + Fore.RESET)
        mutex.release()
    def white(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.LIGHTWHITE_EX + str(message) + Fore.RESET)
        mutex.release()
    def blue(self, message):
        mutex.acquire()
        print("[" + self.timestamp() + "] " + Fore.LIGHTBLUE_EX + str(message) + Fore.RESET)
        mutex.release()