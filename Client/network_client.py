import socket, threading, json

class NetworkClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.buffer = ""#chuoi rong de gui du lieu server
        self.callback = None

    def wait_for_init(self):
        """Chờ server gửi INIT ban đầu"""
        while True:
            self.buffer += self.client.recv(1024).decode() #nhan du lieu
            lines = self.buffer.split("\n")#cat tung dong
            for line in lines:
                if line.startswith("INIT:"):#co 2 loai chi lay init (dung de cap nhat vi tri)
                    return json.loads(line[5:])#bo chu init

    def start_receiving(self, callback):
        """Bắt đầu thread nhận dữ liệu STATE"""
        self.callback = callback
        threading.Thread(target=self.receive_loop, daemon=True).start()#tao mot luong de nhan trang va se tu dong khi ket thuc

    def receive_loop(self):
        while True:
            try:
                chunk = self.client.recv(4096).decode()#du lieu nhan
                if not chunk:
                    raise Exception("Mất kết nối tới server")
                self.buffer += chunk

                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)
                    if line.startswith("STATE:") and self.callback:
                        try:
                            state = json.loads(line[6:])
                            self.callback(state)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                print("[LỖI]", e)
                break

    def send_input(self, inputs):
        try:
            self.client.sendall(json.dumps(inputs).encode()) #gui du lieu tu ban phim cho sever
        except:
            pass

    def close(self):
        self.client.close()