# /// script
# dependencies = ["pytmx"]
# ///
import pygame
from sys import exit
import math
from settings import *
from map_loader import *
from Assets import Assets
import asyncio


import pytmx.util_pygame
pygame.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Photo puzzel")
clock = pygame.time.Clock()
currentLevel = "untitled.tmx"
tmxdata = pytmx.util_pygame.load_pygame(currentLevel)
mouse_lock = False
paste_lock = False
scroll = False
Active = False
LevelSelect = False 
coppied = True
assets = Assets()
map_cords = assets.frame_rect
class Player(pygame.sprite.Sprite ):
    def __init__(self , x ,y):
        super().__init__()
        self.image = pygame.Surface(PlayerSize).convert_alpha()
        self.image.fill((255,255,0))
        self.pos = pygame.math.Vector2(x, y)
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
        if self.Win():
            global currentLevel
            currentLevel = "untitled2.tmx"
            Reset()
    def Colide(self):
        tile_id = Get_tile(tmxdata, self)
        return tile_id in (103, 115 , 334 , 87 , 332)
    def Win(self):
            return Get_tile(tmxdata, self) in (335,336)
    def PlayerRotate(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change = (self.mouse_pos[0] - self.pos.x)
        self.y_change = (self.mouse_pos[1] - self.pos.y)
        self.angle = math.degrees(math.atan2(self.y_change , self.x_change))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
    def Respawn(self) :
        global mouse_lock, paste_lock
        self.hitbox.x = StartX
        self.hitbox.y = StartY
        mouse_lock = False
        paste_lock = False

def Reset():
    global tmxdata , photoS , selected , data , Active
    data = None 
    photoS.clear()
    tmxdata = pytmx.util_pygame.load_pygame(currentLevel)
    selected.clear 
    player.Respawn()
    Active = False

async def main():
  global player, currentLevel, LevelSelect, Active, scroll
  global mouse_lock, paste_lock, coppied, data
  print("main() entered")
  player = Player(StartX ,StartY)
  data = None
  player = Player(StartX, StartY)
  while True:
    if Active:
      screen.fill((0,0,0))
      Select_CrossTile(tmxdata)  
      Get_tile(tmxdata,player)
      load_map(tmxdata, screen , map_cords )
      draw_selected(tmxdata, screen)
      screen.blit(player.image, player.rect)
      assets.draw(screen)
      if scroll:
          assets.scroll()
      else:
          assets.pull()
    elif not Active and not LevelSelect:
        screen.fill((200,200,200))
        screen.blit(assets.Hover(assets.ButtonPlay, assets.ButtonPlayHover, assets.ButtonPlay_rect),assets.ButtonPlay_rect)
        screen.blit(assets.Hover(assets.ButtonSettings, assets.ButtonSettingsHover, assets.ButtonSettings_rect),assets.ButtonSettings_rect)
        screen.blit(assets.Hover(assets.ButtonQuit, assets.ButtonQuitHover, assets.ButtonQuit_rect),assets.ButtonQuit_rect)
    elif LevelSelect:
        assets.drawLevels(screen)


    #==============EVENTS===========
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
            
        if event.type == pygame.MOUSEBUTTONDOWN:
             if LevelSelect:
                 for rect , level in ((assets.Level1_rect, "untitled.tmx")
                                     ,(assets.Level2_rect, "untitled2.tmx")
                                     ,(assets.Level3_rect, "untitled3.tmx") ):
                     if rect.collidepoint(event.pos):
                         currentLevel = level 
                         LevelSelect = False 
                         Reset()
                         if level == "untitled3.tmx":
                            player.hitbox.x = 20
                            player.hitbox.y = 300
                         Active = True
                     
             if event.button == 1 and assets.ButtonQuit_rect.collidepoint(event.pos) and not Active:
                 pygame.quit()
                 exit()
             if assets.ButtonPull_rect.collidepoint(event.pos) and Active:
                scroll = not scroll
             if event.button == 1 and not mouse_lock and not assets.ButtonPull_rect.collidepoint(event.pos) and Active:
                data = Get_CrossTile(tmxdata)
                if data is not None:
                 update_strogae(tmxdata , data )
                 mouse_lock = True
                 paste_lock = True
                 coppied = True
             if event.button == 3 and paste_lock and Active:
                 paste_lock = False
                 clear_strogae(tmxdata)
                 place_photo(tmxdata , data)
                 mouse_lock = False
             if assets.ButtonPlay_rect.collidepoint(event.pos) and not Active:
                 LevelSelect = True           
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_1:
              currentLevel = "untitled.tmx"
          if event.key == pygame.K_q and Active:
              trow_away(tmxdata)
              mouse_lock = False
              paste_lock = False
          if event.key == pygame.K_e:
              Reset()
          if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
              pygame.quit()
              exit()
        await asyncio.sleep(0)
    player.Update()
    pygame.display.update()
    clock.tick(FPS)
    await asyncio.sleep(0)
asyncio.run(main())
print("main() entered")
