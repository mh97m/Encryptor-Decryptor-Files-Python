#!/usr/bin/env python
import os
import sys
import time
import argparse
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor


class EncryptorDecryptor:

    def __init__(self) -> None:
        args = self.getArgs()
        self.mode = args.mode
        self.num_encryption = args.num_enc
        self.directory = args.dir
        self.chunk_size = 1024 * 1024 * 1024
        self.new_key = args.new_key

        self.keys = self.createKeys()

    def getArgs(self):
        parser = argparse.ArgumentParser(
            description='Encrypt or decrypt all files in a directory')
        parser.add_argument('--mode', choices=[
                            'encrypt', 'decrypt'], help='Mode to run the program in (encrypt or decrypt)')
        parser.add_argument('--dir', help='Directory to process')
        parser.add_argument('--num-enc', type=int, default=1,
                            help='Number of times each file should be encrypted or decrypted')
        parser.add_argument('--new-key', type=bool, default=False,
                            help='Make new key for encryption')
        return parser.parse_args()

    def createKeys(self):
        keys_file = os.path.join(os.getcwd(), 'key.txt')
        if self.new_key and self.mode == 'encrypt':
            keys = b''
            for i in range(0, self.num_encryption):
                key = Fernet.generate_key()
                keys += key + b' - '
            with open(keys_file, 'wb') as file:
                file.write(keys)
        elif os.path.exists(keys_file):
            with open(keys_file, 'rb') as file:
                keys = file.read()
        else:
            print('Key encryption not exists')
            exit()
        return keys.split(b' - ')[0:-1]

    def encryptData(self, file_name):
        with open(file_name, 'rb') as file:
            file_data = file.read()
        new_file_data = b''
        file_size = sys.getsizeof(file_data)
        chunk_size = self.chunk_size if self.chunk_size < len(file_data) else len(file_data)-1 
        for i in range(0, len(file_data), chunk_size):
            data = file_data[i:i+chunk_size]
            for key in self.keys:
                fernet = Fernet(key)
                data = fernet.encrypt(data)
            new_file_data += data
            time.sleep(file_size / (100  * 1024 * 1024))
        with open(file_name, 'wb') as new_file:
            new_file.write(new_file_data)

    def decryptData(self, file_name):
        with open(file_name, 'rb') as file:
            file_data = file.read()
        new_file_data = b''
        file_size = sys.getsizeof(file_data)
        chunk_size = self.chunk_size if self.chunk_size < len(file_data) else len(file_data)
        for i in range(0, len(file_data), chunk_size):
            data = file_data[i:i+chunk_size]
            for key in reversed(self.keys):
                fernet = Fernet(key)
                data = fernet.decrypt(data)
            new_file_data += data
            time.sleep(file_size / (100  * 1024 * 1024))
        with open(file_name, 'wb') as new_file:
            new_file.write(new_file_data)

    def execute(self):
        with ThreadPoolExecutor() as executor:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    file_name = os.path.join(root, file)
                    if self.mode == 'encrypt':
                        executor.submit(self.encryptData, file_name)
                    elif self.mode == 'decrypt':
                        executor.submit(self.decryptData, file_name)


if __name__ == '__main__':
    start = time.monotonic()
    EncryptorDecryptor().execute()
    end = time.monotonic()
    print(f"Operation completed in: {end-start} seconds")


        # with ThreadPoolExecutor() as executor:
        #     for root, _, files in os.walk(self.directory):
        #         for file in files:
        #             filename = os.path.join(root, file)
        #             with open(filename, 'rb') as file:
        #                 file_data = file.read()
        #                 for i in range(0, len(file_data), self.chunk_size):
        #                     data = file_data[i:i+self.chunk_size]
        #                     if self.mode == 'encrypt':
        #                         executor.submit(self.encryptData, data)
        #                     elif self.mode == 'decrypt':
        #                         executor.submit(self.decryptData, data)
        #             print(self.new_file_data, self.key)
        #             exit()
        #             with open(filename, 'wb') as new_file:
        #                 new_file.write(self.new_file_data)
