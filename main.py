from concurrent.futures import ThreadPoolExecutor
from itertools import product
from time import time

import rarfile

rarfile.UNRAR_TOOL = "UnRAR.exe"


class RARCracker:
    def __init__(self, file, save_file=None, path=None, workers=30, chars=None):
        self.cracked = False
        self.file = file
        self.path = path
        self.save_file = save_file
        self.time_started = time()
        self.workers = workers
        self.chars = chars or "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&*-_+=~`.?"

    def save_try(self, password):
        with open(self.save_file, "a") as f:
            f.write(f"{password}\n")

    def crack(self, password):
        try:
            if not self.cracked:
                rf = rarfile.RarFile(self.file)

                if self.save_file:
                    self.save_try(password)

                rf.extractall(self.path, pwd=password)

                print(f"[+] Password found: {password}")
                print(f"Elapsed time: {time() - self.time_started:.0f} seconds")

                if self.save_file:
                    self.save_try(f"{password} << Cracked!")

                self.cracked = True
            else:
                return
        except rarfile.RarWrongPassword:
            pass

    def main(self):
        length = 1
        count = 0
        save_file = None

        if self.save_file:
            save_file = open(self.save_file, "r").read()
            if 'Cracked!' in save_file:
                print("[!] File already cracked!")
                return

        while True:
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                for password in product(self.chars, repeat=length):
                    password = ''.join(password)
                    # Check if the password is already in save_file
                    if save_file:
                        if password in save_file:
                            continue
                    executor.submit(self.crack, password)
                    count += 1
                    if self.cracked:
                        break
            if self.cracked:
                break

            length += 1
            print(f"Trying length: {length}, count: {count}")


if __name__ == '__main__':
    rar = RARCracker('test.rar')  # Test password is ab5
    rar.main()
