Encrypte and decrypt files
=========================================================================

This Code Encrypt and Decrypte files of directory taht you gave for 3 times.
You can change the number of encryption in the code.

key.txt generated in the same directory of the python file that include your key for decryption.

This code wrote with asyncio and threading together for fastest run that ever make...

In this code, the main bottleneck is the I/O operations of reading and writing files, which is why concurrent.futures is used. However, if the code were doing more CPU-bound tasks, multiprocessing might be a better choice.


usage: 
  -encrypt_decrypt_files.py [-h] {encrypt,decrypt} directory 


example: 
  - python encrypt_decrypt_files.py encrypt /path/to/directory
  - python encrypt_decrypt_files.py decrypt /path/to/directory
