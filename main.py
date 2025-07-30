import json
import random
import socket
import threading
import time

import pygame

WIDTH = 1000
HEIGHT = 600

def start_game(name, address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, int(port)))

    player_id = client.recv(1024).decode()
    other_players_data = {}

    def receive_data():
        global other_players_data
        while True:
            try:
                data = client.recv(4096).decode()
                if data:
                    other_players_data = json.loads(data)
            except:
                break
    threading.Thread(target=receive_data, daemon=True).start()
    class Player:
        def __init__(self, x, y, size, color, speed, name):
            self.hitbox = pygame.Rect(x, y, size, size)
            self.color = color
            self.speed = speed
            self.name = name
            self.x = x
            self.y = y
            self.size = size

        def draw(self, window, scale):
            draw_x = int(WIDTH // 2 - (self.size * scale) // 2)
            draw_y = int(HEIGHT // 2 - (self.size * scale) // 2)
            self.hitbox = pygame.Rect(draw_x, draw_y, self.size * scale, self.size * scale)
            pygame.draw.rect(window, self.color, self.hitbox)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_UP]:
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.y += self.speed



    class Food:
        def __init__(self, size, x, y, color):
            self.hitbox = pygame.Rect(x, y, size, size)
            self.color = color
            self.x = x
            self.y = y
            self.size = size

        def draw(self, window, player_x, player_y, scale):
            draw_x = int((self.x - player_x) * scale + WIDTH // 2)
            draw_y = int((self.y - player_y) * scale + HEIGHT // 2)
            self.hitbox = pygame.Rect(draw_x, draw_y, self.size * scale, self.size * scale)
            pygame.draw.rect(window, self.color, self.hitbox)



    pygame.init()

    window = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    andriy = Player(WIDTH // 2, HEIGHT // 2, 50, [255, 123, 123], 3, name)

    foods = []

    for i in range(300):
        food = Food(20,
                    random.randint(-2000, 2000),
                    random.randint(-2000, 2000),
                    [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        foods.append(food)
    scale = 1
    last_send_time = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        scale = max(0.3, min(60 / andriy.size, 1.5))

        for food in foods:
            if andriy.hitbox.colliderect(food.hitbox):
                food.x = random.randint(-2000, 2000)
                food.y = random.randint(-2000, 2000)
                andriy.size += 2

        window.fill([200, 200, 200])
        andriy.update()
        andriy.draw(window, scale)

        if time.time() - last_send_time > 0.1:
            try:
                player_data = json.dumps({
                    "x": andriy.x,
                    "y": andriy.y,
                    "size": andriy.size,
                    "color": andriy.color,
                    "name": andriy.name
                })
                last_send_time = time.time()
                client.send((player_data + "\n").encode())

            except Exception as e:
                print("Connection lost:", e)
                running = False
        tops = [{'name':andriy.name, 'size': andriy.size}]
        for pid, pdata in other_players_data.items():
            if pdata["name"] != andriy.name:
                draw_x = int((pdata["x"] - andriy.x) * scale + WIDTH // 2)
                draw_y = int((pdata["y"] - andriy.y) * scale + HEIGHT // 2)
                size = pdata["size"] * scale
                pygame.draw.rect(window, pdata["color"], pygame.Rect(draw_x, draw_y, size, size))
                print(pdata)
                print(pdata['name'])
                tops.append({'name': pdata["name"], 'size': pdata["size"]})

        y= 0
        for player in tops:
            player_text= pygame.font.Font(None, 20)\
                .render(f"{player['name']}: {player['size']}", True, [0, 0,0])
            window.blit(player_text,(0, y))
            y += 20
        for pid, pdata in other_players_data.items():
            if pdata["name"] == andriy.name and pdata.get("die"):
                exit()
        for food in foods:
            food.draw(window, andriy.x, andriy.y, scale)
        pygame.display.flip()
        clock.tick(60)
