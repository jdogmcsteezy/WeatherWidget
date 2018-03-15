from urllib.request import urlopen
from pygame import Surface, time, font, image, transform, SRCALPHA
from os import path
import json
import sys
import time

class WeatherWidget(Surface):
    def __init__(self, width, height):
        Surface.__init__(self, (width, height))
        font.init()
        self.dir_path = path.dirname(path.realpath(__file__))
        self.assets_path = path.join(self.dir_path, 'Assets')
        self.fonts_path = path.join(self.assets_path, 'Fonts')
        self.fontFile = ('OpenSans-Regular.ttf', 20)
        self.cloudFile = 'Cloud.png'
        self.rainFile = 'Rain.png'
        self.sunFile = 'Sun.png'
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.fill(self.black)
        self.w_list = []
        self.weatherOut()
        self.addText()
        self.addImage()
    def addRect(self):
        self.rect = pygame.draw.rect(self.screen, (black), (0, 0, 250, 150), 2)
    def addText(self):
        self.textFont = font.Font(path.join(self.fonts_path, self.fontFile[0]), self.fontFile[1])
        #self.blit(self.textFont.render(self.w_list[0], True, (255,0,0)), (0,100))
        self.blit(self.textFont.render((str(self.w_list[1]) + ' F'), True, (255,0,0)), (0,0))
    def addImage(self):
        my_string = self.w_list[2]
        sun = ["sun", "Sun", "Sunny", "sunny", "Clear", "clear"]
        rain = ["Rain", "rain", "Raining", "raining", "drizzle", "Drizzle", "showers", "Showers"]
        cloud = ["Cloudy", "cloudy", "overcast", "Overcast", "Clouds", "clouds", "gray", "Gray", "grey", "Grey"]
        for i in my_string.split():
            if i in cloud:
                cloudimage = image.load(path.join(self.assets_path, self.cloudFile))
                self.blit(cloudimage, (100, 0))
            elif i in rain:
                rainimage = image.load(path.join(self.assets_path, self.rainFile))
                self.blit(rainimage, (100, 0))
            elif i in sun:
                sunimage = image.load(path.join(self.assets_path, self.sunFile))
                self.blit(sunimage, (100, 0))
            else:
                #self.screen.blit(sunimage, (845, 0))
                break
    def weatherOut(self):
        self.w_list = []
        f = urlopen('http://api.wunderground.com/api/4e96f64459824b58/geolookup/conditions/q/CA/Oroville.json')
        json_string = f.read()
        parsed_json = json.loads(json_string.decode())
        # location is list 0
        cityweather = parsed_json['location']['city']
        self.w_list.append(cityweather)
        # temp_f is list 1
        citytemp = parsed_json['current_observation']['temp_f']
        citytemp = citytemp / 1
        self.w_list.append(citytemp)
        # weather condition is list 2
        weatherweather = parsed_json['current_observation']['weather']
        self.w_list.append(weatherweather)