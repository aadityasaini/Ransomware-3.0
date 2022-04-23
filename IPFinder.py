import socket
url=input("Enter URL to find IP address: ")
print(socket.gethostbyname(url))
input("Press Enter to exit: ")