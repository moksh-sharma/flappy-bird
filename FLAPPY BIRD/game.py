import pygame as pg
import sys
import time
from random import randint
pg.init()  # Initialize pygame


class Bird(pg.sprite.Sprite):  # Inheriting from Sprite class
    def __init__(self, scale_factor):  # Constructor
        super(Bird, self).__init__()  # Calling parent class constructor
        # Loading bird images and setting initial properties
        self.img_list = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_factor),
                         # List of bird images
                         pg.transform.scale_by(pg.image.load("assets/birddown.png").convert_alpha(), scale_factor)]
        self.image_index = 0  # Index of current bird image
        self.image = self.img_list[self.image_index]  # Current bird image
        self.rect = self.image.get_rect(
            center=(100, 100))  # Rectangle for bird image
        self.y_velocity = 0  # Bird's y-velocity
        self.gravity = 10  # Gravity
        self.flap_speed = 250  # Speed at which bird flaps
        self.anim_counter = 0  # Counter to control bird's animation
        self.update_on = False  # Flag to control bird's update

    def update(self, dt):  # Function to update bird's movement
        if self.update_on:  # Check if bird's update is on
            # Animating bird and applying gravity
            self.playAnimation()  # Play bird's animation
            self.applyGravity(dt)  # Apply gravity to bird's y-coordinate

            if self.rect.y <= 0 and self.flap_speed == 250:  # Check if bird is at top of screen
                self.rect.y = 0  # Set bird's y-coordinate to 0
                self.flap_speed = 0  # Set flap speed to 0
                self.y_velocity = 0  # Set bird's y-velocity to 0
            elif self.rect.y > 0 and self.flap_speed == 0:  # Check if bird is below top of screen
                self.flap_speed = 250  # Set flap speed to 250

    def applyGravity(self, dt):  # Function to apply gravity to bird's y-coordinate
        # Applying gravity to the bird's y-coordinate
        self.y_velocity += self.gravity*dt  # Add gravity to bird's y-velocity
        self.rect.y += self.y_velocity  # Add bird's y-velocity to y-coordinate

    def flap(self, dt):  # Function to flap bird
        # Function to simulate bird flapping
        self.y_velocity = -self.flap_speed*dt  # Set bird's y-velocity to flap speed

    def playAnimation(self):  # Function to play bird's animation
        # Function to switch bird's image for animation
        if self.anim_counter == 5:  # Check if animation counter is 5
            # Set bird's image to current image
            self.image = self.img_list[self.image_index]
            if self.image_index == 0:  # Check if current image is first image
                self.image_index = 1  # Set image index to 1
            else:  # Check if current image is second image
                self.image_index = 0  # Set image index to 0
            self.anim_counter = 0  # Reset animation counter

        self.anim_counter += 1  # Increment animation counter


class Pipe:  # Class for pipes
    def __init__(self, scale_factor, move_speed):  # Constructor
        # Initializing properties of pipes
        self.img_up = pg.transform.scale_by(pg.image.load(
            "assets/pipeup.png").convert_alpha(), scale_factor)  # Pipe image
        self.img_down = pg.transform.scale_by(pg.image.load(
            "assets/pipedown.png").convert_alpha(), scale_factor)  # Pipe image
        self.rect_up = self.img_up.get_rect()  # Rectangle for pipe image
        self.rect_down = self.img_down.get_rect()  # Rectangle for pipe image
        self.pipe_distance = 200  # Distance between pipes
        self.rect_up.y = randint(250, 520)  # Random y-coordinate for top pipe
        self.rect_up.x = 600  # x-coordinate for top pipe
        self.rect_down.y = self.rect_up.y-self.pipe_distance - \
            self.rect_up.height  # y-coordinate for bottom pipe
        self.rect_down.x = 600  # x-coordinate for bottom pipe
        self.move_speed = move_speed  # Speed at which pipes move

    def drawPipe(self, win):  # Function to draw pipes on the window
        # Function to draw pipes on the window
        win.blit(self.img_up, self.rect_up)  # Draw top pipe
        win.blit(self.img_down, self.rect_down)  # Draw bottom pipe

    def update(self, dt):  # Function to update pipe positions
        # Function to update pipe positions
        self.rect_up.x -= int(self.move_speed*dt)  # Move top pipe
        self.rect_down.x -= int(self.move_speed*dt)  # Move bottom pipe


class Game:  # Class for game
    def __init__(self):  # Constructor
        # Setting up the game window and initial configurations
        self.width = 600  # Width of the window
        self.height = 768  # Height of the window
        self.scale_factor = 1.5  # Scale factor for images
        self.win = pg.display.set_mode(
            (self.width, self.height))  # Setting up the window
        self.clock = pg.time.Clock()  # Clock to control FPS
        self.move_speed = 250  # Speed at which pipes move
        self.bird = Bird(self.scale_factor)  # Creating bird object

        self.is_enter_pressed = False  # Flag to check if enter key is pressed
        self.pipes = []  # List to store pipes
        self.pipe_generate_counter = 71  # Counter to control pipe generation
        self.setUpBgAndGround()  # Setting up background and ground

        self.gameLoop()  # Starting the game loop

    def gameLoop(self):  # Function to run the game loop
        last_time = time.time()  # Variable to store last time
        while True:  # Game loop
            # Calculating delta time for smoother movement
            new_time = time.time()  # Variable to store current time
            dt = new_time-last_time  # Delta time
            last_time = new_time  # Updating last time

            for event in pg.event.get():  # Event loop
                if event.type == pg.QUIT:  # Check if user quits
                    pg.quit()  # Quit pygame
                    sys.exit()  # Exit the program
                if event.type == pg.KEYDOWN:  # Check if user presses a key
                    if event.key == pg.K_RETURN:  # Check if user presses enter key
                        self.is_enter_pressed = True  # Set enter pressed flag to True
                        self.bird.update_on = True  # Set bird's update flag to True
                    if event.key == pg.K_SPACE and self.is_enter_pressed:  # Check if user presses space key
                        self.bird.flap(dt)  # Flap the bird

            self.updateEverything(dt)  # Update everything
            self.checkCollisions()  # Check for collisions
            self.drawEverything()  # Draw everything on the window
            pg.display.update()  # Update the window
            self.clock.tick(60)  # Set FPS to 60

    def checkCollisions(self):  # Function to check for collisions
        # Check for collisions with pipes and ground
        if len(self.pipes):  # Check if there are any pipes
            if self.bird.rect.bottom > 568:  # Check if bird collides with ground
                self.bird.update_on = False  # Set bird's update flag to False
                self.is_enter_pressed = False  # Set enter pressed flag to False
                # Print message
                print("\nBird collided with the ground! Exiting...\n")
                # Add a delay before exiting (2 seconds in this case)
                # Add a delay before exiting (2 seconds in this case)
                time.sleep(2)
                sys.exit()  # Exit the program
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                    # Check if bird collides with a pipe
                    self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed = False  # Set enter pressed flag to False
                # Print message
                print("\nBird collided with a pipe! Exiting...\n")
                # Add a delay before exiting (2 seconds in this case)
                # Add a delay before exiting (2 seconds in this case)
                time.sleep(2)
                sys.exit()  # Exit the program

    def updateEverything(self, dt):  # Function to update everything
        if self.is_enter_pressed:  # Check if enter key is pressed
            # Moving the ground
            self.ground1_rect.x -= int(self.move_speed*dt)  # Move ground 1
            self.ground2_rect.x -= int(self.move_speed*dt)  # Move ground 2

            # Resetting ground position when out of screen
            if self.ground1_rect.right < 0:  # Check if ground 1 is out of screen
                self.ground1_rect.x = self.ground2_rect.right  # Reset ground 1 position
            if self.ground2_rect.right < 0:  # Check if ground 2 is out of screen
                self.ground2_rect.x = self.ground1_rect.right  # Reset ground 2 position

            # Generating pipes and moving them
            if self.pipe_generate_counter > 70:  # Check if pipe generation counter is greater than 70
                # Add a new pipe to the list
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0  # Reset pipe generation counter

            self.pipe_generate_counter += 1  # Increment pipe generation counter

            for pipe in self.pipes:  # Loop through pipes
                pipe.update(dt)  # Update pipe position

            # Removing pipes out of screen
            if len(self.pipes) != 0:  # Check if there are any pipes
                # Check if first pipe is out of screen
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)  # Remove first pipe from the list

            # Updating bird's movement
            self.bird.update(dt)  # Update bird's movement

    def drawEverything(self):  # Function to draw everything on the window
        # Drawing background, pipes, ground, and bird on the window
        self.win.blit(self.bg_img, (0, -300))  # Draw background
        for pipe in self.pipes:  # Loop through pipes
            pipe.drawPipe(self.win)  # Draw pipe
        self.win.blit(self.ground1_img, self.ground1_rect)  # Draw ground 1
        self.win.blit(self.ground2_img, self.ground2_rect)  # Draw ground 2
        self.win.blit(self.bird.image, self.bird.rect)  # Draw bird

    def setUpBgAndGround(self):  # Function to set up background and ground
        # Loading images for background and ground
        self.bg_img = pg.transform.scale_by(pg.image.load(
            "assets/bg.png").convert(), self.scale_factor)  # Background image
        self.ground1_img = pg.transform.scale_by(pg.image.load(
            "assets/ground.png").convert(), self.scale_factor)  # Ground image
        self.ground2_img = pg.transform.scale_by(pg.image.load(
            "assets/ground.png").convert(), self.scale_factor)  # Ground image

        # Setting up ground rectangles for movement
        self.ground1_rect = self.ground1_img.get_rect()  # Rectangle for ground image
        self.ground2_rect = self.ground2_img.get_rect()  # Rectangle for ground image

        self.ground1_rect.x = 0  # x-coordinate for ground 1
        self.ground2_rect.x = self.ground1_rect.right  # x-coordinate for ground 2
        self.ground1_rect.y = 568  # y-coordinate for ground 1
        self.ground2_rect.y = 568  # y-coordinate for ground 2


# Initialize the game
game = Game()  # Creating game object
