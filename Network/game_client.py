import socket, threading, json, pygame, sys
from Network.configsever import *
from core.map import renderMap
from core.camera import camerase

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

buffer = ""
init_data = None
while True:
    buffer += client.recv(1024).decode() #goi tin nhan duoc INIT:{"player_id": 0, "x": 100, "y": 100, "color": [255, 0, 0]}\n
    lines = buffer.split("\n")
    for line in lines:
        if line.startswith("INIT:"):
            init_data = json.loads(line[5:]) # giai ma goi tin
            break
    if init_data:
        break

player_id = init_data["player_id"]
color = init_data["color"]
x, y = init_data["x"], init_data["y"]

print(f"[CLIENT] Bạn là người chơi {player_id}, màu {color}")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Pico Park - Player {player_id}")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

try:
    tile_map = renderMap("TileSet_Map/Mario_Test_Map_Cao15.tmx")
except Exception as e:
    print("[LỖI] Không thể load bản đồ:", e)
    pygame.quit()
    sys.exit()

camera = camerase(tile_map.tmx_data.width * tile_map.tmx_data.tilewidth,
                  tile_map.tmx_data.height * tile_map.tmx_data.tileheight)

players_data = {}

def receive_data():
    global players_data
    buffer = ""
    while True:
        try:
            chunk = client.recv(4096).decode()
            if not chunk:
                raise Exception("Mất kết nối: server đóng kết nối")
            buffer += chunk

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.startswith("STATE:"):
                    try:
                        players_data = json.loads(line[6:])
                        print("📥 Nhận state:", players_data)
                    except json.JSONDecodeError as e:
                        print("[LỖI] JSON lỗi:", e, "| raw:", line)
                        continue  # Bỏ qua JSON lỗi, tiếp tục vòng
        except Exception as e:
            print("[LỖI] Mất kết nối tới server:", e)
            pygame.quit()
            sys.exit()

threading.Thread(target=receive_data, daemon=True).start()

def get_input():
    keys = pygame.key.get_pressed()
    inputs = []
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        inputs.append("LEFT")
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        inputs.append("RIGHT")
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        inputs.append("UP")
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        inputs.append("DOWN")
    return inputs

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.close()
            pygame.quit()
            sys.exit()

    inputs = get_input()
    if inputs:
        client.sendall(json.dumps(inputs).encode())

    screen.fill((0, 0, 0))

    if players_data:
        if str(player_id) in players_data:
            my_data = players_data[str(player_id)]
            my_rect = pygame.Rect(my_data["x"], my_data["y"], PLAYER_SIZE, PLAYER_SIZE)
            camera.update([type("Obj", (), {"rect": my_rect})()],
                          tile_map.tmx_data.width * tile_map.tmx_data.tilewidth,
                          tile_map.tmx_data.height * tile_map.tmx_data.tileheight,
                          SCREEN_WIDTH, SCREEN_HEIGHT)

        tile_map.draw(screen, camera)

        for pid, pdata in players_data.items():
            rect = pygame.Rect(pdata["x"], pdata["y"], PLAYER_SIZE, PLAYER_SIZE)
            pygame.draw.rect(screen, pdata["color"], camera.apply(rect))
            if int(pid) == player_id:
                pygame.draw.rect(screen, (255, 255, 255), camera.apply(rect), 2)
    else:
        msg = font.render("⏳ Đang chờ server gửi dữ liệu...", True, (255, 255, 255))
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)  # Giới hạn 60 FPS

