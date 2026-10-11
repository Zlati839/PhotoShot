import pygame
from sys import exit
import math
from settings import *
from map_loader import load_map
from map_loader import Get_tile
from map_loader import Get_CrossTile
import pytmx.util_pygame
pygame.init()

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Photo puzzel")
clock = pygame.time.Clock()
tmxdata = pytmx.util_pygame.load_pygame("untitled.tmx")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(PlayerSize).convert_alpha()
        self.image.fill((255,255,0))
        self.pos = pygame.math.Vector2(StartX, StartY)
        self.hitbox = self.image.get_rect(center = self.pos)
        self.rect = self.hitbox.copy()
        self.base_image = self.image.copy()
    def UserInput(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PlayerSpeed
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.velocity_y = -self.speed
        if key[pygame.K_s]:
            self.velocity_y = self.speed
        if key[pygame.K_d]:
            self.velocity_x = self.speed
        if key[pygame.K_a]:
            self.velocity_x = -self.speed
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= math.sqrt(2)/2
            self.velocity_y *= math.sqrt(2)/2
    def Move(self):
        self.pos.x += self.velocity_x
        self.pos.y += self.velocity_y
        self.hitbox = self.pos
        self.rect.center = self.hitbox
    def Update(self):
        self.UserInput()
        old_pos = self.pos.copy()
        self.Move()
        self.PlayerRotate()
        if self.Colide():
            self.pos = old_pos
            self.rect.center = self.pos
            print("aaa")
    def Colide(self):
        tile_id = Get_tile(tmxdata, self)
        return tile_id in (103, 115)
    def PlayerRotate(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change = (self.mouse_pos[0] - self.pos.x)
        self.y_change = (self.mouse_pos[1] - self.pos.y)
        self.angle = math.degrees(math.atan2(self.y_change , self.x_change))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
player = Player()


while True:
    screen.fill((0,0,0))
    Get_tile(tmxdata,player)
    load_map(tmxdata, screen)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(player.image, player.rect)
    player.Update()
    Get_CrossTile(tmxdata)
    pygame.display.update()
    clock.tick(FPS)
