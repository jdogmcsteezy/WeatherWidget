
# -*- coding: utf-8 -*-
from urllib.request import urlopen, URLError
from pygame import Surface, time, font, image, transform, SRCALPHA
from os import path
import json
import sys
import time
import unicodedata

def aspect_scale(img, bx, by):
        # """ Scales 'img' to fit into box bx/by.
        # This method will retain the original image's aspect ratio """
        ix,iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by/float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return transform.smoothscale(img, (int(sx),int(sy)))

class WeatherWidget(Surface):
    def __init__(self, width, height, bgColor):
        Surface.__init__(self, (width, height))
        font.init()
        self.width = width
        self.height = height
        self.bgColor = bgColor
        self.dir_path = path.dirname(path.realpath(__file__))
        self.assets_path = path.join(self.dir_path, 'Assets')
        self.fonts_path = path.join(self.assets_path, 'Fonts')
        self.fontFile = ('OpenSans-Regular.ttf', int(height * (35/125)))
        self.cloudFile = 'Cloud.png'
        self.rainFile = 'Rain.png'
        self.sunFile = 'Sun.png'
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.fill(bgColor)
        self.w_list = []
        self.Update()

    def addText(self):
        self.textFont = font.Font(path.join(self.fonts_path, self.fontFile[0]), self.fontFile[1])
        textSurface = self.textFont.render((str(self.w_list[1]) + u'\u00b0' + 'F'), True, (242,242,242))
        return textSurface

    def addImage(self):
        my_string = self.w_list[2]
        sun = ["sun", "Sun", "Sunny", "sunny", "Clear", "clear"]
        rain = ["Rain", "rain", "Raining", "raining", "drizzle", "Drizzle", "showers", "Showers", "Hail"]
        cloud = ["Cloudy", "cloudy", "overcast", "Overcast", "Clouds", "clouds", "gray", "Gray", "grey", "Grey", "Fog"]
        for i in my_string.split():
            if i in cloud:
                cloudimage = image.load(path.join(self.assets_path, self.cloudFile))
                return cloudimage
            elif i in rain:
                rainimage = image.load(path.join(self.assets_path, self.rainFile))
                return rainimage
            elif i in sun:
                sunimage = image.load(path.join(self.assets_path, self.sunFile))
                return sunimage
            else:
                #self.screen.blit(sunimage, (845, 0))
                continue

    def weatherOut(self):
        try:
            f = urlopen('http://api.wunderground.com/api/4e96f64459824b58/geolookup/conditions/q/CA/Oroville.json')
        except URLError as e:
            print('URLError = ' + str(e.reason))
            return
        self.w_list = []
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

    def Update(self):
        self.weatherOut()
        if not self.w_list:
            return self
        textSurface = self.addText()
        imageSurface = self.addImage()
        imageSurface = aspect_scale(imageSurface, self.width - textSurface.get_rect().width + 5, self.height)
        self.fill(self.bgColor)
        self.blit(textSurface, (0,0))
        self.blit(imageSurface, (self.width - imageSurface.get_rect().width - 5, 0))
        self.convert()
        return self
