import socket
def main():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0",5000))
    print("UDP server起動")

    while True:
        data,address=sock.recvfrom(4096)
        if len(data)<2:
            print("dataが短すぎます")
            continue
        roomname_size=data[0]
        token_size=data[1]
        roomname=data[2:2+roomname_size].decode("utf-8",errors="replace")
        token=data[2+roomname_size:2+roomname_size+token_size].decode("utf-8",errors="replace")
        message=data[2+roomname_size+token_size:].decode("utf-8",errors="replace")
        print("roomname: ",roomname)
        print("token: ",token)
        print("message: ",message)



