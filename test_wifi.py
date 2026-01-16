import socket

ROBOT_IP = "192.168.1.247"
ROBOT_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

try:
    sock.connect((ROBOT_IP, ROBOT_PORT))
    print("✅ CONNEXION OK AVEC L'ARDUINO")
except Exception as e:
    print("❌ ERREUR :", e)

sock.close()
