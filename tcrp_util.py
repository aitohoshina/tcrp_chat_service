import socket
import random
import string

def recv_exact(conn: socket.socket, n: int) ->bytes:
   buf=b""
   while len(buf)<n:
      chunk=conn.recv(n-len(buf))
      if chunk==b"":
         raise ConnectionError ("connection closed")
      buf+=chunk
   return buf
def generate_token(n:int=16)->str:
   char =string.ascii_letters+string.digits
   token=""
   for _ in range(n):
      token+=random.choice(char)
   return token
if __name__=="__main__":
   print(generate_token())
   print(generate_token())
