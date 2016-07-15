import pygame

#------------Setup-------------------------

# Color assignments
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen assignments
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

#pictures
menu_background = pygame.image.load('Title Screen.png')
menu_background = pygame.transform.scale(menu_background,(1200,600))

background = pygame.image.load('Space Bhagyesh.png')
background = pygame.transform.scale(background,(1200,600))


#-----------Main Menu-----------------------

class GameMenu(): # class for the main menu

    def __init__(self, screen, items):

        self.screen = screen
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        self.background = menu_background
        self.clock = pygame.time.Clock()

        self.items = items
        self.items = []

    def run(self): # function that actually loads the menu

        pygame.init()
        mainloop = True

        # imports and plays title screen music
        pygame.mixer.init()
        pygame.mixer.music.load('title music.mp3')
        pygame.mixer.music.play()

        # loop makes the menu live
        while mainloop:

            self.clock.tick(50)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    mainloop = False

            # Draws the picture for the menu background
            self.screen.blit(menu_background,(0,0))

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()


if __name__ == "__main__": # Not sure why this works tbh

    screen = pygame.display.set_mode((1200, 600), 0, 32)
    pygame.mixer.init()
    pygame.mixer.music.load('title music.mp3')
    pygame.mixer.music.play()
    menu_items = ('Start', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()


#------------Sprites------------------------------

class Charater(pygame.sprite.Sprite): # Sets up character and character movements

    def __init__(self):

        # Calls the parent's constructor
        super().__init__()

        # Assigns a picture to the character sprite
        self.image = pygame.image.load('bhagyesh_new.png')
        self.image.set_colorkey(WHITE)

        # Puts the picture in a sprite
        self.rect = self.image.get_rect()

        # Set speed  of the player
        self.change_x = 0
        self.change_y = 0

        # List of sprites character can collide with
        self.level = None

    def update(self): # Character movement

        # Gravity
        self.calc_gravity()

        # Moveing left and right
        self.rect.x += self.change_x

        # Collision detection
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:

            # If character is moving right,set it's right side to the left side of the item it hits
            if self.change_x > 0:

                self.rect.right = block.rect.left

            elif self.change_x < 0:

                # Else if character is moving left, do the opposite.
                self.rect.left = block.rect.right

        # Moveing up and down
        self.rect.y += self.change_y

        # More collision detection
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:

            # Resets character position based on the top/bottom of the object.
            if self.change_y > 0:

                self.rect.bottom = block.rect.top

            elif self.change_y < 0:

                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_gravity(self): #math for the gravity of the game

        if self.change_y == 0:
            self.change_y = 1

        else:
            self.change_y += .35

        # Checks if the character is on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:

            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self): # function for the jumping mechanic

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is valid to jump, increase speed
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        # user hits left key
        self.change_x = -6

    def go_right(self):
        # user hits right key
        self.change_x = 6

    def stop(self):
        # user lets off keyboard
        self.change_x = 0


class Platform_level_one(pygame.sprite.Sprite): # class for the platform sprites

    def __init__(self, width, height):

        super().__init__()

        # images for the platform texture
        self.image = pygame.image.load("final plat form texture.png")
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()


class Platform_level_two(pygame.sprite.Sprite): # class for the platform sprites in level two

    def __init__(self, width, height):

        super().__init__()

        # images for the platform texture
        self.image = pygame.image.load("big red texture.png")
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

class Flag(pygame.sprite.Sprite): #class for the flag at end of level

    def __init__(self):

        super().__init__()

        # image for flag texture

        self.image = pygame.image.load("flag.png")
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

class MovingPlatform(Platform_level_one): # class for the moving platforms

    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    level = None

    def update(self): # movement of the platform

        # Moveing left and right
        self.rect.x += self.change_x

        # Checks to see if collision with character left and ride
        hit = pygame.sprite.collide_rect(self, self.player)

        if hit:

            if self.change_x < 0:
                self.player.rect.right = self.rect.left

            else:
                self.player.rect.left = self.rect.right

        # Moveing up and down
        self.rect.y += self.change_y

        # Check to see if collision with character up and down
        hit = pygame.sprite.collide_rect(self, self.player)

        if hit:

            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top

            else:
                self.player.rect.top = self.rect.bottom

        # Checks boundries
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift

        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1



# ---------------Level Building-------------------------------

class Level(object): #class that builds each level


    def __init__(self, player):

        # groups the sprites
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = background

        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000

    def update(self):

        #updates level
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):

        # Draw the background
        screen.blit(background, (0,0))

        # Draws all the sprite lists that
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x): # creates a scrolling platformer

        # Keeps track of the amount scrollled
        self.world_shift += shift_x

        # Iterates thru each sprite and moves it
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level): # level one builder

    def __init__(self, player):

        Level.__init__(self, player)

        self.level_limit = -1600
        self.flag_list = []

        # List with width, height, x, and y of platform

        level = [[210, 70, 500, 500],
                 [210, 70, 600, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1120, 280],
                 [210, 70, 1220, 280],
                 [210, 70, 1950, 200],

                 #end of level
                 [210, 70, 2190, 400],
                 [210, 70, 2190, 500],
                 [210, 70, 2290, 400],
                 [210, 70, 2290, 500],
                 [210, 70, 2390, 400],
                 [210, 70, 2390, 500],
                 [210, 70, 2490, 400],
                 [210, 70, 2490, 500],
                 [210, 70, 2590, 400],
                 [210, 70, 2590, 500],

                 [210, 70, 2690, 400],
                 [210, 70, 2690, 500],
                 [210, 70, 2690, 300],
                 [210, 70, 2690, 200],
                 [210, 70, 2690, 100],
                 [210, 70, 2690, 0],

                 [210, 70, 2790, 400],
                 [210, 70, 2790, 500],
                 [210, 70, 2790, 300],
                 [210, 70, 2790, 200],
                 [210, 70, 2790, 100],
                 [210, 70, 2790, 0],

                 [210, 70, 2890, 400],
                 [210, 70, 2890, 500],
                 [210, 70, 2890, 300],
                 [210, 70, 2890, 200],
                 [210, 70, 2890, 100],
                 [210, 70, 2890, 0],

                 [210, 70, 2990, 400],
                 [210, 70, 2990, 500],
                 [210, 70, 2990, 300],
                 [210, 70, 2990, 200],
                 [210, 70, 2990, 100],
                 [210, 70, 2990, 0],

                 [210, 70, 3090, 400],
                 [210, 70, 3090, 500],
                 [210, 70, 3090, 300],
                 [210, 70, 3090, 200],
                 [210, 70, 3090, 100],
                 [210, 70, 3090, 0],

                 [210, 70, 3190, 400],
                 [210, 70, 3190, 500],
                 [210, 70, 3190, 300],
                 [210, 70, 3190, 200],
                 [210, 70, 3190, 100],
                 [210, 70, 3190, 0],

                 [210, 70, 3290, 400],
                 [210, 70, 3290, 500],
                 [210, 70, 3290, 300],
                 [210, 70, 3290, 200],
                 [210, 70, 3290, 100],
                 [210, 70, 3290, 0]]

        flags = [[70, 200, 2590, 200]]

        # Loops through each list and draws corresponding object
        for platform in level:

            block = Platform_level_one(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        for flag in flags:

            block = Flag()
            block.rect.x = flag[2]
            block.rect.y = flag[3]

            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_02(Level): # builds level 2

    def __init__(self, player):

        Level.__init__(self, player)

        self.level_limit = -1500

        # Array with type of platform, and x, y location of the platform.
        level = [
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1100, 300],
                 [210, 70, 1200, 300],
                 [210, 70, 1400, 200],
                 [210, 70, 1800, 100],
                 [210, 70, 1900, 200],
                 [210, 70, 2000, 300],
                 [210, 70, 2100, 400],


                #end of level

                 [210, 70, 2190, 400],
                 [210, 70, 2190, 500],
                 [210, 70, 2290, 400],
                 [210, 70, 2290, 500],
                 [210, 70, 2390, 400],
                 [210, 70, 2390, 500],
                 [210, 70, 2490, 400],
                 [210, 70, 2490, 500],
                 [210, 70, 2590, 400],
                 [210, 70, 2590, 500],


                 [210, 70, 2690, 400],
                 [210, 70, 2690, 500],
                 [210, 70, 2690, 300],
                 [210, 70, 2690, 200],
                 [210, 70, 2690, 100],
                 [210, 70, 2690, 0],

                 [210, 70, 2790, 400],
                 [210, 70, 2790, 500],
                 [210, 70, 2790, 300],
                 [210, 70, 2790, 200],
                 [210, 70, 2790, 100],
                 [210, 70, 2790, 0],

                 [210, 70, 2890, 400],
                 [210, 70, 2890, 500],
                 [210, 70, 2890, 300],
                 [210, 70, 2890, 200],
                 [210, 70, 2890, 100],
                 [210, 70, 2890, 0],

                 [210, 70, 2990, 400],
                 [210, 70, 2990, 500],
                 [210, 70, 2990, 300],
                 [210, 70, 2990, 200],
                 [210, 70, 2990, 100],
                 [210, 70, 2990, 0],

                 [210, 70, 3090, 400],
                 [210, 70, 3090, 500],
                 [210, 70, 3090, 300],
                 [210, 70, 3090, 200],
                 [210, 70, 3090, 100],
                 [210, 70, 3090, 0],

                 [210, 70, 3190, 400],
                 [210, 70, 3190, 500],
                 [210, 70, 3190, 300],
                 [210, 70, 3190, 200],
                 [210, 70, 3190, 100],
                 [210, 70, 3190, 0],

                 [210, 70, 3290, 400],
                 [210, 70, 3290, 500],
                 [210, 70, 3290, 300],
                 [210, 70, 3290, 200],
                 [210, 70, 3290, 100],
                 [210, 70, 3290, 0],

        ]

        flags = [[210, 70, 2500, 200]]

        # Iterates through the list and draws the corresponding platforms
        for platform in level:

            block = Platform_level_two(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            self.platform_list.add(block)

        for flag in flags:
            block = Flag()
            block.rect.x = flag[2]
            block.rect.y = flag[3]

            self.platform_list.add(block)

        # creates a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 10
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

#--------------Main Game----------------------------------------

def main():

    # live game setup
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Main Soundtrack.mp3')
    pygame.mixer.music.play(-1)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("TeleLob")

    # Establishes the character
    player = Charater()

    # Draws the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Manages the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------

    while not done:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

            # keybinds
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the character
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If  character gets near the right side, scroll world left
        if player.rect.right >= 500:

            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the chacter gets near left side, scroll world right
        if player.rect.left <= 120:

            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # Brings character to the next level when reaching the end of the previous
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:

            if current_level_no < len(level_list)-1:

                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

            else:
                done = True

        # --------Drawing Objects--------------------------

        current_level.draw(screen)
        active_sprite_list.draw(screen)


        # All drawing code must stay above this

        # updates screen
        pygame.display.flip()

    pygame.quit()

# idk why this works
if __name__ == "__main__":
    main()

