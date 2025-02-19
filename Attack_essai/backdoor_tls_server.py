import ssl
import socket

# Create TLS context for TLS 1.2 only
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.options |= ssl.OP_NO_TLSv1_3  # Explicitly disable TLS 1.3
context.set_ciphers("DHE-RSA-AES256-GCM-SHA384")  # Only use DH ciphers
context.load_cert_chain(certfile="mycert.pem", keyfile="mykey.pem")
context.load_dh_params("backdoor_DH.pem")  # Use backdoored DH parameters

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 443))  # Listen on port 443
server_socket.listen(5)

print("[🔹] Python TLS Server Running on Port 443 (Forcing TLS 1.2 with DHE)")

while True:
    client_socket, addr = server_socket.accept()
    with context.wrap_socket(client_socket, server_side=True) as tls_conn:
        print(f"[✅] Client Connected: {addr}")
        tls_conn.send(b"Hello, this is a backdoored TLS server.\n")
