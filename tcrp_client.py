import socket
from tcrp_proto import build_tcrp_header,parse_tcrp_header,OP_create,OP_join,ST_request,ST_ack,ST_done,status_ok,status_error
from tcrp_util import recv_exact
from udp_chat_client import udp_chat

def main():
   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   sock.connect(("127.0.0.1", 6000))
   print("connect with server")

   room_name=input("room_nameを入力してください")
   username=input("usernameを入力してください")
   room_name_bytes=room_name.encode("utf-8")
   username_bytes=username.encode("utf-8")
   header=build_tcrp_header(len(room_name_bytes),
                            OP_create,
                            ST_request,
                            len(username_bytes))

   packet=header+room_name_bytes+username_bytes
   sock.sendall(packet)

   ack_header=recv_exact(sock,32)
   _,_,_,payload_size=parse_tcrp_header(ack_header)
   ack_body=recv_exact(sock,payload_size)
   status=ack_body[0]
   
   if status!=status_ok:
      print(f'エラーが発生しました。(status={status})')
      sock.close()
      return   

   done_header=recv_exact(sock,32)
   _,op2,st2,token_size=parse_tcrp_header(done_header)
   token=recv_exact(sock,token_size).decode("utf-8")
   print("あなたのtokenは: ",token)
   sock.close()

   udp_chat(room_name,token)

if __name__=="__main__":
   main()
