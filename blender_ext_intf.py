import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(15):
    msg = "Running " + str(i)
    print(msg)
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    time.sleep(1)

print("Completed!")

