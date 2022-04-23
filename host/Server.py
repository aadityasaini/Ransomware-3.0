import socket
import os
# import sys
import time
# import threading
PORT=5678
SERVER=socket.gethostbyname(socket.gethostname())
# SERVER='192.168.1.16'
ADDR=(SERVER,PORT)
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
def handle_client(conn, addr):
    def delete_line(original_file, line_number):
        say = 0
        """ Delete a line from a file at the given line number """
        is_skipped = False
        current_index = 0
        dummy_file = original_file + '.bak'
        # Open original file in read only mode and dummy file in write mode
        with open(original_file, 'rb') as read_obj, open(dummy_file, 'wb') as write_obj:
            # Line by line copy data from original file to dummy file
            for line in read_obj:
                # If current line number matches the given line number then skip copying
                if current_index != line_number:
                    write_obj.write(line)

                    say = say + 1
                else:

                    is_skipped = True
                current_index += 1

        if is_skipped:
            os.remove(original_file)
            os.rename(dummy_file, original_file)

        else:
            os.remove(dummy_file)

    # sys.stdout = open("server_log.txt", "a")
    print(f'\n[NEW CONNECTION] {addr} connected.\n')
    # sys.stdout.close()
    with conn:
        host_key = conn.recv(1024).decode('utf-8')
        msg, host, key = host_key.split(': ')
        hostandkey = host + ": " + key
        # sys.stdout = open("server_log.txt", "a")
        print(f'[{msg}]')
        # sys.stdout.close()
        if msg == 'Decrypter':
            if os.path.exists("encrypted_hosts.txt"):
                pass
            else:
                with open("encrypted_hosts.txt", "w") as file1:
                    pass
            with open("encrypted_hosts.txt", "r") as file1:
                # setting flag and index to 0
                flag = 0
                index = (-1)
                # Loop through the file line by line
                for line in file1:
                    index += 1
                    read_line = line
                    read_line = read_line.strip()
                    try:
                        date, hot, rkey = read_line.split(': ')
                        rockey = hot + ": " + rkey
                        # checking string is present in line or not
                        if rockey == hostandkey:
                            flag = 1
                            break
                    except:
                        pass

                    # checking condition for string found or not
            if flag == 0:
                # sys.stdout = open("server_log.txt", "a")
                print(f"[{time.asctime(time.localtime(time.time()))}] The key entered by {host}: {key} didn't match any encrypted host!")
                # sys.stdout.close()
                conn.send(bytes("no", 'utf-8'))
                # break
                # print('String', string1, 'Not Found')
            else:
                conn.send(bytes("yes", 'utf-8'))
                delete_line("encrypted_hosts.txt", index)
                with open('decrypted_hosts.txt', 'a') as su:
                    su.write(f'[{time.asctime(time.localtime(time.time()))}]: {hostandkey}' + '\n')
                # sys.stdout = open("server_log.txt", "a")
                print(f'[{time.asctime(time.localtime(time.time()))}] {host} successfully decrypted with key: {key}')
                # sys.stdout.close()
        elif msg == 'Encrypter':
            if os.path.exists("encrypted_hosts.txt"):
                pass
            else:
                with open("encrypted_hosts.txt", "w") as file1:
                    pass
            with open('encrypted_hosts.txt', 'r') as f:
                readdata = f.read()
                if host in readdata:
                    conn.send(bytes("no", 'utf-8'))
                    # sys.stdout = open("server_log.txt", "a")
                    print(f"[{time.asctime(time.localtime(time.time()))}] {host} already encrypted with key: {key}")
                    # sys.stdout.close()
                    f.close()
                else:
                    conn.send(bytes("yes", 'utf-8'))
                    with open('encrypted_hosts.txt', 'a') as f:
                        f.write(f'[{time.asctime(time.localtime(time.time()))}]: {hostandkey}' + '\n')
                        # sys.stdout = open("server_log.txt", "a")
                        print(f'[{time.asctime(time.localtime(time.time()))}] {host} successfully encrypted with key: {key}')
                        # sys.stdout.close()
                        f.close()
    # sys.stdout = open("server_log.txt", "a")
    print(f"\n[DROPPED CONNECTION] {addr} disconnected.")
    print(f'\n[Listening] Server is listening for connections on [{SERVER}]')
    # sys.stdout.close()

def start():
    server.listen(5)
    # sys.stdout = open("server_log.txt", "a")
    print(f'\n[Listening] Server is listening for connections on [{SERVER}]')
    # sys.stdout.close()
    while True:
        conn, addr=server.accept()
        handle_client(conn,addr)
        # thread= threading.Thread(target=handle_client,args=(conn,addr))
        # thread.start()
        # print(f'[ACTIVE CONNECTIONS] {threading.activeCount()-1}\n')
# sys.stdout = open("server_log.txt", "a")
print(f"[{time.asctime(time.localtime(time.time()))}] Starting server...")
# sys.stdout.close()
start()