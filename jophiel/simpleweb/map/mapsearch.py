#coding=utf8
import httplib, urllib
from xml.dom.minidom import parse, parseString
import json
#coding=utf8
from search.searchengine import SharedService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class PoiSearch:
    COUNT_NODE = "count"
    SEARCHTIME_NODE = "searchtime"
    PINYIN_NODE = "pinyin"
    POI_NODE = "poi" 
    
    PAGE_SIZE = 8
    
    def __init__(self):
        self.count = '0'
        self.searchtime = '0'
        self.suggestions = []
        self.searchresult = []
        self.jsonresult=[]
        self.earthshow = []
        self.address='127.0.0.1'
        self.port=9090
        self.transport = TSocket.TSocket(self.address,self.port)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = SharedService.Client(self.protocol)
        self.transport.open()

    def get_count(self):
        return self.count
    
    def get_searchtime(self):
        time = float(self.searchtime)
        return str(time)
    
    def get_suggestions(self):
        return self.suggestions
    def filter_result(self, input):
        return input
    
        
    def get_searchresult(self):
        return self.searchresult
        
    def get_poi_info(self, city_code, params, page):
        #print "city_code:",city_code,params
        result = self.client.SearchCityTerm(city_code, params.encode("utf-8"), (page - 1) * PoiSearch.PAGE_SIZE, PoiSearch.PAGE_SIZE)
        return result
    
    def search_poi(self, city_code, keyword="", batch="", data_type=["mpoi"], query_type="tquery", **kwd):
        #print keyword
        data = self.get_poi_info(city_code, keyword, int(batch))
        self.parse_response(data)
        
    def search_around(self, keyword, lat, lng, distance, citycode):
        result = self.client.SearchArround(keyword.encode("utf-8"), lng, lat, distance)     
        self.parse_response(result)
        
    def search_detail(self, city_code, pguid):        
        result = self.client.SearchPoi(pguid)
        self.parse_response(result)
            
    def parse_response(self, resp):
        self.searchtime = resp.search_time
        self.count = resp.matches
        self.searchresult=[]
        self.jsonresult=[]
        for item in resp.values:
            value = json.loads(item.value)
            filter = self.filter_result(value)
            self.searchresult.append(filter)
            self.jsonresult.append(json.dumps(value,ensure_ascii=False).replace("\\n","<br/>"))
            
    def close(self):
        self.transport.close()
     
    
def main():
    poi = PoiSearch()
    poi.search_poi("021", "海淀", '', "10")
    
    print poi.count
    print poi.searchtime
    print poi.suggestions
    for search in poi.searchresult:
        print search
            
