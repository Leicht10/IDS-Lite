import socket
import time
import logging


my_logger = logging.getLogger("IDS_Lite")
my_logger.setLevel(logging.INFO)


file_handler = logging.FileHandler("events.log")
formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s - %(name)s :: %(message)s"
)
file_handler.setFormatter(formatter)
my_logger.addHandler(file_handler)

N = 5           
T = 10          
BAN_TIME = 30   

current_ip = None
timestamps = []
blacklist = {}  


u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
u.bind(("127.0.0.1", 9999))
u.settimeout(5.0)

print("IDS Lite running...")

try:
    while True:
        try:
            data, addr = u.recvfrom(3072)
        except socket.timeout:
            print("No packets in 5 seconds")
            continue

        ts = time.time()
        ip = addr[0]

        if ip in blacklist:
            if ts - blacklist[ip] < BAN_TIME:
                my_logger.info(f"DROPPED packet from blacklisted IP: {ip}")
                continue
            else:
                del blacklist[ip]

        if ip != current_ip:
            current_ip = ip
            timestamps = []

        timestamps.append(ts)

        timestamps = [t for t in timestamps if ts - t <= T]

        if len(timestamps) > N:
            my_logger.warning(f"BURST detected from {ip} — {len(timestamps)} packets in {T}s")
            blacklist[ip] = ts
            continue  

        print(f"{ts:.3f} - {ip}:{addr[1]} - {len(data)} bytes")

except KeyboardInterrupt:
    print("\nServer terminated")
finally:
    u.close()
