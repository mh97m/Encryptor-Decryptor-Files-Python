import os
import datetime
import argparse
from cryptography.fernet import Fernet
import multiprocessing

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

def process_files(directory, key, num_encryption, mode):
    for root, _, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            if mode == "encrypt":
                encrypt_file(filename, key, num_encryption)
            elif mode == "decrypt":
                decrypt_file(filename, key, num_encryption)

def main():
    args = get_args()

    key_file = os.path.join(os.getcwd(), 'key.txt')
    if os.path.exists(key_file):
        with open(key_file, 'rb') as file:
            key = file.read()
    else:
        key = create_key(key_file)

    processes = []
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=process_files, args=(args.directory, key, args.num_encryption, args.mode))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == '__main__':
    start = datetime.datetime.now()

    main()

    end = datetime.datetime.now()

    print("Operation completed! in : ' " + str(end-start) + " '")
