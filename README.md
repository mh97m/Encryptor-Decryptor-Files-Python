
# Encrypte , Decrypt Files

This Code Encrypt and Decrypte files of directory that you gave for several times.

Key is generate when run encrypt files and stored in key.txt in the same directory of the python file.

## Performance

This code wrote with asyncio and threading together for fastest run that ever can make...

In this code, the main bottleneck is the I/O operations of reading and writing files, which is why concurrent.futures is used. However, if the code were doing more CPU-bound tasks, multiprocessing might be a better choice.


## Usage

#### Note

python3 is prefix for execute python files in linux.

py is prefix for execute python files in windows.

### Syntax

```bashe
encrypt_decrypt_files.py [-h] {encrypt,decrypt} directory num_encryption
```

### Encrypt

this is example of encrypting files for 3 time.

```bash
python3 encrypt_decrypt_files.py encrypt /home/user/directory 3
```


### Decrypt

this is example of decrypting files for 3 time.

```bash
python3 encrypt_decrypt_files.py decrypt /home/user/directory 3
```


#### Note

For decrypt files you must enter exact the number time that you encrypt files.

-Python encryptor-File encryption-Encrypting files-Encrypt using python-Encrypt files using python-Python decryptor-File decryption-Decrypting files-Decrypt using python-Decrypt files using python
