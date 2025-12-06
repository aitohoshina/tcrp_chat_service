import socket

rooms = {
    "hoshina": {
        "host_token": "DUMMY",
        "host_ip": "127.0.0.1",
        "members": {
            "ksksksksksksksksk": {
                "ip": "127.0.0.1",
                "username": "test-user",
            }
        }
    }
}

def main():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0",5000))
    print("UDP server起動")

    while True:
        data,address=sock.recvfrom(4096)
        client_ip,client_port=address
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

        if roomname not in rooms:
            print("そのルームは存在しません")
            continue
        room=rooms[roomname]
        if token not in room["members"]:
            print("tokenが間違ってます")
            continue
        member=room["members"][token]
        if client_ip != member["ip"]:
            print("ipアドレスが一致しません")
            continue
        print("認証完了：",member["username"],"からのメッセージは",message)
        member["udp_addr"]=address
        message_bytes=message.encode("utf-8")

        for t,m in room["members"].items():
            if "udp_addr" not in m:
                continue
            sock.sendto(message_bytes,m["udp_addr"])


        

if __name__=="__main__":
    main()



