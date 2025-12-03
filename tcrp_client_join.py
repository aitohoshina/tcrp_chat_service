import socket
from tcrp_proto import build_tcrp_header,parse_tcrp_header,OP_create,OP_join,ST_request,ST_ack,ST_done
from tcrp_util import recv_exact,generate_token

def main():
   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   sock.connect(("127.0.0.1",6000))
   print("connect with server")

   roomname=input("roomnameを入力してください")
   username=input("名前を入力してください")
   roomname_bytes=roomname.encode("utf-8")
   username_bytes=username.encode("utf-8")

   header=build_tcrp_header(len(roomname_bytes),OP_join,ST_request,len(username))
   packet=header+roomname_bytes+username_bytes
   sock.sendall(packet)

   ack_header=recv_exact(sock,32)
   _,operation,state,token_size=parse_tcrp_header(ack_header)
   token=recv_exact(sock,token_size).decode("utf-8")
   print("あなたのトークンは： ",token)
   sock.close()
   
if __name__=="__main__":
   main()
