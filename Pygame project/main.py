# /// script
# dependencies = ["pytmx", "pygame_gui", "!python-i18n"]
# ///
import pygame
from sys import exit
import math
import sys
from pathlib import Path
from settings import *
from map_loader import *
from Assets import Assets
import asyncio
sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
import pygame_gui 
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog
from pygame_gui.core.gui_font_freetype import GUIFontFreetype
from pygame_gui.core.gui_font_pygame import GUIFontPygame
from pygame_gui.core.package_resource import PackageResource
from pygame_gui.core.utility import FontResource
import pytmx.util_pygame
import random


# pygame.font needs file paths for package fonts in the browser build.
load_gui_font = FontResource.load

#==============================================
def load_gui_font_from_path(font_resource):#===
    if not isinstance(font_resource.location, PackageResource):
        return load_gui_font(font_resource)

    try:
        font_path = font_resource.location.to_path()
        if font_resource.font_type_to_use == "freetype":
            font_resource.loaded_font = GUIFontFreetype(
                font_path,
                font_resource.size,
                font_resource.force_style,
                font_resource.style,
            )
        else:
            font_resource.loaded_font = GUIFontPygame(
                font_path,
                font_resource.size,
                font_resource.force_style,
                font_resource.style,
            )
    except (pygame.error, OSError):
        return FileNotFoundError(
            f"Unable to load resource with path: {font_resource.location}"
        )
    return None
FontResource.load = load_gui_font_from_path#===
class SynchronousResourceLoader:           #===
    def __init__(self):
        self.resources = []
        self._started = False

    def add_resource(self, resource):
        if self._started:
            self._load(resource)
        else:
            self.resources.append(resource)

    def start(self):
        self._started = True

    def started(self):
        return self._started

    def update(self):
        while self.resources:
            self._load(self.resources.pop(0))
        return True, 1.0

    @staticmethod
    def _load(resource):
        error = resource.load()
        if error is not None:
            raise error
#==============================================

pygame.init()
pygame.display.set_caption("Photo puzzel")
#Flash
Flash = pygame.Surface((960, 650), pygame.SRCALPHA)
Flash.fill((255,255,255))

#Bakcground color changer
color_picker = None
currentColor = pygame.Color(200,200,200)

#Gui color
color_picker_Gui  = None
currentColor_Gui = pygame.Color(200,200,200)

#Player color
color_picker_Player  = None
currentColor_Player = pygame.Color(255,255,0)

#screen
screen = pygame.display.set_mode((Width, Height))

#ui manager and elements
ui_resource_loader = SynchronousResourceLoader()
ui_manager = pygame_gui.UIManager((Width, Height), resource_loader=ui_resource_loader)
ui_resource_loader.start()
ui_resource_loader.update()
button_color = UIButton(relative_rect=pygame.Rect(-500, -460, 150 , 30), text= 'Pick Color' ,anchors={'left': 'right' ,'right': 'right' ,'top' : 'bottom' ,  'bottom':'bottom'},manager=ui_manager)
button_color_Gui = UIButton(relative_rect=pygame.Rect(-600, -345, 150 , 30), text= 'Pick Color for Gui' ,anchors={'left': 'right' ,'right': 'right' ,'top' : 'bottom' ,  'bottom':'bottom'},manager=ui_manager)
button_color_Player = UIButton(relative_rect=pygame.Rect(-600, -255, 150 , 30), text= 'Pick Player color' ,anchors={'left': 'right' ,'right': 'right' ,'top' : 'bottom' ,  'bottom':'bottom'},manager=ui_manager)

#brightness
Brightness = pygame.Surface((960, 650), pygame.SRCALPHA)
Bright = 1

#General
clock = pygame.time.Clock()
currentLevel = "untitled.tmx"
tmxdata = pytmx.util_pygame.load_pygame(currentLevel)

#Locks
mouse_lock = False
paste_lock = False
scroll = False
coppied = True
tutorialing = False
playing = False
water = False

#Game States
Active = False
LevelSelect = False 
Setting = False
Paused = False
Winer = False
win_positions = []
Taken_Photos = 0

#Assets and idk
assets = Assets()
map_cords = assets.frame_rect

#Paused
PausedBg = pygame.Surface((960, 650), pygame.SRCALPHA)
PausedBg.fill((0,0,0 ,128 ))

class Player(pygame.sprite.Sprite ):
    def __init__(self , x ,y):
        super().__init__()
        self.image = pygame.Surface(PlayerSize).convert_alpha()
        self.image.fill(currentColor_Player)
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
    def Colide(self):
        tile_id = Get_tile(tmxdata, self)
        return tile_id in (103, 115 , 334 , 87 , 332)
    def Win(self):
            return Get_tile(tmxdata, self) in (335,336)
    def Teleport(self):
                return Get_tile(tmxdata, self) == 331
    def PlayerRotate(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.x_change = (self.mouse_pos[0] - self.pos.x)
        self.y_change = (self.mouse_pos[1] - self.pos.y)
        self.angle = math.degrees(math.atan2(self.y_change , self.x_change))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)
    def Respawn(self):
     global mouse_lock, paste_lock,tmxdata
     if currentLevel == "untitled3.tmx":
         StartX = 20
         StartY = 300
     else:
         StartX = 100
         StartY = 100
     tmxdata = pytmx.util_pygame.load_pygame(currentLevel)
     self.pos.update(StartX, StartY)
     mouse_lock = paste_lock = False

class Slider():
    def __init__(self , pos:  tuple , size:tuple , initial_value : float , min: int , max: int ):
        self.pos = pos 
        self.size = size 

        self.slider_left = self.pos[0] - (size[0]//2) # gets the left side of the slider 
        self.slider_right = self.pos[0] + (size[0]//2) # ge5ts the right side of the slider
        self.slider_top = self.pos[1] - (size[1]//2) #takes the top of the slider 

        self.min  = min 
        self.max = max 
        self.initial = (self.slider_right - self.slider_left)* initial_value # this is an %

        self.container_rect = pygame.Rect(self.slider_left , self.slider_top , self.size[0] , self.size[1])
        self.button_rect = pygame.Rect(self.slider_left +self.initial - 5 , self.slider_top, 10, self.size[1])
    def render(self , app):
        pygame.draw.rect(app , "darkgray" , self.container_rect)
        pygame.draw.rect(app , "blue" , self.button_rect)
    def MoveSlide(self , mouse):
        self.button_rect.centerx = mouse[0]
    def get_value(self):
        valueRange = self.slider_right - self.slider_left -1
        buttonVal = self.button_rect.centerx - self.slider_left
        return (buttonVal/valueRange)*(self.max-self.min)+self.min
slider = [Slider((450,50) , (500,30),0 , 0 ,255)]

class Timer():
    def __init__(self):
        self.start_time = 0
        self.stopped = 0        
        self.running = False

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True
    def stop(self):
        if self.running:
            self.stopped = pygame.time.get_ticks() - self.start_time
            self.running = False
    def text(self):
        if self.running:
            text = pygame.time.get_ticks() - self.start_time
        else :
            text = self.stopped
        total_seconds = int(text/1000)
        minutes = total_seconds//60
        seconds = total_seconds%60
        return f"{minutes:02}:{seconds:02}"
    def resume(self):
     if not self.running:
        self.start_time = pygame.time.get_ticks() - self.stopped
        self.running = True


def make_win_positions(count=5):
    return [(random.randint(0, Width - 300), random.randint(0, Height - 100))
            for _ in range(count)]
def Random_text():
    for x, y in win_positions:
        draw_text("You Won!", big_font, (0, 0, 255), x, y)
    
  
def Reset():
    global tmxdata , photoS , selected , data , Active , Paused,tutorialing , tutorial_text, Setting , Taken_Photos  
    data = None 
    Taken_Photos = 0
    tutorialing = False
    tutorial_text = "Press m1 to take a picture"
    photoS.clear()
    tmxdata = pytmx.util_pygame.load_pygame(currentLevel)
    selected.clear()
    Setting = False 
    player.Respawn()
    Active = False
    Paused = False
text_font = pygame.font.SysFont("None" , 30)
tutorial_font = pygame.font.SysFont("None" , 35)
big_font = pygame.font.SysFont("None", 90)
tutorial_text = "Press m1 to take a picture"
def draw_text(text , font , text_color , x ,y ):
    img = font.render(text , True , text_color)
    screen.blit(img,(x,y))

async def main():
  global player, currentLevel, LevelSelect, Active, scroll , color_picker_Gui , currentColor_Gui, Paused ,  Winer , win_positions , tutorialing, tutorial_text, water,Taken_Photos
  global mouse_lock, paste_lock, coppied, data , Setting , Bright , Brightness,currentColor,color_picker,color_picker_Player , currentColor_Player , playing , Flash
  data = None
  player = Player(StartX, StartY)
  Time = Timer()
  while True:
    time_delta = clock.tick(FPS) / 1000.0
    ui_manager.update(time_delta)
    Brightness.fill((0,0,0 , int(Bright)))
    #=================Ingame=====================
    if Active:
      screen.fill((0,0,0))
     #Map loader
      Select_CrossTile(tmxdata)  
      Get_tile(tmxdata,player)
      if not Setting:
        load_map(tmxdata, screen , map_cords )
      if not Paused:
        draw_selected(tmxdata, screen , currentColor_Gui)

     #Player drawn
      screen.blit(player.image, player.rect)

     # Draws layer 2 on top of the player
      if not Setting:
        draw_layer2(tmxdata, screen, map_cords)
    
     # Blocked tiles highlight
      if not Paused:
        if Blocked_photo(tmxdata):
            draw_selected(tmxdata, screen , (255, 60, 60))
        else:
            draw_selected(tmxdata, screen , currentColor_Gui)
     #Player Win
      if player.Win():
          tutorialing = False
          Active  = False
          Winer = True
          win_positions = make_win_positions()
          Time.stop()
      if player.Teleport():
          if get_tile_cords(tmxdata,330):
              cords = get_tile_cords(tmxdata, 330)
              if cords is not None:
                player.pos.update(cords[0], cords[1])
                player.rect.center = player.pos
     #Text during tutorial
      if tutorialing:
           draw_text(tutorial_text , tutorial_font , (255,255,255),100 , 400)

     #Photo Counter
      draw_text("Photos taken: " + str(Taken_Photos)  , tutorial_font , (255,255,255),750 , 600)
  
     #Gui
      assets.draw(screen)
     #Draws timer
      draw_text(Time.text() , tutorial_font, (255,255,255),20 , 600)
     #Paused
      if Paused:
          Time.stop()
          screen.blit(PausedBg, (0, 0))
          draw_text("Paused" , big_font , (255,255,255),375 , 40)
          screen.blit(assets.Resume, assets.resume_rect)
          draw_text("Resume" , text_font , (255,255,255),assets.buttonXR - 38 , assets.buttonYR - 10)
          screen.blit(assets.Options, assets.options_rect)
          draw_text("Options" , text_font , (255,255,255),assets.buttonXO - 38 , assets.buttonYO - 10)
          screen.blit(assets.Quit, assets.quit_rect)
          draw_text("Quit" , text_font , (255,255,255),assets.buttonXQ - 20 , assets.buttonYQ - 10)

     #Storage pull and push
      if scroll:
          assets.scroll()
      else:
          assets.pull()
          
    #==========================Main Menu============================
    elif not Active and not LevelSelect and not Setting and not Winer:
        screen.fill((currentColor))
        screen.blit(assets.Hover(assets.ButtonPlay, assets.ButtonPlayHover, assets.ButtonPlay_rect),assets.ButtonPlay_rect)
        screen.blit(assets.Hover(assets.ButtonSettings, assets.ButtonSettingsHover, assets.ButtonSettings_rect),assets.ButtonSettings_rect)
        screen.blit(assets.Hover(assets.ButtonQuit, assets.ButtonQuitHover, assets.ButtonQuit_rect),assets.ButtonQuit_rect)
   #=======================While selecting level====================
    elif LevelSelect:
        assets.drawLevels(screen)
   #============================Winner============================= 
    elif Winer:
        screen.fill((currentColor))
        Random_text()
        draw_text("Photos to beat the level: " + str(Taken_Photos)  , big_font , (255,255,255),100 , 500)
        screen.blit(assets.Return, assets.Return_rect)
        draw_text("Return" , text_font , (255,255,255),assets.buttonXRE - 35 , assets.buttonYRE - 10)
        draw_text(Time.text() , big_font , (255,255,255),630 , 340)
        

    #=========================While settings=================d
    if Setting and not LevelSelect:
        screen.fill((currentColor))
        mouse = pygame.mouse.get_pos()
        for s in slider:
            if s.container_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                s.MoveSlide(mouse)
            s.render(screen)
            Bright = s.get_value()
        #Text beign drawn
        draw_text("Darkness:" , text_font , (0,0,0),50 , 40)
        draw_text("Background Color:" , text_font , (0,0,0),50 , 150)
        draw_text("Gui color:" , text_font , (0,0,0),50 , 260)
        draw_text("Player color:" , text_font , (0,0,0),50 , 350)
        ui_manager.draw_ui(screen)

    #==============EVENTS===========
    for event in pygame.event.get():
        ui_manager.process_events(event)
     #==============================TUTORIAL====================================================================================================
        if event.type == pygame.MOUSEBUTTONDOWN and tutorial_text == "Press m1 to take a picture" and tutorialing:
            tutorial_text = "Press m2 to place the picture anywhere on the map"
        if event.type == pygame.MOUSEBUTTONDOWN and tutorial_text == "Press m2 to place the picture anywhere on the map" and tutorialing:
            if event.button == 3:
              tutorial_text = "You can press q to remove your current picture that you have stored"
        if event.type == pygame.KEYDOWN and tutorial_text == "You can press q to remove your current picture that you have stored" and tutorialing:
                    if event.key == pygame.K_q:
                      tutorial_text = "You can press e if you ever get stuck"
        if event.type == pygame.KEYDOWN and tutorial_text == "You can press e if you ever get stuck" and tutorialing:
                            if event.key == pygame.K_e:
                              tutorial_text = "Thats all Feel free to explore the special tiles"
     #============================================================================================================================================   
     #Button Pressed from pygame_gui
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
         if event.ui_element == button_color and Setting:
             color_picker = UIColourPickerDialog(pygame.Rect(160,50 , 420 , 400),ui_manager ,window_title="Change Backgorund colour" , initial_colour = currentColor)
         if  event.ui_element == button_color_Gui and Setting:
            color_picker_Gui = UIColourPickerDialog(pygame.Rect(160,50 , 420 , 400),ui_manager ,window_title="Change Gui colour" , initial_colour = currentColor_Gui)
         if  event.ui_element == button_color_Player and Setting:
             color_picker_Player = UIColourPickerDialog(pygame.Rect(160,50 , 420 , 400),ui_manager ,window_title="Change Player colour" , initial_colour = currentColor_Player)
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            if event.ui_element == color_picker:
                currentColor = event.colour
            elif event.ui_element == color_picker_Gui:
             currentColor_Gui = event.colour
            elif event.ui_element == color_picker_Player:
                currentColor_Player = event.colour
                player.base_image.fill(currentColor_Player)

     #inside here is select level , All buttons  , taking a picture , pasting a picture , slide storage trigger  
        if event.type == pygame.MOUSEBUTTONDOWN :
             playing = Active and not Paused
             #Select level
             if LevelSelect and not Setting:
                 for rect , level in ((assets.Level1_rect, "untitled.tmx"),(assets.Level2_rect, "untitled2.tmx"),(assets.Level3_rect, "untitled3.tmx"),(assets.Tutorial_rect, "untitled0.tmx"),(assets.Level4_rect, "untitled4.tmx"),(assets.Level5_rect , "untitled5.tmx") ):
                     if rect.collidepoint(event.pos):
                         currentLevel = level 
                         LevelSelect = False 
                         Reset()
                         if level == "untitled0.tmx":
                            tutorialing = True
                         if level == "untitled3.tmx":
                            player.hitbox.x = 20
                            player.hitbox.y = 300
                            
                         Active = True  
                         Time.start()           
            
             #If Left mouse button has been clicked
             if event.button == 1: 
                 if assets.Return_rect.collidepoint(event.pos) and Winer:
                     Winer = False
                     Time.resume()
                 #Resume
                 if assets.resume_rect.collidepoint(event.pos) and Paused:
                     Paused = False
                     Time.resume()
                 #Settings paused
                 if assets.options_rect.collidepoint(event.pos) and Paused:
                     Setting = True
                 #Quit button paused
                 if assets.quit_rect.collidepoint(event.pos) and Paused:
                     Reset()
                 #Quit button
                 if assets.ButtonQuit_rect.collidepoint(event.pos) and not Active and not LevelSelect and not Setting and not Winer:
                   pygame.quit()
                   exit()
                 #Taking a picture
                 if not mouse_lock and not assets.ButtonPull_rect.collidepoint(event.pos) and Active and not Paused and playing:
                    Taken_Photos += 1
                    screen.blit(Flash,(0,0))
                    data = Get_CrossTile(tmxdata)
                    if data is not None:
                        if get_tile_in_photo(tmxdata , data):
                            water = True
                        update_strogae(tmxdata , data )
                        mouse_lock = True
                        paste_lock = True
                        coppied = True
             
             #Storage pull and push
             if assets.ButtonPull_rect.collidepoint(event.pos) and Active and not Paused: 
                scroll = not scroll
            
             #Picture Paste
             if event.button == 3 and paste_lock and Active:
                 paste_lock = False
                 clear_strogae(tmxdata)
                 place_photo(tmxdata , data , water)
                 mouse_lock = False
                 water = False
            
             #Playe Button
             if assets.ButtonPlay_rect.collidepoint(event.pos) and not Active and not LevelSelect and not Setting and not Winer:
                 LevelSelect = True     
            
             #Settings button
             if  assets.ButtonSettings_rect.collidepoint(event.pos) and not Active and not LevelSelect and not Setting and not Winer:
                 Setting = True
                 LevelSelect = False            

     #qol comands lke unstuck and reset picture also esc shortcuts
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_e and Active:
              player.Respawn()
          if event.key == pygame.K_ESCAPE:
            if Setting :
                Setting = False
            elif Active and Paused:
                 Paused = False
                 Time.resume()
            elif Active:
                 Paused = True
          if event.key == pygame.K_1:
              currentLevel = "untitled.tmx"
          if event.key == pygame.K_q and Active:
              trow_away(tmxdata)
              mouse_lock = False
              paste_lock = False
        
        if event.type == pygame.QUIT:
              pygame.quit()
              exit()
        
        await asyncio.sleep(0)
    screen.blit(Brightness, (0, 0))
    if not Paused and Active:
      player.Update()
    pygame.display.update()
    await asyncio.sleep(0)
asyncio.run(main())
