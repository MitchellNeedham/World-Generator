import pygame
import pygameMenu
import csv
import pyperclip
import sys
import os

COLOR_BLACK = (0, 0, 0)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_LIGHT_GRAY = (175, 175, 175)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 125
FONT_SIZE_MAIN = 72



class main_menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_size = screen.get_size()

        self.play_button = menu_button(COLOR_DARK_GRAY, (self.screen_size[0]-BUTTON_WIDTH)/2, \
            (self.screen_size[1]-BUTTON_HEIGHT)/2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT, FONT_SIZE_MAIN, 'Play')
        self.quit_button = menu_button(COLOR_DARK_GRAY, (self.screen_size[0]-BUTTON_WIDTH)/2, \
            (self.screen_size[1]-BUTTON_HEIGHT)/2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT, FONT_SIZE_MAIN, 'Quit')
        

    def display(self):
        
        self.play_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if self.play_button.isOver(mouse_position):
                    self.play_button.color = COLOR_LIGHT_GRAY
                else:
                    self.play_button.color = COLOR_DARK_GRAY

                if self.quit_button.isOver(mouse_position):
                    self.quit_button.color = COLOR_LIGHT_GRAY
                else:
                    self.quit_button.color = COLOR_DARK_GRAY

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.isOver(mouse_position):
                    return 1
                if self.quit_button.isOver(mouse_position):
                    return 0
        return None



class menu_button:
    def __init__(self, color, x, y, width, height, font_size, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0)
        #self.screen_size = screen.get_size()
        #self.width = self.screen_size[0]
        #self.height = self.screen_size[1]

        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Arial', self.font_size)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False





    

