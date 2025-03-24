import socket, threading, json, time
from Server.configsever import HOST, PORT
from Server.sever_player import ServerPlayer
from Collision.collision_map import CollisionMap
clients = {}  # {player_id: conn}
players = {}  # {player_id: ServerPlayer}
colors = [1,2,3]
collision_map = CollisionMap("TileSet_Map/Mario_Test_Map_Cao15.tmx")
def handle_client(conn, player_id):
    print(f"[KẾT NỐI] Người chơi {player_id} đã tham gia.")
    x, y = 100 + player_id * 100, 500
    color = colors[player_id % len(colors)]
    players[str(player_id)] = ServerPlayer(x, y, color,collision_map)

    init_data = {
        "player_id": player_id,
        "color": color,
        "x": x,
        "y": y
    }
    conn.sendall(f"INIT:{json.dumps(init_data)}\n".encode())

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            inputs = json.loads(data)
            players[str(player_id)].handle_input(inputs)
    except:
        pass
    finally:
        print(f"[NGẮT] Người chơi {player_id} đã thoát.")
        conn.close()
        players.pop(str(player_id), None)
        clients.pop(player_id, None)

def broadcast_loop():
    while True:
        if clients:
            for player in players.values():
                player.update()

            state = {
                str(pid): player.get_state()
                for pid, player in players.items()
            }
            state_data = f"STATE:{json.dumps(state)}\n".encode()
            for conn in clients.values():
                try:
                    conn.sendall(state_data)
                except:
                    pass
        time.sleep(0.02)

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