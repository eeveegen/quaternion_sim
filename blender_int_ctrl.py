# run this file within blender
import bpy
import socket
import threading

print("Start")

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5005))
    sock.settimeout(5.0)
    
    while True:    
        try:
            data, _ = sock.recvfrom(1024)
            msg = data.decode().strip()
            print(msg)
        except socket.timeout:
            print("Timeout -> terminating!")
            break
        
    sock.close()
    print("End")
    
threading.Thread(target=udp_listener, daemon=True).start()