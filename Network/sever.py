import socket, threading, json, time
from Network.configsever import HOST, PORT, PLAYER_SIZE, PLAYER_SPEED

clients = {}  
players = {}  #{"x": int, "y": int, "color": [r,g,b]}
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

def handle_client(conn, player_id):
    print(f"[KẾT NỐI] Người chơi {player_id} đã tham gia.")
    init_data = {
        "player_id": player_id,
        "color": colors[player_id % len(colors)],
        "x": 100 + player_id * 100,
        "y": 100
    }
    players[str(player_id)] = {"x": init_data["x"], "y": init_data["y"], "color": init_data["color"]}
    conn.sendall(f"INIT:{json.dumps(init_data)}\n".encode()) #json.dump bien thanh json

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            inputs = json.loads(data)
            if "LEFT" in inputs:
                players[str(player_id)]["x"] -= PLAYER_SPEED
            if "RIGHT" in inputs:
                players[str(player_id)]["x"] += PLAYER_SPEED
            if "UP" in inputs:
                players[str(player_id)]["y"] -= PLAYER_SPEED
            if "DOWN" in inputs:
                players[str(player_id)]["y"] += PLAYER_SPEED
    except:
        pass
    finally:
        print(f"[NGẮT] Người chơi {player_id} đã thoát.")
        conn.close()
        if str(player_id) in players: del players[str(player_id)]
        if player_id in clients: del clients[player_id]

def broadcast_loop():
    while True:
        if clients:
            state = f"STATE:{json.dumps(players)}\n".encode()
            for conn in clients.values():
                try:
                    conn.sendall(state)
                except:
                    pass
        time.sleep(0.02)  # Giới hạn tốc độ gửi (50 lần/giây)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(4)
    print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")

    threading.Thread(target=broadcast_loop, daemon=True).start()

    player_id = 0
    while True:
        conn, _ = server.accept()
        clients[player_id] = conn
        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()
        player_id += 1

if __name__ == "__main__":
    start_server()
