# run this file within blender
import bpy
import socket
import threading

DATA_TIMEOUT = 5

print("Start")

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5005))
    sock.settimeout(DATA_TIMEOUT)
    
    ack_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:    
        try:
            data, _ = sock.recvfrom(1024)
            ack_sock.sendto("ACK".encode(), ("127.0.0.1", 5006))
            
            msg = data.decode().strip()
            print(msg)
        except socket.timeout:
            print("Timeout -> terminating!")
            break
        
    sock.close()
    print("End")
    
threading.Thread(target=udp_listener, daemon=True).start()