import pygame as pg
import sys
import time
from random import randint
pg.init()


class Bird(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super(Bird, self).__init__()
        # Loading bird images and setting initial properties
        self.img_list = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_factor),
                         pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(), scale_factor)]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 100))
        self.y_velocity = 0
        self.gravity = 10
        self.flap_speed = 250
        self.anim_counter = 0
        self.update_on = False  # Flag to control bird's update

    def update(self, dt):
        if self.update_on:
            # Animating bird and applying gravity
            self.playAnimation()
            self.applyGravity(dt)

            if self.rect.y <= 0 and self.flap_speed == 250:
                self.rect.y = 0
                self.flap_speed = 0
                self.y_velocity = 0
            elif self.rect.y > 0 and self.flap_speed == 0:
                self.flap_speed = 250

    def applyGravity(self, dt):
        # Applying gravity to the bird's y-coordinate
        self.y_velocity += self.gravity*dt
        self.rect.y += self.y_velocity

    def flap(self, dt):
        # Function to simulate bird flapping
        self.y_velocity = -self.flap_speed*dt

    def playAnimation(self):
        # Function to switch bird's image for animation
        if self.anim_counter == 5:
            self.image = self.img_list[self.image_index]
            if self.image_index == 0:
                self.image_index = 1
            else:
                self.image_index = 0
            self.anim_counter = 0

        self.anim_counter += 1


class Pipe:
    def __init__(self, scale_factor, move_speed):
        # Initializing properties of pipes
        self.img_up = pg.transform.scale_by(pg.image.load(
            "assets/pipeup.png").convert_alpha(), scale_factor)
        self.img_down = pg.transform.scale_by(pg.image.load(
            "assets/pipedown.png").convert_alpha(), scale_factor)
        self.rect_up = self.img_up.get_rect()
        self.rect_down = self.img_down.get_rect()
        self.pipe_distance = 200
        self.rect_up.y = randint(250, 520)
        self.rect_up.x = 600
        self.rect_down.y = self.rect_up.y-self.pipe_distance-self.rect_up.height
        self.rect_down.x = 600
        self.move_speed = move_speed

    def drawPipe(self, win):
        # Function to draw pipes on the window
        win.blit(self.img_up, self.rect_up)
        win.blit(self.img_down, self.rect_down)

    def update(self, dt):
        # Function to update pipe positions
        self.rect_up.x -= int(self.move_speed*dt)
        self.rect_down.x -= int(self.move_speed*dt)


class Game:
    def __init__(self):
        # Setting up the game window and initial configurations
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.bird = Bird(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            # Calculating delta time for smoother movement
            new_time = time.time()
            dt = new_time-last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        # Check for collisions with pipes and ground
        if len(self.pipes):
            if self.bird.rect.bottom > 568:
                self.bird.update_on = False
                self.is_enter_pressed = False
                print("\nBird collided with the ground! Exiting...\n")
                # Add a delay before exiting (2 seconds in this case)
                time.sleep(2)
                sys.exit()
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                    self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed = False
                print("\nBird collided with a pipe! Exiting...\n")
                # Add a delay before exiting (2 seconds in this case)
                time.sleep(2)
                sys.exit()

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # Moving the ground
            self.ground1_rect.x -= int(self.move_speed*dt)
            self.ground2_rect.x -= int(self.move_speed*dt)

            # Resetting ground position when out of screen
            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Generating pipes and moving them
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            for pipe in self.pipes:
                pipe.update(dt)

            # Removing pipes out of screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)

            # Updating bird's movement
            self.bird.update(dt)

    def drawEverything(self):
        # Drawing background, pipes, ground, and bird on the window
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

    def setUpBgAndGround(self):
        # Loading images for background and ground
        self.bg_img = pg.transform.scale_by(pg.image.load(
            "assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load(
            "assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load(
            "assets/ground.png").convert(), self.scale_factor)

        # Setting up ground rectangles
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568


# Initialize the game
game = Game()
