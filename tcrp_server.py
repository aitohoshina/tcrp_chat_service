import socket
from tcrp_proto import build_tcrp_header,parse_tcrp_header,OP_create,OP_join,ST_request,ST_ack,ST_done
from tcrp_util import recv_exact,generate_token

rooms={}

def main():
   server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   server_sock.bind(("0.0.0.0", 6000))
   server_sock.listen(5)
   print("server起動")

   while True:
      conn,address=server_sock.accept()
      print(f'connect with {address}')
      header=recv_exact(conn,32)
      roomname_size,operation,state,payload_size=parse_tcrp_header(header)

      body_size=roomname_size+payload_size
      body=recv_exact(conn,body_size)

      roomname=body[:roomname_size].decode("utf-8",errors="replace")
      username=body[roomname_size:].decode("utf-8",errors="replace")

      kind = "UNKNOWN"
      if operation == OP_create:
         kind = "CREATE"
      elif operation == OP_join:
         kind = "JOIN"

      phase = "UNKNOWN"
      if state == ST_request:
         phase = "REQUEST"
      elif state == ST_ack:
         phase = "ACK"
      elif state == ST_done:
         phase = "DONE"

      print(f'operation={kind}({operation}),state={phase}({state})')
      print(f'roomname_size={roomname_size},payload_size={payload_size}')
      print("roomname:", roomname)
      print("username:", username)

      token=generate_token(16)
      if operation==OP_create and state==ST_request:
         if roomname in rooms:
            print("すでにこのルーム名は存在します")
            conn.close()
            return
         rooms[roomname]=set()
      elif operation==OP_join and state==ST_request:
         if not roomname in rooms:
            print("そのルームは存在しません")
            conn.close()
            continue
      rooms[roomname].add(token)
      print("generated token:", token)
      token_bytes=token.encode("utf-8")
      ack_header=build_tcrp_header(0,operation,ST_ack,len(token_bytes))
      print(f'ack_header: {operation}, {state}')
      packet=ack_header+token_bytes
      conn.sendall(packet)
      
      conn.close()

if __name__ == "__main__":
   main()
