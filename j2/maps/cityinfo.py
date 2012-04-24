#coding=utf-8
from . import settings

comm_city =["全国","北京","上海","广州","天津","重庆",
    "深圳","苏州","杭州","佛山","成都",
    "东莞","西安","武汉","青岛","温州",
    "沈阳","宁波","长沙 ","大连"
    ]
import os
import json

class CityInfo:
    mapabc_city = None
    prov_city = None
    alpha_city = None
    
    @classmethod
    def get_mapabc_city(cls):
        if not cls.mapabc_city:
            with open(settings.CITY_INFO,"r") as file :
                cls.mapabc_city = json.loads(file.read())
        return cls.mapabc_city
    
    @classmethod
    def get_prov_city(cls):
        if not cls.prov_city:
            with open(settings.PRO_CITY,"r") as file:
                cls.prov_city = json.loads(file.read())
        return cls.prov_city

    @classmethod
    def get_alpha_city(cls):
        if not cls.alpha_city:
            with open(settings.ALPHA_CITY,"r") as file:
                cls.alpha_city = json.loads(file.read())
        return cls.alpha_city
                                       
    
    def __init__(self,cityname):
        self.name=cityname
        self.city_map=None
        #print "name: ",self.name
        mapabc_city = self.get_mapabc_city()
        if mapabc_city.has_key(self.name) :
            self.city_map=mapabc_city[self.name]
        
    def get_citycode(self):
        #name=cityname
        if self.city_map:
            print self.city_map
            return self.city_map[u"adcode"]
        return ""

    def get_cent_point(self):
        if self.city_map:
            return self.city_map[u"geospatial"]
        mapabc_city = self.get_mapabc_city()
        return mapabc_city[u"北京"][u"geospatial"]
    
    def get_common_city(self):
        return comm_city


