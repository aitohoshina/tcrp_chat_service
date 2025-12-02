import socket
import sys
import threading 

max_packet_size=4096

def parse_packet(packet):
   len_username=packet[0]
   username=packet[1:1+len_username].decode("utf-8",errors="replace")
   text=packet[1+len_username:].decode("utf-8",errors="replace")
   return username,text
def build_packet(username,text):
   username_byte=username.encode("utf-8")
   text_byte=text.encode("utf-8")
   len_username=len(username_byte)
   len_username_byte=b'len_username'
   packet=len_username_byte+username_byte+text_byte
   return packet
def recv_loop(sock: socket.socket):
   while True:
      try:
         packet=sock.recv(max_packet_size)
      except OSError:
         break
      username,text=parse_packet(packet)
      print(f'受信内容：{text} from {username}')
      print(">", end="", flush=True)
def main():
   sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   if len(sys.argv)!=3:
      print(f'例：python3 {sys.argv[0]} <server_ip> <server_port>')
      sys.exit(1)
   server_ip=sys.argv[1]
   username=input("名前を入力してください")
   try:
      server_port=int(sys.argv[2])
   except ValueError:
      print("<server_port>は整数で入力してください")
      sys.exit(1)
   sock.connect((server_ip,server_port))
   t=threading.Thread(target=recv_loop, args=(sock,), daemon=True)
   t.start()
   while True:
      print("メッセージを入力してください")
      text=input(">")
      if not text:
         continue
      if text=="/quit":
         break
      packet=build_packet(username,text)
      sock.send(packet)

if __name__ == "__main__":
   main()
