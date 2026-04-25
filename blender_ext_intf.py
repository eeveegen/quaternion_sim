import socket
import time
import threading

UDP_IP = "127.0.0.1"
DATA_PORT = 5005
HB_PORT = 5006 # back connection -> listen for heartbeat

BLENDER_TIMEOUT = 7 # seconds
timeout = False

def watchdog():
    global timeout
    hb_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hb_sock.bind((UDP_IP, HB_PORT))
    hb_sock.settimeout(BLENDER_TIMEOUT)

    while True:
        try:
            hb_sock.recvfrom(1024)
        except socket.timeout:
            timeout = True
            break
    
    hb_sock.close()
    print("Blender process timed out. Terminating.")

def fake_send():
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i = 0

    while True:
        msg = "Running " + str(i)
        print(msg)
        data_sock.sendto(msg.encode(), (UDP_IP, DATA_PORT))
        i = i + 1
        time.sleep(1)

        if i > 15:
            break
        if timeout:
            break
    
    data_sock.close()
    print("Demo finished.")
    return

    
threading.Thread(target=watchdog, daemon=True).start()
data_thread = threading.Thread(target=fake_send, daemon=True)
data_thread.start()

while data_thread.is_alive():
    pass

