OP_create=1
OP_join=2

ST_request=0
ST_ack=1
ST_done=2

def build_tcrp_header(roomname_size:int,
                      operation:int,
                      state:int,
                      payload_size:int) -> bytes:
   byte0=roomname_size.to_bytes(1,"big")
   byte1=operation.to_bytes(1,"big")
   byte2=state.to_bytes(1,"big")
   byte3_31=payload_size.to_bytes(29,"big")
   return byte0+byte1+byte2+byte3_31

def parse_tcrp_header(header:bytes) -> int:
   roomname_size=header[0]
   operation=header[1]
   state=header[2]
   payload_size=int.from_bytes(header[3:],"big")
   return roomname_size,operation,state,payload_size




