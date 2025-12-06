起動手順
1. python3 tcrp_server.py   # TCP: ルーム作成 / JOIN / token 発行
2. python3 udp_server.py    # UDP: チャット本体
3. python3 tcrp_client.py    # ルーム作成（CREATE）
4. python3 tcrp_client_join.py  # ルーム参加（JOIN）

🧩 システム概要

TCP (TCRP)

ルーム作成 / JOIN

サーバが token を発行

token を受け取ったら UDP チャットへ移行

UDP

実際のチャットは全部 UDP

roomname + token + message を送信

サーバが token/IP をチェックしてブロードキャスト

📡 TCRP ヘッダ（32バイト）
1 byte  roomname_size
1 byte  operation (1=create, 2=join)
1 byte  state (0=req, 1=ack, 2=done)
29 bytes payload_size


ボディ：

roomname + payload(username)

💬 UDP パケット
[header]
 1 byte roomname_size
 1 byte token_size
[body]
 roomname + token + message

🗄 rooms データ構造（概要）
rooms = {
  roomname: {
    host_token: "...",
    host_ip: "...",
    members: {
      token: { ip, username, udp_addr }
    }
  }
}

✔ 動作イメージ
CREATE -> token受け取り -> UDPチャット開始
JOIN   -> token受け取り -> UDPチャット開始
