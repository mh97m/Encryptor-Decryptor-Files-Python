import os

import argparse

from cryptography.fernet import Fernet

from concurrent.futures import ThreadPoolExecutor

import time

def encrypt_file(filename, key, num_encryption):

    with open(filename, 'rb') as file:

        file_data = file.read()

    for i in range(num_encryption):

        fernet = Fernet(key)

        encrypted_data = fernet.encrypt(file_data)

    with open(filename, 'wb') as file:

        file.write(encrypted_data)

def decrypt_file(filename, key, num_encryption):

    with open(filename, 'rb') as file:

        encrypted_data = file.read()

    for i in range(num_encryption):

        fernet = Fernet(key)

        decrypted_data = fernet.decrypt(encrypted_data)

    with open(filename, 'wb') as file:

        file.write(decrypted_data)

def create_key(key_file):

    key = Fernet.generate_key()

    with open(key_file, 'wb') as file:

        file.write(key)

    return key

def get_args():

    parser = argparse.ArgumentParser(description="Encrypt or decrypt all files in a directory")

    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode to run the program in (encrypt or decrypt)")

    parser.add_argument("directory", help="Directory to process")

    parser.add_argument("num_encryption", type=int, help="Number of times each file should be encrypted or decrypted")

    return parser.parse_args()

def main():

    args = get_args()

    key_file = os.path.join(os.getcwd(), 'key.txt')

    if os.path.exists(key_file):

        with open(key_file, 'rb') as file:

            key = file.read()

    else:

        key = create_key(key_file)

    with ThreadPoolExecutor() as executor:

        if args.mode == "encrypt":

            for root, _, files in os.walk(args.directory):

                for file in files:

                    filename = os.path.join(root, file)

                    executor.submit(encrypt_file, filename, key, args.num_encryption)

        elif args.mode == "decrypt":

            for root, _, files in os.walk(args.directory):

                for file in files:

                    filename = os.path.join(root, file)

                    executor.submit(decrypt_file, filename, key, args.num_encryption)

if __name__ == '__main__':

    start = time.monotonic()

    main()

    end = time.monotonic()

    print(f"Operation completed in: {end-start} seconds")

