import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong Game")

# Цвета
black = (11, 22, 33)
white = (255, 255, 255)

# Частота обновления экрана
clock = pygame.time.Clock()
fps = 60

# Класс для платформы
class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 7

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

# Класс для мяча
class Ball:
    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.radius = radius
        self.dx = random.choice([-7, 7])
        self.dy = random.choice([-7, 7])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.ellipse(screen, white, self.rect)

    def bounce(self, axis):
        if axis == "x":
            self.dx = -self.dx
        elif axis == "y":
            self.dy = -self.dy

# Создание объектов
paddle1 = Paddle(30, screen_height // 2 - 60, 20, 120)
paddle2 = Paddle(screen_width - 50, screen_height // 2 - 60, 20, 120)
ball = Ball(screen_width // 2, screen_height // 2, 15)

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.rect.top > 0:
        paddle1.move(up=True)
    if keys[pygame.K_s] and paddle1.rect.bottom < screen_height:
        paddle1.move(up=False)
    if keys[pygame.K_UP] and paddle2.rect.top > 0:
        paddle2.move(up=True)
    if keys[pygame.K_DOWN] and paddle2.rect.bottom < screen_height:
        paddle2.move(up=False)

    # Движение мяча
    ball.move()

    # Отскок мяча от верхнего и нижнего края
    if ball.rect.top <= 0 or ball.rect.bottom >= screen_height:
        ball.bounce(axis="y")

    # Отскок мяча от платформ
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.bounce(axis="x")

    # Проверка на выход мяча за пределы экрана
    if ball.rect.left <= 0 or ball.rect.right >= screen_width:
        ball = Ball(screen_width // 2, screen_height // 2, 15)  # Перезапуск мяча в центре

    # Отрисовка объектов
    screen.fill(black)
    paddle1.draw()
    paddle2.draw()
    ball.draw()
    pygame.display.flip()

    # Обновление экрана
    clock.tick(fps)

pygame.quit()
