import socket
import serial
import time
import threading

### ---

# serial port variables
SERIAL_PORT = "COM3"
SERIAL_RATE = 115200

# blender script communication variables
UDP_IP = "127.0.0.1"
DATA_PORT = 5005
HB_PORT = 5006 # back connection -> listen for heartbeat

# custom timeout
BLENDER_TIMEOUT = 7 # seconds

### ---

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
    ser = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_RATE, timeout=5)

    while True:
        msg = ser.readline()
        print(msg)
        data_sock.sendto(msg, (UDP_IP, DATA_PORT))

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

