import struct
import socket
import requests

UDP_IP = "0.0.0.0"
UDP_PORT = 20778

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP}:{UDP_PORT}")

API_URL = "http://localhost:8000/speed"  # your HTTP endpoint

SPEED_OFFSET = 256
OFFSET_CURRENT_RPM = 16
OFFSET_MAX_RPM = 8

while True:
    data, addr = sock.recvfrom(1024)
    print("Packet length:", len(data))

    if len(data) >= SPEED_OFFSET + 4:
        speed_m_s = struct.unpack_from("<f", data, SPEED_OFFSET)[0]
        current_rpm = struct.unpack_from("<f", data, OFFSET_CURRENT_RPM)[0]
        max_rpm = struct.unpack_from("<f", data, OFFSET_MAX_RPM)[0]
        speed_kmh = speed_m_s * 3.6
        speed_mph = speed_m_s * 2.23694
    else:
        speed_m_s = speed_kmh = speed_mph = 0.0

    print(f"Speed: {speed_m_s:.2f} m/s  | {speed_kmh:.2f} km/h | {speed_mph:.2f} mph")
    try:
        speed_mph = float(speed_mph)
        payload = {"speed_mph": speed_mph}
        # print(payload, type(payload["speed_mph"]))
        requests.post(API_URL, json=payload, timeout=0.2)
    except Exception as e:
        print("failed to post speed:", e)