import pygame
import random
import sys


class Snake:
    def __init__(self):
        self.length = 1
        self.direction = (0, 0)
        self.body = [[dis_width / 2, dis_height / 2]]
        self.color = white
        self.score = 0

    def get_head(self):
        return self.body[-1]

    def turn(self, point):
        # Forbid the snake of going in on itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self, dis):
        # Set motion to the snake
        x = self.get_head()[0]
        y = self.get_head()[1]
        x += self.direction[0] * gridsize
        y += self.direction[1] * gridsize

        # Move on other side at the boundaries
        if x > (dis_width - gridsize):
            x = 0
        if y > (dis_height - gridsize):
            y = 0
        if x < 0:
            x = dis_width - gridsize
        if y < 0:
            y = dis_height - gridsize

        # Update the snakes body with the new position
        self.body.append([x, y])

        # "Cut" the snake's tail if it's too long
        if len(self.body) > self.length:
            del self.body[0]

        # Snake can't eat itself
        for x in self.body[:-1]:
            if x == self.get_head():
                self.handle_death(dis)

        # Display score as part of the move method because
        # it updates the screen and I didn't want it to be a stand-alone method
        score_font = pygame.font.SysFont("comicsansms", 35)
        value = score_font.render("Your Score: " + str(self.score), True, yellow)
        dis.blit(value, [0, 0])

    def handle_death(self, dis):
        score_font = pygame.font.SysFont("comicsansms", 35)
        score_text = score_font.render("Your Score: " + str(self.score), True, yellow)
        font_style = pygame.font.SysFont("bahnschrift", 25)
        end_text = font_style.render(
            "You Lost! Press Q-Quit or C-Play Again", True, red
        )
        while True:
            dis.fill(black)
            dis.blit(end_text, [dis_width / 4.5, dis_height / 3])
            dis.blit(score_text, [dis_width / 2.8, dis_height / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        main()

    def draw_snake(self, dis):
        for x in self.body:
            pygame.draw.rect(dis, self.color, [x[0], x[1], gridsize, gridsize])

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


class Food:
    def __init__(self):
        self.position = [0, 0]
        self.color = blue
        self.randomize_position()

    def randomize_position(self):
        self.position = [
            random.randrange(0, dis_width - gridsize, gridsize),
            random.randrange(0, dis_height - gridsize, gridsize),
        ]

    def draw_food(self, dis):
        pygame.draw.rect(
            dis, blue, [self.position[0], self.position[1], gridsize, gridsize]
        )


## DEFINE GLOBAL VARIABLES ##
gridsize = 15

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)

dis_width = 810
dis_height = 600

snake_speed = 10

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def main():
    pygame.init()

    # Create a display and name it
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption("Snake game by Dimitar")

    # Introduce a clock, used to keep the snake at a certain speed
    clock = pygame.time.Clock()

    # Initialize our snake and food classes
    snake = Snake()
    food = Food()

    # Main game loop
    while True:
        # Establish snake speed
        clock.tick(snake_speed)

        # Update background
        dis.fill(black)
        snake.handle_keys()
        snake.move(dis)

        # Grow snake if it has eaten and put out a new piece of food
        if food.position == snake.get_head():
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        snake.draw_snake(dis)
        food.draw_food(dis)
        pygame.display.update()


main()
