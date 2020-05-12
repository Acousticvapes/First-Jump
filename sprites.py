# Sprite classes for platform game
import pygame as pg
from settings import *
from os import path
from random import choice, randrange
vec = pg.math.Vector2 

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab image out of spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x , y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(20, HEIGHT - 100) 
        self.vel = vec(0, 0) # (x, y)
        self.acc = vec(0, 0)
    
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(0, 0, 36, 39)]
        for frame in self.standing_frames:
            frame.set_colorkey(0)
        self.walk_frames_r = [self.game.spritesheet.get_image(0, 0, 36, 39)]
        for frame in self.standing_frames:
            frame.set_colorkey(0)
        self.walk_frames_l = [self.game.spritesheet.get_image(36, 0, 36, 39)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(0)     

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.image = self.game.spritesheet.get_image(42, 0, 31, 39)
            self.image.set_colorkey(0)
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.image = self.game.spritesheet.get_image(5, 0, 30, 39)
            self.image.set_colorkey(0)

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # Wrap around sides of screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = (game.all_sprites, game.platforms)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(72, 41, 28, 7),
                  self.game.spritesheet.get_image(0, 80, 24, 7)]
        self.image = choice(images)
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Power(self.game, self)

class Power(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = (game.all_sprites, game.powerups)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])
        self.image = self.game.spritesheet.get_image(126, 10, 27, 38)
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top
    
    def update(self):
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat):
            self.kill()
