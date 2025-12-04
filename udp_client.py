import socket

def main():
    server_ip = "127.0.0.1"
    server_port = 5000

    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("UDP client起動")

    roomname=input("roomnameを入力してください")
    token=input("tokenを入力してください")
    message=input("messageを入力してください")

    roomname_bytes=roomname.encode("utf-8")
    token_bytes=token.encode("utf-8")
    message_bytes=message.encode("utf-8")

    header=len(roomname_bytes).to_bytes(1,"big") \
          +len(token_bytes).to_bytes(1,"big")
    body=roomname_bytes+token_bytes+message_bytes
    data=header+body
    sock.sendto(data,(server_ip,server_port))
    print("message送信完了")
    sock.close()

if __name__=="__main__":
    main()