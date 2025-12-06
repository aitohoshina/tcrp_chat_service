import socket
import threading

def udp_chat(roomname:str,token:str,server_ip="127.0.0.1",server_port=5000):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect((server_ip,server_port))
    print("chat start in ",roomname, "token=",token)

    roomname_bytes=roomname.encode("utf-8")
    token_bytes=token.encode("utf=8")

    def recv_loop():
        while True:
            data,addr=sock.recvfrom(4096)
            messege=data.decode("utf-8",errors="replace")
            print(messege)

    threading.Thread(target=recv_loop,daemon=True).start()

    while True:
        text=input("> ")
        text_bytes=text.encode("utf-8")
        header=len(roomname_bytes).to_bytes(1,"big")+len(token_bytes).to_bytes(1,"big")
        body=roomname_bytes+token_bytes+text_bytes
        packet=header+body
        sock.sendto(packet,(server_ip,server_port))



