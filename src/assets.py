import pygame as pg
import os
from src.settings import *

class LazyLoader:
    def __init__(self):
        self.game_folder = os.path.dirname(os.path.dirname(__file__))
        self.img_folder = os.path.join(self.game_folder, SPRITE_FOLDER)
        self.cache = {}
    
    def get_image(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        
        path = os.path.join(self.img_folder, filename)
        
        try:
            image = pg.image.load(path).convert_alpha()
            self.cache[filename] = image
            return image
        
        except pg.error as e:
            print(f"Could not load image {filename}: {e}")
            surface = pg.Surface((TILESIZE, TILESIZE))
            surface.fill(LIGHTGREY)
            return surface
            
class SoundLoader:
    def __init__(self):
        self.game_folder = os.path.dirname(os.path.dirname(__file__))
        self.sound_folder = os.path.join(self.game_folder, SOUND_FOLDER)
        self.cache = {}

    def get_sound(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        
        path = os.path.join(self.sound_folder, filename)

        try:
            sound = pg.mixer.Sound(path)
            self.cache[filename] = sound
            return sound
        
        except pg.error as e:
            print(f"Could not load sound {filename}: {e}")
            return None
        
    def play_sound(self, filename):
        sound = self.get_sound(filename)
        if sound:
            sound.play()

class SoundManager:
    def __init__(self):
        pg.mixer.init()
        self.sounds = {}

    def play_sound(self, sound_file):
        if sound_file not in self.sounds:
            try:
                full_path = os.path.join(SOUND_FOLDER, sound_file)
                self.sounds[sound_file] = pg.mixer.Sound(full_path)
            except:
                print(f"Could not load sound: {sound_file}")
                return
        self.sounds[sound_file].play()