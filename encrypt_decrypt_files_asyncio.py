import os
import argparse
from cryptography.fernet import Fernet
import asyncio
import time


class EncryptorDecryptor:

    def __init__(self) -> None:
        args = self.getArgs()
        self.mode = args.mode
        self.num_encryption = args.num_enc
        self.directory = args.dir
        self.new_key = args.new_key

        self.keys = []
        args = self.createKeys()

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
        if os.path.exists(keys_file) and not self.new_key:
            with open(keys_file, 'rb') as file:
                keys = file.read()
        else:
            keys = b''
            for i in range(0, self.num_encryption):
                key = Fernet.generate_key()
                keys += key + b' - '
            with open(keys_file, 'wb') as file:
                file.write(keys)
        self.keys = keys.split(b' - ')[0:-1]

    def encryptData(self, file_name):
        with open(file_name, 'rb') as file:
            file_data = file.read()
        for key in self.keys:
            fernet = Fernet(key)
            file_data = fernet.encrypt(file_data)
        with open(file_name, 'wb') as new_file:
            new_file.write(file_data)

    def decryptData(self, file_name):
        with open(file_name, 'rb') as file:
            file_data = file.read()
        for key in reversed(self.keys):
            fernet = Fernet(key)
            file_data = fernet.decrypt(file_data)
        with open(file_name, 'wb') as new_file:
            new_file.write(file_data)

    async def execute(self,file_name):
        if self.mode == 'encrypt':
            self.encryptData(file_name)
        elif self.mode == 'decrypt':
            self.decryptData(file_name)

    async def executeAll(self):
        for root, _, files in os.walk(self.directory):
            tasks = []
            for file in files:
                file_name = os.path.join(root, file)
                tasks.append(asyncio.ensure_future(self.execute(file_name)))

            await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time.monotonic()
    asyncio.run(EncryptorDecryptor().executeAll())
    end = time.monotonic()
    print(f"Operation completed in: {end-start} seconds")
