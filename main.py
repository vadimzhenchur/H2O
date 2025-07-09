import random

import pygame

WIDTH = 600
HEIGHT = 600

pygame.init()
pygame.display.set_caption("Напис у Pygame")
font = pygame.font.SysFont(None, 48)
text = font.render("Привіт, Pygame!", True, "green")


class Player:
    def __init__(self, x, y, size, color, speed, name):
        self.hitbox = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed
        self.name = name
        self.x = x
        self.y = y
        self.size = size

        def draw(self, scale):
            draw_x = int(WIDTH // 2 - (self.size *))
            draw_y = int((self.y - player_y) * scale + HEIGHT // 2)
            self.hitbox = pygame.Rect(draw_x, draw_y, self.size + scale, self.size + scale)
            pygame.draw.rect(window, self.color, self.hitbox)


    def draw(self, window):
        pygame.draw.rect(window, self.color, self.hitbox)



    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            pass
            


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
        self.hitbox = pygame.Rect(draw_x, draw_y, self.size + scale, self.size + scale)
        pygame.draw.rect(window, self.color, self.hitbox)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.hitbox)





pygame.init()


window = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

andriy = Player(WIDTH//2, HEIGHT//3, 50, [255, 0, 0], 3, "lubomyr")

foods = []
for i in range(300):
    food = Food(25,
                random.randint(-2000, 2000),
                random.randint(-2000, 2000),
                [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) ])
    foods.append(food)
    scale = 1

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

    window.fill([123, 123, 123])
    andriy.update()
    andriy.draw(window, scale)

    for food in foods:
        food.draw(window, andriy.x, andriy.y)
    pygame.display.flip()
    clock.tick(60)