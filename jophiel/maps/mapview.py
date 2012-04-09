#coding=utf-8

import time
import math
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import  settings

from .cityinfo import CityInfo
from .searchform import IndexForm,DetailForm,SearchForm

try:
    from .mapsearch import PoiSearch
    search = PoiSearch()
except:
    pass

def template(request,name, **kwd):
    """Renders a template and wraps it as an http response"""
    #templ = loader.get_template(name)
    #page  = templ.render( Context(kwd) )
    #print kwd
    c = RequestContext(request,kwd)
    return render_to_response(name, context_instance=c)

def param(request, name, default=''):
    """Shortcut for getting a parameter value"""
    return request.REQUEST.get(name, default).strip()


PAGE_SHOW_COUNT = 6
def calculate_page(page_cur, page_size, total):
    page_pre = ""
    page_next = ""
    page_arr = []
    
    page_total = int(math.ceil(total / page_size))
    if page_cur > page_total:
        page_cur = 1
    
    if page_cur > 1:
        page_pre = page_cur - 1
    
    if page_cur < page_total :
        page_next = page_cur + 1
    
    page_tmp = int(math.floor((page_cur - 1) / PAGE_SHOW_COUNT));
    page_begin = page_tmp * PAGE_SHOW_COUNT + 1;
    page_end = min((page_tmp + 1) * PAGE_SHOW_COUNT, page_total);
    
    if page_pre != "":
        page_arr.append({"key":"上一页", "value": page_pre});
    
    for i in range(page_begin, page_end + 1):
        page_arr.append({"key":i, "value": i})
    
    if page_next != "":
        page_arr.append({"key":"下一页", "value":page_next})
    
    if len(page_arr) == 1:
        page_arr = [];
    return (page_arr, page_pre, page_next)
#
# normally one would read and write the text from some sort of storage
# for this example we'll use a global variable to hold the content
#
def map(request):
    fname = "maps/index.html"
    form = IndexForm()
    
    if request.method == 'GET':
        form = IndexForm(request.GET, auto_id=False)
        if form.is_valid():
            cd = form.cleaned_data
                
            cityname = cd["cityname"]
            cinfo = CityInfo(cityname)
            citycode = cinfo.get_citycode(cityname)
            centpoint = cinfo.get_cent_point(citycode)
            
            #print cityname+citycode
            
            return template(request,fname,
                            form=form,
                            cityname=cd["cityname"],
                            init_x=centpoint["x"],
                            init_y=centpoint["y"],
                            commoncity=cinfo.get_common_city()
                            )

def index(request):
    fname = "maps/index.html"
    form = IndexForm()
    cityname = u'北京'
    
    cinfo = CityInfo(cityname)
    citycode = cinfo.get_citycode()
    centpoint = cinfo.get_cent_point()
    
    return template(request,fname,
                    form=form,
                    cityname=cityname,
                    init_x=centpoint["x"],
                    init_y=centpoint["y"],
                    commoncity=cinfo.get_common_city()
                )
    
def cityinfo(request):pass
    

def main(request):
    fname = "maps/main.html"
    return template(request,fname)

def detail(request):
    fname = "maps/detail.html"
    if request.method == 'GET':
        form = DetailForm(request.GET, auto_id=False)
        if form.is_valid():
            cd = form.cleaned_data
            cinfo = CityInfo(cd["cityname"])
            citycode = cinfo.get_citycode()
            pguid = cd["pguid"]
            search.search_detail(citycode, pguid)
            centpoint = cinfo.get_cent_point()
            
            return template(request,fname,
                            form=form,
                            cityname=cd["cityname"],
                            searchresult=search.get_searchresult(),
                            init_x=centpoint["x"],
                            init_y=centpoint["y"],
                            commoncity=cinfo.get_common_city()
                            )

def list(request):
    fname = "maps/list.html"
    if request.method == 'GET':
        form = SearchForm(request.GET, auto_id=False)
        if form.is_valid():
            cd = form.cleaned_data
            cinfo = CityInfo(cd["cityname"])
            citycode = cinfo.get_citycode()
            keyword = cd["kw"]
            page = cd["page"]
            searchtype = cd["enginechoose"]
            if not page:
                page = "1"
            lat = cd["lat"]
            lng = cd["lng"]
            distance = cd["distance"]
            searchtype = cd["searchtype"]

            if searchtype and searchtype == "around":
                centpoint = cinfo.get_cent_point() 
                search.search_around(keyword, lat, lng, distance, citycode)
            else:
                centpoint = cinfo.get_cent_point()         
                search.search_poi(citycode, keyword, page, data_type=searchtype)
            page_arr, page_pre, page_next = calculate_page(int(page), search.PAGE_SIZE, search.get_count())
            #print cinfo.get_common_city()
            return template(request,fname,
                        form=form,
                        cityname=cd["cityname"],
                        keyword=keyword,
                        suggestions=search.get_suggestions(),
                        count=search.get_count(),
                        searchtime=search.get_searchtime(),
                        searchresult=search.get_searchresult(),
                        jsonresult=search.jsonresult,
                        pagearr=page_arr,
                        pagepre=page_pre,
                        pagenext=page_next,
                        pagecur=page,
                        init_x=centpoint["x"],
                        init_y=centpoint["y"],
                        commoncity=cinfo.get_common_city()
                    )
        else:
            fname = "maps/index.html"
            cityname = request.GET["cityname"] or u"北京"
            cinfo = CityInfo(cityname)
            citycode = cinfo.get_citycode()
            centpoint = cinfo.get_cent_point()  
            return template(request,fname,
                            form=form,
                            init_x=centpoint["x"],
                            init_y=centpoint["y"],
                            commoncity=cinfo.get_common_city()
                            )
