import pygame
from sys import exit
import math
class Assets:
    def __init__(self):
        self.frame = pygame.image.load("Assets/Gui/Photo_frame.png").convert_alpha()
        self.frame_rect = self.frame.get_rect(topleft=(-100,85) )
        self.ButtonPull = pygame.Surface((self.frame.width/5 ,self.frame.height)).convert_alpha()
        self.ButtonPull.fill((255,255,255))
        self.ButtonPull_rect = self.ButtonPull.get_rect(topleft = (self.frame_rect.x +self.frame_rect.width , self.frame.height ))
        #Settings
        self.ButtonSettings = pygame.image.load("Assets/Gui/SettingButton.png").convert_alpha()
        self.ButtonSettingsHover = pygame.image.load("Assets/Gui/SettingButtonHover.png").convert_alpha()
        self.ButtonSettings_rect = self.ButtonSettings.get_rect(topleft = (10 , 100))
        #Play
        self.ButtonPlay = pygame.image.load("Assets/Gui/PlayButton.png").convert_alpha()
        self.ButtonPlayHover = pygame.image.load("Assets/Gui/PlayButtonHover.png").convert_alpha()
        self.ButtonPlay_rect = self.ButtonSettings.get_rect(center = (420 , 230))
        #Quit
        self.ButtonQuit = pygame.image.load("Assets/Gui/QuitButton.png").convert_alpha()
        self.ButtonQuitHover = pygame.image.load("Assets/Gui/QuitButtonHover.png").convert_alpha()
        self.ButtonQuit_rect = self.ButtonSettings.get_rect(topleft = (620 , 100))
        #LevelBackground
        self.LevelBackground = pygame.image.load("Assets/Gui/Level_background.png").convert_alpha()
        self.Background_rect = self.LevelBackground.get_rect(topleft = (0,0))
        #Level1
        self.Level1 = pygame.image.load("Assets/Gui/Level1Button.png").convert_alpha()
        self.Level1_rect = self.Level1.get_rect(topleft = (20, 20))
        #Level2
        self.Level2 = pygame.image.load("Assets/Gui/Level2Button.png").convert_alpha()
        self.Level2_rect = self.Level2.get_rect(topleft = (300, 20))
        #Level3
        self.Level3 = pygame.image.load("Assets/Gui/Level3Button.png").convert_alpha()
        self.Level3_rect = self.Level3.get_rect(topleft = (520, 20))
    def drawLevels(self,screen):
        screen.blit(self.LevelBackground, self.Background_rect)  
        screen.blit(self.Level1, self.Level1_rect)  
        screen.blit(self.Level2, self.Level2_rect) 
        screen.blit(self.Level3, self.Level3_rect) 
        
    def draw(self, screen):
        self.ButtonPull_rect.topleft = (self.frame_rect.right,self.frame_rect.top)
        screen.blit(self.frame, self.frame_rect)  
        screen.blit(self.ButtonPull,self.ButtonPull_rect)   
    def scroll(self):
     if self.frame_rect.x != 20:
        self.frame_rect.x += 10
        if self.frame_rect.x >= 20:
            self.frame_rect.x = 20
    def pull(self):
         if self.frame_rect.x != -100:
            self.frame_rect.x -= 10
            if self.frame_rect.x <= -100:
                self.frame_rect.x = -100
    def Hover(self, picture, hoverpicture, rect):
        if rect.collidepoint(pygame.mouse.get_pos()):
            return hoverpicture
        return picture 
            

    
        
        