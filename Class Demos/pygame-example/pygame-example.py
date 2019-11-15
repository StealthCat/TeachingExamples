from PIL import Image
import pygame
from pygame.locals import *
import os

import time

class GIFImage(object):
    def __init__(self, filename, flip = False):
        self.filename = filename
        self.image = Image.open(filename)
        self.flip = flip
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False

    def get_rect(self):
        return pygame.rect.Rect((0,0), self.image.size)

    def get_frames(self):
        image = self.image
        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)
        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette
                if self.flip:
                    imag2 = image.transpose(Image.FLIP_LEFT_RIGHT)
                else:
                    imag2 = image
                pi = pygame.image.fromstring(imag2.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                #import pdb;pdb.set_trace()
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0,0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()

        screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames)-1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)
    def fastforward(self):
        self.seek(self.length()-1)

    def get_height(self):
        return self.image.size[1]
    def get_width(self):
        return self.image.size[0]
    def get_size(self):
        return self.image.size
    def length(self):
        return len(self.frames)
    def reverse(self):
        self.reversed = not self.reversed
    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        return new

class Character(object):
    #Class Constants
    IDLE = 0x1
    WALK = 0x2
    RIGHT = 0x1
    LEFT = 0x2
    def __init__(self, rel_path, screen):
        #Storage path for backing files, character images and sounds
        self.rel_path = rel_path
        #Load animation files
        self.animations = list()
        self.animations.append(None) #Place holder bc I don't want to use zero for an index action
        self.animations.append((GIFImage(os.path.join(self.rel_path,"idle.gif")), GIFImage(os.path.join(self.rel_path,"idle.gif"), flip = True)))
        self.animations.append((GIFImage(os.path.join(self.rel_path,"walk.gif")), GIFImage(os.path.join(self.rel_path,"walk.gif"), flip = True)))
        #Store connditions of character that effect rendering
        self.momentum_x = 0
        self.momentum_y = 1 #Start with gravity applied?
        self.screen = screen
        self.set_active_animation(self.IDLE, self.RIGHT) 
        self.is_jumping = False
    def check_collision(self):
        character_info = self.active_animation.get_width(), self.active_animation.get_height()
        ceiling = 0
        floor = self.screen.get_height() -110
        left_wall = 0
        right_wall = self.screen.get_width()
        #import pdb;pdb.set_trace()
        if self.location[0] < left_wall:
            self.location = (left_wall, self.location[1])
        elif self.location[0]+ character_info[0] > right_wall:
            self.location = (right_wall - character_info[0], self.location[1])
        if self.location[1] < ceiling:
            self.location = (self.location[0], ceiling)
        elif self.location[1] + character_info[1] > floor:
            self.is_jumping = False
            self.location = (self.location[0], (floor - character_info[1]))
    def render(self):
        self.active_animation.render(self.screen, self.location)
    def set_active_animation(self, idx, direction):
        try:
            self.active_animation = self.animations[idx][direction - 1]
        except IndexError as e:
            print("Animation not implemented with ID: {} for {}".format(idx, self.__class__.__name__))
        

class Player(Character):
    RUN = 0x3
    JUMPUP = 0x4
    FALLING = 0x5
    def __init__(self, rel_path, screen, background_handler):
        #Call Character init to get everything they initialize
        super().__init__(rel_path, screen)
        #Player specific stuff
        self.animations.append((GIFImage(os.path.join(self.rel_path,"run.gif")), GIFImage(os.path.join(self.rel_path,"run.gif"), flip = True)))
        self.animations.append((GIFImage(os.path.join(self.rel_path,"jumpup.gif")), GIFImage(os.path.join(self.rel_path,"jumpup.gif"), flip = True)))
        self.animations.append((GIFImage(os.path.join(self.rel_path,"jumpdown.gif")), GIFImage(os.path.join(self.rel_path,"jumpdown.gif"), flip = True)))
        self.set_location()
        self.keydown_list = []
        self.multiplier = 1
        self.direction = self.RIGHT
        self.max_momentum = 5
        self.background_handler = background_handler
    def set_location(self):
        x = (self.screen.get_width() / 2) - (self.active_animation.get_width() / 2)
        y = (self.screen.get_height() / 2) - (self.active_animation.get_height()/ 2)
        self.location =  x, y
    def handle_keydown(self, key):
        if key in [97, 100, 32]:
            self.keydown_list.append(key)
            '''
            if key == 100:
                self.set_active_animation(self.WALK, self.RIGHT)
                self.keydown_list.append()
            elif key == 97:
                self.set_active_animation(self.WALK, self.LEFT)
            '''
        elif key in [303,304]:
            self.multiplier += 2
        else:
            print(key)
    def handle_keyup(self, key):
        if key in [97, 100, 32]:
            try:
                self.keydown_list.remove(key)
            except ValueError as e:
                pass
        elif key in [303,304]:
            self.multiplier -= 2
        else:
            print(key)
    def increase_momentum_x(self, value):
        if not self.is_jumping:
            new_momentum = self.momentum_x + (value * self.multiplier)
        else:  #Looks weird to sprint jump sideways
            new_momentum = self.momentum_x + value
        if new_momentum > 0:
            if new_momentum <= self.max_momentum:
                self.momentum_x = new_momentum
            else:
                self.momentum_x = self.max_momentum
        else:
            if new_momentum >= (self.max_momentum *-1):
                self.momentum_x = new_momentum
            else:
                self.momentum_x = (self.max_momentum *-1)
    def render(self):
        #Check key state and apply
        #direction_set will handle if both right and left are held down(will rely on the one pushed last until keyup)
        direction_set = False
        for key in self.keydown_list:
            if key == 97 and not direction_set: 
                self.increase_momentum_x(-1)
                self.direction = self.LEFT
            elif key == 100 and not direction_set:
                self.increase_momentum_x(1)
                self.direction = self.RIGHT
            elif key == 32:
                if not self.is_jumping:
                    self.is_jumping = True
                    self.momentum_y = -50
        #Set new location based on momentum
        self.location = (self.location[0]),  (self.location[1] + (-2 if self.momentum_y < 0 else self.momentum_y))
        #Scroll screen based on momentum
        self.background_handler.bg_x -= self.momentum_x
        self.background_handler.bg_x2 -= self.momentum_x
        #Set image based on momentum
        if self.momentum_y <=0:
            self.set_active_animation(self.JUMPUP, self.direction)
        elif self.is_jumping:
            self.set_active_animation(self.FALLING, self.direction)
        elif not self.momentum_x == 0:
            if self.momentum_x == 1 or self.momentum_x == -1:
                self.set_active_animation(self.WALK, self.direction)
            else:
                self.set_active_animation(self.RUN, self.direction)
        else:
            self.set_active_animation(self.IDLE, self.direction)
        #Check for bounds collision
        self.check_collision()
        # Render
        self.active_animation.render(self.screen, self.location)
            
class background_scroller(object):   
    def __init__(self, image_name, screen):
        self.bg = pygame.image.load(os.path.join('images',image_name)).convert()
        self.image_width = self.bg.get_width()
        self.screen = screen
        self.bg_x = 0
        self.bg_x2 = self.image_width
    def render(self):
        if self.bg_x < self.image_width * -1:
            self.bg_x = self.image_width
        if self.bg_x2 < self.image_width * -1:
            self.bg_x2 = self.image_width 

        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg_x2, 0))
        
        
        
def exert_forces(charcter):
    #Gravity
    if not charcter.momentum_y == 1:
        charcter.momentum_y += 1
    #Drag
    if charcter.momentum_x < 0:
        if charcter.momentum_x < -1:
            charcter.momentum_x += 1
        charcter.momentum_x += 1
    elif charcter.momentum_x  > 0:
        if charcter.momentum_x > 1:
            charcter.momentum_x -= 1
        charcter.momentum_x -= 1
        
def main():
    pygame.init()
    clock = pygame.time.Clock()
    TICK_RATE = 60
    screen = pygame.display.set_mode((640, 480))
    bg_scroller = background_scroller('bg.png', screen)
    pygame.mixer.music.load('findyou.ogg')
    pygame.mixer.music.play(-1)
    characters = []
    player = Player('./Player_One', screen, bg_scroller)
    characters.append(player)
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                player.handle_keydown(event.key)
            elif event.type == KEYUP:
                player.handle_keyup(event.key)
            else:
                print(event)
        bg_scroller.render()
        player.render()
        for character in characters:
            exert_forces(character)
        pygame.display.flip()
        clock.tick(TICK_RATE)

if __name__ == "__main__":
    main()