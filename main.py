import random
import pygame
import pickle

pygame.init()

def loadBest():
    try:
        file_name = "bestScore.db"
        with open(file_name, "rb") as file:
            best_score = pickle.load(file)
            return best_score
    except:
        return 0

def saveBest(best):
    try:
        file_name = "bestScore.db"
        with open(file_name, "wb") as file:
            pickle.dump(best, file)
    except Exception as e:
        print("Save failed")

class HUD:
    color = (255, 255, 0)
    size = (500, 100)

    def __init__(self):
        self.texture = pygame.Surface(self.size)
        self.texture.fill(self.color)

        self.position = (0, 500)

    def blit(self, screen, score, best):
        black = (0, 0, 0)
        screen.blit(self.texture, self.position)
        small_font = pygame.font.Font("freesansbold.ttf", 14)
        big_font = pygame.font.Font("freesansbold.ttf", 30)

        #Score
        score_text = big_font.render("Score: {}".format(score), True, black)
        screen.blit(score_text, (10, 560))

        #Best
        best_text = big_font.render("Best: {}".format(best), True, black)
        rect = best_text.get_rect().width
        screen.blit(best_text, (490 - rect, 560))

        #Play/Pause
        p_key = small_font.render("Press \"P\" to pause/resume the game", True, black)
        screen.blit(p_key, (10, 510))
        if paused:
            play_pause = small_font.render(" PAUSED ", True, black, (255, 0, 0))
        else:
            play_pause = small_font.render(" RESUMED ", True, black, (0, 255, 0))
        screen.blit(play_pause, (370, 510))

        #Edges
        e_key = small_font.render("Press \"E\" to turn on/off collision with window edge", True, black)
        screen.blit(e_key, (10, 530))
        if edges:
            edge_on_off = small_font.render(" ON ", True, black, (0, 255, 0))
        else:
            edge_on_off = small_font.render(" OFF ", True, black, (255, 0, 0))
        screen.blit(edge_on_off, (370, 530))

class Snake:
    color = (255, 255, 255)
    size = (10, 10)
    velocity = 10

    def __init__(self, best):
        self.texture = pygame.Surface(self.size)
        self.texture.fill(self.color)

        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "r"

        self.score = 0
        self.best = best

    def blit(self, screen):
        for position in self.body:
            screen.blit(self.texture, position)

    def move(self):
        new_head = tuple()
        if self.direction == "r":
            new_head = (self.body[0][0] + 10, self.body[0][1])
        elif self.direction == "l":
            new_head = (self.body[0][0] - 10, self.body[0][1])
        elif self.direction == "u":
            new_head = (self.body[0][0], self.body[0][1] - 10)
        elif self.direction == "d":
            new_head = (self.body[0][0], self.body[0][1] + 10)
        x = new_head[0]
        y = new_head[1]
        if x > 490 and not edges:
            x = 0
        elif x < 0 and not edges:
            x = 490
        elif y > 490 and not edges:
            y = 0
        elif y < 0 and not edges:
            y = 490
        new_head = (x, y)
        self.body.pop(-1)
        self.body.insert(0, new_head)

    def change_direction(self, direction: str):
        if direction == "r":
            if self.direction != "l":
                self.direction = direction
        elif direction == "l":
            if self.direction != "r":
                self.direction = direction
        elif direction == "u":
            if self.direction != "d":
                self.direction = direction
        elif direction == "d":
            if self.direction != "u":
                self.direction = direction

    def eat(self):
        if self.body[0] == fruit.position:
            new_slice = (self.body[-1][0], self.body[-1][1])
            self.body.append(new_slice)
            self.score += 1
            if self.score > self.best:
                self.best = self.score
            return True

    def colision(self, head):
        if head in self.body[1:]:
            saveBest(snake.best)
            return True
        if edges:
            if head[0] > 490 or head[0] < 0 or head[1] > 490 or head[1] < 0:
                saveBest(snake.best)
                return True

class Fruit:
    color = (240, 0, 0)
    size = (10, 10)

    def __init__(self, snake):
        self.texture = pygame.Surface(self.size)
        self.texture.fill(self.color)

        self.position = Fruit.spawn(snake)

    def blit(self, screen):
        screen.blit(self.texture, self.position)

    @staticmethod
    def spawn(snake):
        conflict = True
        while conflict:
            position = (random.randint(1, 49) * 10, random.randint(1, 49) * 10)
            if position not in snake.body:
                conflict = False
        return position

if __name__ == '__main__':

    screen = pygame.display.set_mode((500, 600))  # game 500x500px, HUD 500x100px
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()

    best = loadBest()

    snake = Snake(best)
    fruit = Fruit(snake)
    hud = HUD()
    paused = False
    edges = False

    while True:
        clock.tick(18)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not paused:
                    snake.change_direction("u")
                    break
                elif event.key == pygame.K_DOWN and not paused:
                    snake.change_direction("d")
                    break
                elif event.key == pygame.K_RIGHT and not paused:
                    snake.change_direction("r")
                    break
                elif event.key == pygame.K_LEFT and not paused:
                    snake.change_direction("l")
                    break
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_e:
                    if snake.score == 0:
                        edges = not edges

        if not paused:
            screen.fill((0, 0, 0))
            fruit.blit(screen)
            snake.blit(screen)
            if snake.eat():
                fruit = Fruit(snake)
            if snake.colision(snake.body[0]):
                best = loadBest()
                snake = Snake(best)
            snake.move()
        hud.blit(screen, snake.score, snake.best)
        pygame.display.update()