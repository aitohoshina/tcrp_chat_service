import socket
from tcrp_proto import build_tcrp_header,parse_tcrp_header,OP_create,OP_join,ST_request,ST_ack,ST_done,status_ok,status_error
from tcrp_util import recv_exact

def main():
   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   sock.connect(("127.0.0.1",6000))
   print("connect with server")

   roomname=input("roomnameを入力してください")
   username=input("名前を入力してください")
   roomname_bytes=roomname.encode("utf-8")
   username_bytes=username.encode("utf-8")

   header=build_tcrp_header(len(roomname_bytes),OP_join,ST_request,len(username_bytes))
   packet=header+roomname_bytes+username_bytes
   sock.sendall(packet)

   ack_header=recv_exact(sock,32)
   _,op,st,payload_size=parse_tcrp_header(ack_header)
   ack_body=recv_exact(sock,payload_size)
   status=ack_body[0]

   if status!=status_ok:
      print(f'エラーが発生しました。(status={status})')
      sock.close()
      return

   done_header=recv_exact(sock,32)
   _,op2,st2,token_size=parse_tcrp_header(done_header)
   done_body=recv_exact(sock,token_size)
   token=done_body.decode("utf-8",errors="replace")
   print("あなたのトークンは： ",token)
   sock.close()

if __name__=="__main__":
   main()
