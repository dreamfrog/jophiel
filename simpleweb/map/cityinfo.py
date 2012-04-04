#coding=utf-8
import settings

comm_city =["全国","北京","上海","广州","天津","重庆",
    "深圳","苏州","杭州","佛山","成都",
    "东莞","西安","武汉","青岛","温州",
    "沈阳","宁波","长沙 ","大连"
    ]
import os
import json
print os.listdir(".")
file=open(settings.CITY_INFO,"r")
value=file.read()
mapabc_city = json.loads(value)
file.close()

#print mapabc_city

file=open(settings.PRO_CITY,"r")
value=file.read()
prov_city = json.loads(value)
file.close()

file=open(settings.ALPHA_CITY,"r")
value=file.read()
alpha_city = json.loads(value)
file.close()


class city_info:
    def __init__(self,cityname):
        self.name=cityname
        self.city_map=None
        #print "name: ",self.name
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
        return mapabc_city[u"北京"][u"geospatial"]
    
    def get_common_city(self):
        return comm_city
    
if __name__=="__main__":
    cinfo=city_info()
    print cinfo.get_citycode("北京")
