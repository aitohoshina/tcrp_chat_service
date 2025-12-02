import socket

clients=set()

def parse_packet(packet):
   len_username=packet[0]
   username=packet[1:1+len_username].decode("utf-8",errors="replace")
   text=packet[1+len_username:].decode("utf-8",errors="replace")
   return username,text

def main():
   sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   sock.bind(("0.0.0.0",5000))
   print("UDP server 起動")
   while True:
      packet,address=sock.recvfrom(4096)
      clients.add(address)
      username,text=parse_packet(packet)
      print("受信内容：",text, "from", username)
      for addr in clients:
         if addr !=address:
            sock.sendto(packet,addr)

if __name__ == "__main__":
   main()
