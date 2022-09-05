import pygame
import random
from pygame.math import Vector2

# Extensions:
#   { Score; Background; Food; Snake; Music }


block = 30
block_num = 20
fnt = pygame.font.init()


class Snake:
    def __init__(self, direction, screen):
        self.direction = direction
        self.screen = screen
        self.body = [Vector2(9, 10), Vector2(8, 10), Vector2(7, 10),
                     Vector2(6, 10), Vector2(5, 10)]
        self.newBlock = False
        self.image = pygame.image.load("einstein.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 270, 0.07)

    def render(self):
        headX = int(self.body[0].x * block)
        headY = int(self.body[0].y * block)
        headRect = pygame.Rect(headX, headY, block, block)
        self.screen.blit(self.image, headRect)

        for blk in self.body[1:]:
            blockRect = pygame.Rect(int(blk.x * block), int(blk.y * block), block, block)
            pygame.draw.rect(self.screen, (128, 128, 128), blockRect)

    def update(self):
        if self.newBlock:
            body = self.body
        else:
            body = self.body[:-1]

        if self.direction == 0:
            body.insert(0, body[0] - Vector2(0, 1))

        elif self.direction == 90:
            body.insert(0, body[0] - Vector2(1, 0))

        elif self.direction == 180:
            body.insert(0, body[0] + Vector2(0, 1))

        elif self.direction == 270:
            body.insert(0, body[0] + Vector2(1, 0))

        self.body = body

        self.newBlock = False


class Food:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.pos = pygame.math.Vector2(self.x, self.y)

        self.image = pygame.image.load("pi.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.05)

    def render(self):
        foodRect = pygame.Rect(int(self.pos.x * block), int(self.pos.y * block), block, block)
        self.screen.blit(self.image, foodRect)


class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.timer = None
        self.screen = None
        self.snake = None
        self.food = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((block * block_num, block * block_num))
        pygame.display.set_caption("Einsnake")

        self.clock = pygame.time.Clock()
        self.running = True
        self.timer = pygame.USEREVENT
        pygame.time.set_timer(self.timer, 110)

        x = random.randint(0, block_num - 1)
        y = random.randint(0, block_num - 1)
        self.food = Food(x, y, self.screen)

        self.snake = Snake(270, self.screen)

        pygame.mixer.init()
        pygame.mixer.music.load("backSound.wav")
        pygame.mixer.music.play(-1)

    def update(self):
        self.events()

        if self.food.pos == self.snake.body[0]:
            self.snake.newBlock = True
            x = random.randint(0, block_num - 1)
            y = random.randint(0, block_num - 1)
            self.food.pos = Vector2(x, y)

        if self.snake.body[0].x < 0 or self.snake.body[0].x >= block_num or \
                self.snake.body[0].y < 0 or self.snake.body[0].y >= block_num:
            self.running = False

        for part in self.snake.body[1:]:
            if part == self.snake.body[0]:
                self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == self.timer:
                self.snake.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # UP
            if self.snake.direction == 90:
                self.snake.direction = 0
                self.snake.image = pygame.transform.rotate(self.snake.image, -90)
            elif self.snake.direction == 270:
                self.snake.direction = 0
                self.snake.image = pygame.transform.rotate(self.snake.image, 90)

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:  # LEFT
            if self.snake.direction == 0:
                self.snake.direction = 90
                self.snake.image = pygame.transform.rotate(self.snake.image, 90)
            elif self.snake.direction == 180:
                self.snake.direction = 90
                self.snake.image = pygame.transform.rotate(self.snake.image, -90)

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # RIGHT
            if self.snake.direction == 0:
                self.snake.direction = 270
                self.snake.image = pygame.transform.rotate(self.snake.image, -90)
            elif self.snake.direction == 180:
                self.snake.direction = 270
                self.snake.image = pygame.transform.rotate(self.snake.image, 90)

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # DOWN
            if self.snake.direction == 90:
                self.snake.direction = 180
                self.snake.image = pygame.transform.rotate(self.snake.image, 90)
            elif self.snake.direction == 270:
                self.snake.direction = 180
                self.snake.image = pygame.transform.rotate(self.snake.image, -90)

    def render(self):
        self.screen.fill((0, 0, 0))

        background = pygame.image.load("bckground.png")
        self.screen.blit(background, (0, 0))

        self.food.render()
        self.snake.render()

        game_font = pygame.font.Font('Freshman.ttf', 20)
        score_font = game_font.render("Score: " + str(len(self.snake.body) - 5), True, (255, 255, 0))
        self.screen.blit(score_font, [0, 0])

        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
