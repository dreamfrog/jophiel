var mapList={};
var s,b1,b2,r1,r2;
var c_s,c_b,c_r1,c_r2;
var area;//查询周边
var area_range;
var dataNum;
var differentiate_s = 0;//区别关键字查询和周边查询
var page,page_now,page_allnum,points;
var sis,sp,start,end,bus,route,lszb,sis1,sis2;
var search_x,search_y,search_pn,point_sp;//通过x,y查询周边

var bus_fettle="";//公交查询状态

var bus_way=0;//公交查询方式(0,1,2,3,4)
var route_way=0;//驾车查询方式(0,1,2)

function search_lc(ch){
	var ctv =$F('citykey') ;
    var sear =$F('searchkey') ;
	var check = inputif(ctv,sear);
	ctv = encodeURI(ctv);
	sear = encodeURI(sear);
	if(check=="N"){
		alert("请输入完整的查询条件      ");
	}else{
		if(ch=="0"){//index查询
			var url = 'c='+ctv+'&s='+sear+'&page=lc';
			location.href='/search.html?'+url;
		}else{//search页查询
			s_ls();
			logingin('1');
			var city =$F('citykey') ;
			
			s = $F('searchkey') ;
			$('b1').value=s;
			$('r1').value=s;
			document.title=city+'  '+s+' - MapABC地图';

			var str = search_type(city).split(",");
			if(str.length==4){//=4是关键字查询
				$('b1').value=s;
				$('r1').value=s;
				c_s = getcityname(city,"code"); 
				dataNum = $F('showDatanum');
				search_lc_map();
			}
			if(str.length==5){//=5是周边查询
				area = str[4];
				$('b1').value=s;
				$('r1').value=s;
				c_s = str[1];
				dataNum = $F('showDatanum');
				area_range = $F('showDataarea');
				if(area_range=="" || area_range==null){
					area_range = 3000;
				}
				search_zb_map();
			}		
		}
	}
}
//判断输入条件是否正确
function inputif(ctv,sear){
	var check = "Y";
    if(ctv==null || ctv=="" || ctv==" "){ctv="北京";check = "N";}else{
		var city_c = search_type(ctv);
		if(city_c==null){check = "N";}
	}
    if(sear==null || sear=="" || sear==" " )
    {
    	sear="酒店";check = "N";
    }
	return check;
}
function search_bus(ch){
	
	var bus1 =$F('b1') ;
    var bus2 =$F('b2') ;
    var bc =$F('citylistb') ;
    var che = "以下错误造成公交换乘查询失败         \n\n";
    var i = 1 ;
    if(bus1==""){
        che += i + "．起点不能为空\n" ;
        i = i + 1 ;
    }
    if(bus2==""){
        che += i + "．终点不能为空\n" ;
        i = i + 1 ;
    }
    if(bc==""){
        che += i + "．请选择您要查询的城市\n" ;
        i = i + 1 ;
    }
    if(i==1){
		bus1 = encodeURI(bus1);
		bus2 = encodeURI(bus2);
		if(ch=="0"){//INDEX为‘0’时为刷新页面查询，带url
			location.href='/search.html?cc='+bc+'&b1='+bus1+'&b2='+bus2+'&page=b';
		}else if(ch=="5"){//简版搜索(二级域名)
			location.href='http://www.mapabc.com/search.html?cc='+bc+'&b1='+bus1+'&b2='+bus2+'&page=b';
		}else{//search查询			
			logingin('1');
			nn_b=1;
			s_b();
			c_b = $F('citylistb') ;
			b1 = $F('b1') ;
			b2 = $F('b2') ;
			$('searchkey').value=b1;
			$('r1').value=b1;
			document.title=b1+' - '+b2+' - '+getcityname(c_b,"name")+'MapABC公交地图查询  ';	
			if($('default_bus').style.display==""){
				var bus_s_types =  document.getElementsByName("bus_s_type1").length;
				for(var i=0;i<bus_s_types;i++){
					if( document.getElementsByName("bus_s_type1")[i].checked){
						bus_way=i;
					}
				}
			}else{
				bus_way=0;
			}
				
			search_bus_map();
		}
		
    }else{
        alert(che);
    }
}
function search_route(ch){
	var route1 =$F('r1') ;
    var route2 =$F('r2') ;
    var routec1 =$F('citylistr') ;
	var routec2 =$F('citylistr2') ;
    var che = "以下错误造成驾车路线查询失败         \n\n";
    var i = 1 ;
    if(route1==""){
        che += i + "．起点不能为空\n" ;
        i++;
    }
    if(route2==""){
        che += i + "．终点不能为空\n" ;
        i++;
    }
    if(routec1==""){
        che += i + "．请选择起点城市\n" ;
        i++;
    }
	if(routec2==""){
        che += i + "．请选择终点城市\n" ;
        i++;
    }
    if(i==1){
		route1 = encodeURI(route1);
		route2 = encodeURI(route2);
		if(ch=="0"){//INDEX为‘0’时为刷新页面查询，带url
			location.href='/search.html?c1='+routec1+'&c2='+routec2+'&r1='+route1+'&r2='+route2+'&page=r';
		}else{
			//查询方法
			logingin('1');
			nn_r = 1;
			s_r();
			r1 = $F('r1') ;
			r2 = $F('r2') ;
			c_r1 =$F('citylistr') ;
			c_r2 = $F('citylistr2') ;
			document.title=r1+' - '+getcityname(c_r1,"name")+' - '+r2+' - '+getcityname(c_r2,"name")+'MapABC驾车地图查询  ';	
		
			$('b1').value = r1;
			$('b2').value = r2;
			$('searchkey').value = r1;
			if($('default_route').style.display==""){
				var route_s_types = document.getElementsByName("route_s_type1").length;
				for(var i=0;i<route_s_types;i++){
					if( document.getElementsByName("route_s_type1")[i].checked){
						route_way=i;
					}
				}
			}else{
				route_way=0;
			}
			search_route_map();
		}
    }else{
        alert(che);
    }
}
function search_lc_map(){
	differentiate_s=0;
	if(mapList[''+c_s+'_'+s+'_'+page_now+'_'+dataNum]==null){
			page = 1;
			page_now = 1
			page_allnum = 0;
			points=null ;
			sis = new MSISSearch();
			sp = new MSearchPointPara();
			sis.setSISCallbackFunction(myfuncb);
			sp.setCitycode(c_s);
			sp.setKeyword(s);
			sp.setNumber(dataNum); 
			sp. setBatch(page); 
			sis.searchByKeyword (sp); 	
		}else{
			history_bd = 0;
			write_ls("key");
		}
}
function myfuncb(data){
	mapList[''+c_s+'_'+s+'_'+page_now+'_'+dataNum]=eval('(data)');
	if(data.message!='ok'){
		logingin('0');
		$('result_search').style.display="";
		$('result_search').innerHTML = "<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;<b>服务器异常！请重新尝试！</b><br />&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;如果您刷新页后仍无法显示结果，请过几分钟后再次尝试或者与我们的服务人员联系。<br />&nbsp;&nbsp;&nbsp;Email：service@mapabc.com <br />&nbsp;&nbsp;&nbsp;电话：400 810 0080</div>";
	}else{
		write_ls("key");
	}
}	
function search_zb_map(){
	differentiate_s=1;
	if(mapList[''+c_s+area+'_'+s+'_'+page_now+'_'+area_range+'_'+dataNum]==null){
			page = 1;
			page_now = 1
			page_allnum = 0;
			points=null ;
			sis = new MSISSearch();
			lszb = new MSearchPointPara();
			lszb.setCenterKeyword(area);
			lszb.setCitycode(c_s);
			lszb.setKeyword(s);
			lszb.setNumber(dataNum); 
			lszb.setRange(area_range);
			lszb. setBatch(page); 
			sis.setSISCallbackFunction(myfunczb);
			sis.localSearchByKeyword (lszb); 
		}else{
			history_bd = 0;
			write_ls("zb");
		}
}
function myfunczb(data){
	mapList[''+c_s+area+'_'+s+'_'+page_now+'_'+area_range+'_'+dataNum]=eval('(data)');
	if(data.message!='ok'){
		logingin('0');
		$('result_search').style.display="";
		$('result_search').innerHTML = "<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;<b>服务器异常！请重新尝试！</b><br />&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;如果您刷新页后仍无法显示结果，请过几分钟后再次尝试或者与我们的服务人员联系。<br />&nbsp;&nbsp;&nbsp;Email：service@mapabc.com <br />&nbsp;&nbsp;&nbsp;电话：400 810 0080</div>";
	}else{
		write_ls("zb");
	}	
}	
var nn_b = 1;//判断起点与终点
var start_x="",start_y="",start_name="",start_type="",start_address="",start_tel="",start_pid="",start_citycode="",start_cityname="";
var end_x="",end_y="",end_name="",end_type="",end_address="",end_tel="",end_pid="",end_citycode="",end_cityname="";
var xy_array ;
var xy_hc_array="";
var start_temp="",end_temp="";
var bus_NN=0;//判断是否查询过.	
function search_bus_map(){
	bus_fettle = "1";//公交查询状态(公交查询)
	document.getElementsByName("gjs")[0].checked=true;

bus_NN=0;
	if(mapList[''+c_b+'_'+b1+'_1'] != null){
		var rs = mapList[''+c_b+'_'+b1+'_1'];
		if(rs.count!=0){
		start_x = rs.poilist[0].x;
		start_y = rs.poilist[0].y;	
		}
	}
	if(mapList[''+c_b+'_'+b2+'_1'] != null){
		var rs1 = mapList[''+c_b+'_'+b2+'_1'];
		if(rs1.count!=0){
		end_x = rs1.poilist[0].x;
		end_y = rs1.poilist[0].y;
		}
	}	
	
	sis1 = new MSISSearch();
	start = new MSearchPointPara();
	end = new MSearchPointPara();
	bus = new MSearchRoutPara();
	sis1.setSISCallbackFunction(myfunc1);
	
	if(mapList[''+c_b+'_'+b1+'_1']==null){
		nn_b=1;
		start.setCitycode(c_b);
		start.setKeyword(b1);
		start.setNumber(20); 
		start. setBatch(1); 
		sis1.searchByKeyword (start); 
	}
	else if(mapList[''+c_b+'_'+b2+'_1']==null){
		nn_b=0;
		end.setCitycode(c_b);
		end.setKeyword(b2);
		end.setNumber(20); 
		end. setBatch(1); 
		sis1.searchByKeyword(end);
	}
	else if(mapList[''+c_b+'_'+b1+'_'+b2+'_'+bus_NN+'_'+bus_way]==null){
		nn_b=2;
		if(start_x == null || start_x=="" || start_x==" "||end_x ==null || end_x == "" || end_x==" "){
				write_bus();
			}else{
				//alert(start_x);
				bus.setStartXY(start_x,start_y);
			    bus.setEndXY(end_x,end_y);
				bus.setCitycode(c_b);//调用MSearchRoutPara的citycode方法
				bus.setRouteType(bus_way);
				bus.setType("bus");//路径查询
				sis1.searchBusAndDrive(bus);//调用MSearchRoutPara的searchBusAndDrive方法
			}
	}
	else{
	//写
	history_bus=0;
	write_bus();
	}
}
function myfunc1(data){
	if(data.message!='ok'){
		logingin('0');
		$('result_bus').style.display="";
		$('result_bus').innerHTML = "<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;<b>服务器异常！请重新尝试！</b><br />&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;如果您刷新页后仍无法显示结果，请过几分钟后再次尝试或者与我们的服务人员联系。<br />&nbsp;&nbsp;&nbsp;Email：service@mapabc.com <br />&nbsp;&nbsp;&nbsp;电话：400 810 0080</div>";
	}else{
		if(nn_b==2){
			mapList[''+c_b+'_'+b1+'_'+b2+'_'+bus_NN+'_'+bus_way]=eval('(data)');
			write_bus();
		}else{
			if(nn_b==1){
				mapList[''+c_b+'_'+b1+'_1']=eval('(data)');
				var rs = mapList[''+c_b+'_'+b1+'_1'];
				if(rs.count!=0){
				start_x = rs.poilist[0].x;
				start_y = rs.poilist[0].y;
				}
			}
			if(nn_b==0){
				mapList[''+c_b+'_'+b2+'_1']=eval('(data)');
				var rs = mapList[''+c_b+'_'+b2+'_1'];
				if(rs.count!=0){
				end_x = rs.poilist[0].x;
				end_y = rs.poilist[0].y;
				}
			}
		start_end_bus();
		}
	}
}	
function start_end_bus(){
	if(nn_b==1){
		nn_b=0;
			if(mapList[''+c_b+'_'+b2+'_1']==null){
				end.setCitycode(c_b);
				end.setKeyword(b2);
				end.setNumber(20); 
				end. setPageSum(1); 
				end. setBatch(1); 
				sis1.searchByKeyword(end);
			}else{
				search_bus_map();
			}	
	}else{
		nn_b=2;
		if(mapList[''+c_b+'_'+b1+'_'+b2+'_'+bus_NN+'_'+bus_way]==null){
			if(start_x == null || start_x=="" || start_x==" "||end_x ==null || end_x == "" || end_x==" "){
				write_bus();
			}else{
				bus.setStartXY(start_x,start_y);
				bus.setEndXY(end_x,end_y);
				bus.setCitycode(c_b);
				bus.setRouteType(bus_way);
				bus.setType("bus");
				sis1.searchBusAndDrive(bus);
			}
		}else{
				search_bus_map();
			}	
	}
}

//驾车
var nn_r = 1;//判断起点与终点
var r_start_x="",r_start_y="",r_start_name="",r_start_type="",r_start_address="",r_start_tel="",r_start_pid="",r_start_citycode="",r_start_cityname="";
var r_end_x="",r_end_y="",r_end_name="",r_end_type="",r_end_address="",r_end_tel="",r_end_pid="",r_end_citycode="",r_end_cityname="";
var r_xy_array ;
var r_xy_hc_array="";
var r_start_temp="",r_end_temp="";
var route_NN=0;//判断是否查询过.

function search_route_map(){
	route_NN=0;
	if(mapList[''+c_r1+'_'+r1+'_1'] != null){
		var rs = mapList[''+c_r1+'_'+r1+'_1'];
		if(rs.count!=0){
		r_start_x = rs.poilist[0].x;
		r_start_y = rs.poilist[0].y;
		}
	}
	if(mapList[''+c_r2+'_'+r2+'_1'] != null){
		var rs1 = mapList[''+c_r2+'_'+r2+'_1'];
		if(rs1.count!=0){
		r_end_x = rs1.poilist[0].x;
		r_end_y = rs1.poilist[0].y;
		}
	}
	sis2 = new MSISSearch();
	start = new MSearchPointPara();
	end = new MSearchPointPara();
	route = new MSearchRoutPara();
	sis2.setSISCallbackFunction(myfunc2);
	
	if(mapList[''+c_r1+'_'+r1+'_1']==null){
		nn_r=1;
		start.setCitycode(c_r1);
		start.setKeyword(r1);
		start.setNumber(20); 
		start. setPageSum(1);
		start. setBatch(1); 
		sis2.searchByKeyword (start); 
	}
	else if(mapList[''+c_r2+'_'+r2+'_1']==null){
		nn_r=0;
		end.setCitycode(c_r2);
		end.setKeyword(r2);
		end.setNumber(20); 
		end. setPageSum(1); 
		end. setBatch(1); 
		sis2.searchByKeyword(end);
	}
	else if(mapList[''+c_r1+'_'+c_r2+'_'+r1+'_'+r2+'_'+route_NN+'_'+route_way]==null){
		nn_r=2;
		if(r_start_x == null || r_start_x=="" || r_start_x==" "||r_end_x ==null || r_end_x == "" || r_end_x==" "){
				write_route();
			}else{
				route.setStartXY(r_start_x,r_start_y);
				route.setEndXY(r_end_x,r_end_y);
				route.setCitycode(c_r1);//调用MSearchRoutPara的citycode方法
				route.setRouteType(route_way);
				route.setType("drive");//路径查询
				sis2.searchBusAndDrive(route);//调用MSearchRoutPara的searchBusAndDrive方法
			}
	}
	else{
	//写
	 history_route=0;
	write_route();
	}		
}
function myfunc2(data){
	if(data.message!='ok'){
		logingin('0');
		$('result_route').style.display="";
		$('result_route').innerHTML = "<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;<b>服务器异常！请重新尝试！</b><br />&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;如果您刷新页后仍无法显示结果，请过几分钟后再次尝试或者与我们的服务人员联系。<br />&nbsp;&nbsp;&nbsp;Email：service@mapabc.com <br />&nbsp;&nbsp;&nbsp;电话：400 810 0080</div>";
	}else{
		if(nn_r==2){  
			mapList[''+c_r1+'_'+c_r2+'_'+r1+'_'+r2+'_'+route_NN+'_'+route_way]=eval('(data)');
			//写
			write_route();
		}else{
			if(nn_r==1){
				mapList[''+c_r1+'_'+r1+'_1']=eval('(data)');
				var rs = mapList[''+c_r1+'_'+r1+'_1'];
				if(rs.count!=0){
				r_start_x = rs.poilist[0].x;
				r_start_y = rs.poilist[0].y;
				}
				
			}
			if(nn_r==0){
				mapList[''+c_r2+'_'+r2+'_1']=eval('(data)');
				var rs = mapList[''+c_r2+'_'+r2+'_1'];
				if(rs.count!=0){
				r_end_x = rs.poilist[0].x;
				r_end_y = rs.poilist[0].y;
				}

			}
		start_end_route();
		}
	}
}
function start_end_route(){
	if(nn_r==1){
		nn_r=0;
			if(mapList[''+c_r1+'_'+r1+'_1']==null){
				end.setCitycode(c_r1);
				end.setKeyword(r2);
				end.setNumber(20); 
				end. setPageSum(1); 
				end. setBatch(1); 
				sis2.searchByKeyword(end);
			}else{
				search_route_map();
			}	
	}else{
		nn_r=2;
		if(mapList[''+c_r1+'_'+c_r2+'_'+r1+'_'+r2+'_'+route_NN+'_'+route_way]==null){
			if(r_start_x == null || r_start_x=="" || r_start_x==" "||r_end_x ==null || r_end_x == "" || r_end_x==" "){
				write_route();
			}else{
				route.setStartXY(r_start_x,r_start_y);
				route.setEndXY(r_end_x,r_end_y);
				route.setCitycode(c_r1);//调用MSearchRoutPara的citycode方法
				route.setRouteType(route_way);
				route.setType("drive");//路径查询
				sis2.searchBusAndDrive(route);//调用MSearchRoutPara的searchBusAndDrive方法
			}
		}else{
				search_route_map();
			}	
	}
}

function page_all(page_url,index){//page_all('北京,邮政局','lc')
		logingin('1');
		if(index=="lc"){
			var str1 = page_url.split(",");
			s = str1[1];
			dataNum = $F('showDatanum');
			document.title=str1[0]+'  '+s+' - MapABC地图';
			
			var str = search_type(str1[0]).split(",");
			if(str.length==4){//=4是关键字查询		
				$('b1').value=s;
				$('r1').value=s;
				c_s = getcityname(str[0],"code");
				search_lc_map();
			}
			if(str.length==5){//=5是周边查询
				area = str[4];
				$('b1').value=s;
				$('r1').value=s;
				c_s = str[1];
				area_range = 3000;
				search_zb_map();
			}			
		}
		if(index=="b"){//page_all('021,浦东国际机场,东方明珠广播电视塔','b')
			var bus_str = page_url.split(",");
			c_b = bus_str[0];
			b1 = bus_str[1] ;
			b2 = bus_str[2] ;

			$('searchkey').value=b1;
			$('r1').value=b1;

			document.title=b1+' - '+b2+' - 北京公交地图  ';	
			search_bus_map();
		}
		if(index=="r"){//page_all('010,010,西单,颐和园','r')
			var route_str = page_url.split(",");
			nn_r = 1;
			s_r();
			r1 = route_str[2];
			r2 = route_str[3];
			c_r1 =route_str[0];
			c_r2 = route_str[1];
		
			$('b1').value = r1;
			$('b2').value = r2;
			$('searchkey').value = r1;
			document.title=getcityname(c_r1,"name")+' '+r1+' - '+getcityname(c_r2,"name")+' '+r2+' - MapABC驾车地图查询';
			search_route_map();
			}
}

function show_history(){
	try{
		hide_stationlist();
	}catch(ex){}
	Element.show('alldistory');
}
function colse_alldistory(){
	Element.hide('alldistory');
}

function intercept_t(v,i){
	//设置字符截取		
		try{
			if(v.length<i){
				return v;
			}else{
				var t_v = v.substring(0,i);
				return t_v+"";
			}
		}catch(e){
			return v;
		}
}
//用于切换公交查询类型()
function bus_type(){
	$('bus_type').style.display="";
	$('busline_type').style.display="none";
	$('busstation_type').style.display="none";
try{
	$('exempligratia_b').style.display="";
	$('exempligratia_l').style.display="none";
	$('exempligratia_s').style.display="none";
	}catch(ex){}
}
function busline_type(){
	$('bus_type').style.display="none";
	$('busline_type').style.display="";
	$('busstation_type').style.display="none";
	var va = $F('station_value');
	if(va!="输入站点名：天安门，中关村…"){
		$('line_value').value = va;
	}
try{
	$('exempligratia_b').style.display="none";
	$('exempligratia_l').style.display="";
	$('exempligratia_s').style.display="none";
}catch(ex){}
}
function busstation_type(){
	$('bus_type').style.display="none";
	$('busline_type').style.display="none";
	$('busstation_type').style.display="";
	var va = $F('line_value');
	if(va!="输入线路号：300，840…"){
		$('station_value').value = va;
	}
try{
	$('exempligratia_b').style.display="none";
	$('exempligratia_l').style.display="none";
	$('exempligratia_s').style.display="";
	}catch(ex){}

}
//公交线路查询
function search_bus_l(ch){

	bus_fettle = "2";//公交查询状态(线路查询)

	var bus1 =$F('line_value') ;
    var bc =$F('citylistb') ;
    var che = "以下错误造成路线查询失败         \n\n";
    var i = 1 ;
    if(bus1==""){
        che += i + "．路线不能为空\n" ;
        i = i + 1 ;
    }
//	if(isNUM(bus1)){
//		che += i + "．路线只能为数字\n" ;
//		i = i + 1 ;
//	}
    if(bc==""){
       che += i + "．请选择您要查询的城市\n" ;
        i = i + 1 ;
    }
    if(i==1){
		bus1 = encodeURI(bus1);
		if(ch=="0"){//INDEX为‘0’时为刷新页面查询，带url
			location.href='/search.html?cc='+bc+'&line='+bus1+'&page=bl';
			//location.href='/search.html?line='+bus1+'&page=bl';
		}else if(ch=="5"){//简版搜索(二级域名)
			location.href='http://www.mapabc.com/search.html?cc='+bc+'&line='+bus1+'&page=bl';
		}else{//search查询			
			logingin('1');
			//nn_b=1;
			s_b();
			c_b = $F('citylistb') ;
			//b1 = $F('b1') ;
			//b2 = $F('b2') ;
			var line_value = $F('line_value');
			//$('searchkey').value=b1;
			//$('r1').value=b1;
			document.title=line_value+' - '+getcityname(c_b,"name")+'MapABC公交线路查询  ';		
			//document.title=line_value+' - MapABC公交线路查询  ';	
			search_busl_map(line_value);
		}
		
    }else{
        alert(che);
    }
	
}

//公交站点查询
function search_bus_s(ch){
	var bus1 =$F('station_value') ;
    var bc =$F('citylistb') ;
    var che = "以下错误造成路线查询失败         \n\n";
    var i = 1 ;
    if(bus1==""){
        che += i + "．站点名称不能为空\n" ;
        i = i + 1 ;
    }
   
    if(bc==""){
        che += i + "．请选择您要查询的城市\n" ;
        i = i + 1 ;
   }
    if(i==1){
		bus1 = encodeURI(bus1);
		if(ch=="0"){//INDEX为‘0’时为刷新页面查询，带url
			location.href='/search.html?cc='+bc+'&station='+bus1+'&page=bs';
		}else if(ch=="5"){//简版搜索(二级域名)
			location.href='http://www.mapabc.com/search.html?cc='+bc+'&station='+bus1+'&page=bs';
		}else{//search查询			
			logingin('1');
			//nn_b=1;
			s_b();
			c_b = $F('citylistb') ;
			var station_value = $F('station_value');
			//$('searchkey').value=b1;
			//$('r1').value=b1;
			document.title=station_value+' - '+getcityname(c_b,"name")+'MapABC公交线路查询  ';		
			search_buss_map(station_value);
		}
		
    }else{
        alert(che);
    }
	
}

var history_bus_l = 1;//判断公交线路查询是否记录在历史记录里
var history_bus_s1 = 1;//判断公交站点查询是否记录在历史记录里

var sis3,sis4,buslinename;
var busline_xy,busstation_xy;
var busline_poi;

function search_busl_map(line_v){

	bus_fettle = "2";//公交查询状态(线路查询)

	$("line_value").value=decodeURI(line_v);
	$('citylistb').value=c_b ;
	document.getElementsByName("gjs")[1].checked=true;
	$('bus_type').style.display="none";
	$('busline_type').style.display="";
	$('busstation_type').style.display="none";

	$('default_bus1').style.display="none";
	$('default_bus').style.display="none";
	$('result_bus').style.display="";

	sis3 = new MSISSearch();
	buslinename = new MSearchRoutPara();
	sis3.setSISCallbackFunction(busLineNameCallBack); 
	buslinename.setCitycode(c_b);
	buslinename.setBusName(line_v);
	buslinename.setResData('3');

	buslinename.setFlag('1');//返回xml

	sis3.searchBusLineName(buslinename);

	document.title=getcityname(c_b,"name")+' - '+decodeURI(line_v)+'- MapABC公交线路查询  ';
	$('bus_currently').innerHTML="线路查询&nbsp;&nbsp;&nbsp;&nbsp;"+getcityname(c_b,"name")+"-"+decodeURI(line_v)+"路";
	var link = "http://www.mapabc.com/search.html?cc="+c_b+"&line="+encodeURI(line_v)+"&page=bl";
	addLink(link);
	getWeatherInfo(c_b,"code");	
}
function busLineNameCallBack(data){
	busline_xy = new Array();
	busline_poi = new Array();
	var lineNum = data.list.length;
		if(lineNum!=0){
			var bus_line_content = "<div id=\"xlDetail\" class=\"xlDetail scroll\">";
			for(var i=0;i<lineNum;i++){

				if(data.list[i].company==""){var company="";}else{var company = "所属公司："+data.list[i].company+"";}

				bus_line_content += "<div class=\"searchbus_close\" onclick=\"open_busline('"+i+"','"+lineNum+"')\"><img src=\"/html/images/searchbus_close.gif\"  id=\"busline_img"+i+"\" class=\"xlimg\" onMouseOver=\"this.className='xlimg1'\" onMouseOut=\"this.className='xlimg2'\" onmousedown=\"javascript:p_setc('0065a9')\" />"+data.list[i].name+"</div><div  id=\"busline_table"+i+"\" style=\"display:none;\"><div class=\"searchbus_busdetail\">首末车时间："+data.list[i].start_time.substring(0,2)+":"+data.list[i].start_time.substring(2,4)+"-"+data.list[i].end_time.substring(0,2)+":"+data.list[i].end_time.substring(2,4)+"；全长："+data.list[i].length+"公里;"+company+"</div><ul class=\"searchbus_buslist f14\">";
							
				var line1 = new Array();
				line1 = sis3.getBusAllStations(data.list[i].stationdes,0); 
				
				var poistr = "";
				for(var a=0; a<line1.length;a++){
					var str = line1[a].split(";");		
					//bus_line_content += "<li  onclick=\"getselected('"+i+"','"+a+"','"+line1.length+"')\" id=\"line_li_"+i+a+"\"><a href=\"javascript:drawSinglePoi('"+str[1]+"','"+str[2]+"','"+str[3]+"','"+str[0]+"','"+data.list[i].name+"')\">"+str[3]+""+str[0]+"</a></li>";

					bus_line_content += "<li  onclick=\"getselected('"+i+"','"+a+"','"+line1.length+"')\" id=\"line_li_"+i+a+"\"><a href=\"javascript:opentip('"+str[3]+"')\">"+str[3]+"&nbsp;&nbsp;"+str[0]+"</a></li>";
					
					poistr += str[1]+";"+str[2]+";"+str[3]+";"+str[0]+";"+data.list[i].name+",";
					
				}
				bus_line_content += "</ul></div>";
				busline_xy[i] =data.list[i].xys+ ",";
				busline_poi[i] = poistr+"-";
			}
		
			logingin('0');
			drawLine('0');drawallpoi('0');
			$('result_bus').innerHTML=bus_line_content;
			$('busline_table0').style.display="";
			if(history_bus_l==1){	
					var linename = $("line_value").value;
					var s2 = $('history_bus1').innerHTML;
					$('history_bus1').innerHTML ="<span style=\"cursor:pointer;color:#2155bc;text-decoration:none;\" onclick=\"javasrcipt:history_bus_sl('"+linename+"','"+c_b+"')\"><span class=\"f8\">在</span>"+getcityname(c_b,"name")+"<span class=\"f8\">查询</span>"+linename+"<span class=\"f8\">路</span></span><br/>"+s2;
			}else{
				 history_bus_l=1;
			}
		}else{
			logingin('0');
			$('result_bus').innerHTML="<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;１.请确保输入路线正确。<br />&nbsp;&nbsp;&nbsp;２.请确保已切换到所要查询的城市。<br />&nbsp;&nbsp;&nbsp;３.尝试不同的线路。<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;可尝试输入：1<br /></div>";
//			$('default_bus1').style.display="";
//			$('default_bus').style.display="none";
//			$('bus_currently').innerHTML="";
		}
}
			
function search_buss_map(station_v){

	bus_fettle = "3";//公交查询状态(站点查询)

	$("station_value").value=station_v;
	$('citylistb').value=c_b ;
	document.getElementsByName("gjs")[2].checked=true;
	$('bus_type').style.display="none";
	$('busline_type').style.display="none";
	$('busstation_type').style.display="";

	$('default_bus1').style.display="none";
	$('default_bus').style.display="none";
	$('result_bus').style.display="";

	sis4 = new MSISSearch();
	busstationname = new MSearchRoutPara();
	sis4.setSISCallbackFunction(busStationNameCallBack); 
	busstationname.setCitycode(c_b);
	busstationname.setStationName(station_v);
	busstationname.setResData('3');
	busstationname.setFlag("1");
	sis4.searchBusStationName(busstationname);	

	document.title=getcityname(c_b,"name")+' - '+station_v+'- MapABC公交站点查询  ';
	$('bus_currently').innerHTML="站点查询&nbsp;&nbsp;&nbsp;&nbsp;"+getcityname(c_b,"name")+"-"+station_v;
	var link = "http://www.mapabc.com/search.html?cc="+c_b+"&station="+encodeURI(station_v)+"&page=bs";
	addLink(link);
	getWeatherInfo(c_b,"code");	
}
function busStationNameCallBack(data){//alert(2);
	var station_n = $F('station_value');
	var stationNum = data.list.length;

	if(stationNum!=0){
		var bus_station_content ="<div id=\"xlDetail\" class=\"xlDetail scroll\"><div class=\"numberdetail\">共有<span style=\"font-weight:bold; color:#ff0000;\">"+data.list.length+"</span>条线路经过此站点</div><ul  class=\"searchbus_buslist f14\" >";
		for(var i=0;i<stationNum;i++){
			bus_station_content += "<li onclick=\"getselected_s('"+i+"','"+stationNum+"')\" id=\"line_li_"+i+"\"><a href=\"javascript:search_line('"+data.list[i].line_id+"','"+data.list[i].name+"')\">"+data.list[i].name+"</a></li>";
		}
		bus_station_content +="<li class=\"cc\"></li></ul></div>"
		logingin('0');
		$('result_bus').innerHTML= bus_station_content;
		if(history_bus_s1==1){	
					var stationname = $("station_value").value;
					var s2 = $('history_bus1').innerHTML;
					$('history_bus1').innerHTML ="<span style=\"cursor:pointer;color:#2155bc;text-decoration:none;\" onclick=\"javasrcipt:history_bus_ss('"+stationname+"','"+c_b+"')\"><span class=\"f8\">在</span>"+getcityname(c_b,"name")+"<span class=\"f8\">查询</span>"+stationname+"<span class=\"f8\"></span></span><br/>"+s2;
			}else{
				 history_bus_s1=1;
			}
	}else{
		logingin('0');
			$('result_bus').innerHTML="<div class=\"reinfo\">&nbsp;&nbsp;&nbsp;建议：<br />&nbsp;&nbsp;&nbsp;１.请确保输入站名正确。<br />&nbsp;&nbsp;&nbsp;２.请确保已切换到所要查询的城市。<br />&nbsp;&nbsp;&nbsp;３.尝试不同的名称。<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br /></div>";
	}
}
var stateOpen_id = "busline_table0";
var stateOpen_img = "busline_img0";
function open_busline(num,linenum){
	var id = "busline_table"+num;
	var imgid = "busline_img"+num;
	var ids = $(id).style.display;
	if(stateOpen_id==id ){
		if(ids=="none"){
			$(id).style.display="";
			drawLine(num);
			$(imgid).src = "html/images/searchbus_open.gif";
		}else{
			$(id).style.display="none";
			$(imgid).src = "html/images/searchbus_close.gif";
		}
	}else{
		$(id).style.display="";
		drawLine(num);
		drawallpoi(num);
		$(imgid).src = "html/images/searchbus_open.gif";
		$(stateOpen_id).style.display="none";
		$(stateOpen_img).src = "html/images/searchbus_close.gif";
	}
	stateOpen_id = id;
	stateOpen_img = imgid;
	
	
	

//	for(var i = 0;i<linenum;i++){
//		var id1 = "busline_table"+i;
//		var imgid1 = "busline_img"+i;
//		$(id1).style.display="none";
//		$(imgid1).src = "html/images/searchbus_close.gif";
//	}
//	if(ids=="none"){
//		$(id).style.display="";
//		$(imgid).src = "html/images/searchbus_open.gif";
//		drawLine(num);
//	}else{
//		$(id).style.display="none";
//		$(imgid).src = "html/images/searchbus_close.gif";
//	}
	
}
//判断输入路线号是否为数字
//function isNUM(parameter){
//	 var re = /^[0-9]+.?[0-9]*$/;   //判断字符串是否为数字  
//     if (!re.test(parameter)){
//		return true;
//     }else{
//		return false;
//	 }
//}
function drawallpoi(num){
	var poi_xy = busline_poi[num].split(",");
//	alert(poi_xy);
//	alert(poi_xy.length);
	for(var i = 0;i<poi_xy.length-1;i++){
		var str =  poi_xy[i].split(";");


		var pointStyle1 = new MStyle();
		pointStyle1.lineColor = getMaptips_c();
		pointStyle1.lineSize = 1;
		pointStyle1.fillColor = getMaptips_c();
		pointStyle1.fillOpacity = 90;
		pointStyle1.labelColor = 0x00ff00;
		var sContent1 = "<font color='#ffffff'>站点名称："+str[3]+"</font><br>";
		sContent1 += "<font color='#ffffff'>所属线路："+str[4]+"站</font><br>";
        sContent1 += "<font color='#ffffff'>站点序号：第"+str[2]+"站</font><br>";
		pointStyle1.textContent = sContent1;

		var customPoint2 = new MCustomPointOverlay(new MLatLng(str[1],str[0]), "http://www.mapabc.com/html/images/wwwdiyimg/001.png", pointStyle1, str[2]+1);
	
	mapObj.drawCustomPoints([customPoint2], false);

	}
}


//画线
function drawLine(num){
	mapObj.removeAllOverlays();
	var startObj=new MStyle();
		startObj.lineColor = 0xff0000;
		startObj.lineSize = 5;
		//startObj.showTip = false; 
		startObj.maxZoomLevel = "500"

	var endObj=new MStyle();
		endObj.lineColor = 0xff0000;
		endObj.lineSize = 5;
		//endObj.showTip = false; 
		endObj.maxZoomLevel = "500"
		
	
	var lineObj=new MStyle();

	lineObj.lineSize=6;
	//lineObj.lineColor=0x006400;
	//lineObj.lineColor=0x1522c3;6c95f3
	lineObj.lineColor=0x1d5ceb;

	lineObj.lineOpacity="70";
	lineObj.showTip = false;

	var qdpoiy = getStartY(num);
	var qdpoix = getStartX(num);

	var zdpoiy = getEndY(num);
	var zdpoix = getEndX(num);

	var startPoint = new MPointOverlay(new MLatLng(qdpoiy,qdpoix), "sdfds", startObj);
	var endPoint = new MPointOverlay(new MLatLng(zdpoiy,zdpoix), "sdfsd", endObj);
	if(qdpoix == "" || qdpoix == "null" || zdpoix == "" || zdpoiy =="null"){}else{
	mapObj.drawBusLine(getStrX(num), getStrY(num), "", "", startPoint, endPoint, lineObj,true);
	}
}

function getStrX(num){
		 var poi_xy = busline_xy[num].split(",");
				var arrX = "";//行车路线的X串
				for(var e=0;e<poi_xy.length-1;e=e+2){	
					if(e==poi_xy.length-3){
						arrX += poi_xy[e];
					}else{
						arrX += poi_xy[e]+",";
					}
				}
		return arrX;
}
function getStrY(num){
	var poi_xy = busline_xy[num].split(",");
		var arrY = "";//行车路线的Y串
		for(var e=0;e<poi_xy.length-1;e=e+2){	
			if(e==poi_xy.length-3){
				arrY += poi_xy[e+1];
			}else{
				arrY += poi_xy[e+1]+",";
			}
		}
	return arrY;	
}
function getStartX(num){
	var poi_xy = busline_xy[num].split(",");
	return poi_xy[0];
}
function getStartY(num){
	var poi_xy = busline_xy[num].split(",");
	return poi_xy[1];
}

function getEndX(num){
	var poi_xy = busline_xy[num].split(",");
	return poi_xy[poi_xy.length-3];
}

function getEndY(num){
	var poi_xy = busline_xy[num].split(",");
	return poi_xy[poi_xy.length-2];
}
var point_id = "";
function drawSinglePoi(px,py,serialid,pn,linename){//alert(serialid);
    mapObj.removeCustomPointById(point_id);
	point_id = serialid+1;
	
		var pointStyle1 = new MStyle();
		pointStyle1.lineColor = getMaptips_c();
		pointStyle1.lineSize = 1;
		pointStyle1.fillColor = getMaptips_c();
		pointStyle1.fillOpacity = 90;
		pointStyle1.labelColor = 0x00ff00;
		var sContent1 = "<font color='#ffffff'>站点名称："+pn+"</font><br>";
		sContent1 += "<font color='#ffffff'>所属线路："+linename+"站</font><br>";
        sContent1 += "<font color='#ffffff'>站点序号：第"+serialid+"站</font><br>";
		 	pointStyle1.textContent = sContent1;

	var customPoint2 = new MCustomPointOverlay(new MLatLng(py,px), "http://www.mapabc.com/html/images/wwwdiyimg/001.png", pointStyle1, point_id);
	
	mapObj.drawCustomPoints([customPoint2], false);
	setTimeout(" mapObj.openTipById('"+point_id+"')",300);
	
}

var sis5="";
function search_line(lineid,linename){
	logingin('1');
	sis5 = new MSISSearch();
	var buslineid = new MSearchRoutPara();
	sis5.setSISCallbackFunction(busLineIdCallBack); 
	buslineid.setCitycode(c_b);
	buslineid.setIds(lineid);
	buslineid.setResData('3');

	buslineid.setFlag('1');

	sis5.searchBusLineId(buslineid);
}
var list_cur_num=0;
function busLineIdCallBack(data){
	list_cur_num = 0;
	var station_n = $F('station_value');

	busline_xy = new Array();
	var lineNum = data.list.length;

	var bus_line_content = "<div class=\"div_title\"><span style=\"float:left; font-weight:bold; text-indent:5px;\">"+station_n+"</span><a href=\"javascript:hide_stationlist()\"></a></div>";

	//for(var i=0;i<lineNum;i++){
	

	if(data.list[0].company==""){var company="";}else{var company = "<tr><td valign=\"top\" colspan=\"2\" align=\"left\">所属公司："+data.list[0].company+"</td></tr>"}

	bus_line_content += "<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" style=\"line-height:16px; background:#f9f9f9; border-bottom:1px solid #dcdcdc;\"><tr><td width=\"33%\" align=\"right\">首末时间：</td><td width=\"67%\" align=\"left\">"+data.list[0].start_time.substring(0,2)+":"+data.list[0].start_time.substring(2,4)+"-"+data.list[0].end_time.substring(0,2)+":"+data.list[0].end_time.substring(2,4)+"</td></tr><tr><td align=\"right\">路程全长：</td><td align=\"left\">"+data.list[0].length+"公里</td></tr>"+company+"</table>";

	var line1 = new Array();

	line1 = sis5.getBusAllStations(data.list[0].stationdes,10); 
	var line_pageNum = line1.length;


	for(var b = 0 ;b<line_pageNum;b++){
		if(b==0){
			bus_line_content += "<ul class=\"div_resultlist\" id=\"station_list_"+b+"\" >";
			var str = line1[b].split("#");	
			for(var c =0 ;c<str.length-1;c++){
				var test = str[c].split(";");
			
				bus_line_content += "<li onclick=\"drawSinglePoi('"+test[1]+"','"+test[2]+"','"+test[3]+"','"+test[0]+"','"+data.list[0].name+"')\" style=\"cursor:pointer\">"+test[3]+"&nbsp;&nbsp;"+test[0]+"</li>";
			}
			bus_line_content += "</ul>";
		}else{
			bus_line_content += "<ul class=\"div_resultlist\" id=\"station_list_"+b+"\" style=\"display:none\">";
			var str = line1[b].split("#");	
			for(var c =0 ;c<str.length-1;c++){
				var test = str[c].split(";");
			
				bus_line_content += "<li onclick=\"drawSinglePoi('"+test[1]+"','"+test[2]+"','"+test[3]+"','"+test[0]+"','"+data.list[0].name+"')\" style=\"cursor:pointer\">"+test[3]+"&nbsp;&nbsp;"+test[0]+"</li>";
			}
			bus_line_content += "</ul>";
		}
		}
		bus_line_content += "<span><a href=\"javascript:list_next('"+line_pageNum+"')\" class=\"div_next\"  title=\"下一页\"></a><a href=\"javascript:list_pre("+line_pageNum+")\" class=\"div_pre\" title=\"上一页\"></a></span>";
		busline_xy[0] =data.list[0].xys+ ",";
		
	//}
	logingin('0');
	$('searchLineId_div').innerHTML=bus_line_content;
	show_stationlist();
	drawLine('0');

}
var list_cur_num=0;
function list_next(pagenum){
	if(list_cur_num<pagenum-1){
		for(var i = 0;i<pagenum-1;i++){
	
			var id="station_list_"+i;
			$(id).style.display="none";
		}
		list_cur_num = list_cur_num+1;
		var show_id="station_list_"+list_cur_num;
		$(show_id).style.display="";
	}else{
		
		var show_id="station_list_"+pagenum;
		$(show_id).style.display="";
	}
}
function list_pre(pagenum){
if(list_cur_num==0){}else{
	if(list_cur_num<pagenum){
		for(var i = 0;i<pagenum;i++){
	
			var id="station_list_"+i;
			$(id).style.display="none";
		}
		list_cur_num = list_cur_num-1;
		var show_id="station_list_"+list_cur_num;
		$(show_id).style.display="";
	}
	}
}
//显示隐藏站点查询中路线所经站列表
function  show_stationlist(){
	$('stationlist_div').style.display="";
}
function hide_stationlist(){
	$('stationlist_div').style.display="none";
}
function getselected(n1,n2,num){
	var id = "line_li_"+n1+n2;
	//alert(id);
	//$(id).style.backgroundColor="#993399";
	for(var i =0;i<num;i++){
		var id1 = "line_li_"+n1+i;
		Element.removeClassName(id1,'selectid');
	}
	document.getElementById(id).className = "selectid";
}
function getselected_s(n1,num){
	var id = "line_li_"+n1;
	//alert(id);
	//$(id).style.backgroundColor="#993399";
	for(var i =0;i<num;i++){
		var id1 = "line_li_"+i;
		Element.removeClassName(id1,'selectid');
	}
	document.getElementById(id).className = "selectid";
}
function history_bus_sl(linename,c_b){
	colse_alldistory();
	logingin('1');
	history_bus_l = 0;
	gj(null);
	search_busl_map(encodeURI(linename));
	c_b=c_b;
}
function history_bus_ss(stationname,c_b){
	colse_alldistory();
	logingin('1');
	history_bus_s1 = 0;
	gj(null);
	search_buss_map(stationname);
	c_b=c_b;
}
function opentip(poiid){
	var point_id = poiid+1;
	mapObj.openTipById(point_id);
}

function point_coor(px,py){
	differentiate_s=1;
	if(mapList[''+c_s+search_x+'_'+s+'_'+page_now+'_'+area_range+'_'+dataNum]==null){
			page = 1;
			page_now = 1
			page_allnum = 0;
			points=null ;
			sis = new MSISSearch();
			point_sp = new MSearchPointPara();
			sis.setSISCallbackFunction(myfunc_p1);
			point_sp.setCitycode(c_s);
			point_sp.setCenXY(px,py);
			point_sp.setKeyword(s);
			point_sp.setNumber(dataNum); 
			point_sp.setRange(area_range);
			point_sp.setPageSum(1);
			point_sp.setBatch(page); 			
			sis.localSearchByXY(point_sp); 
		}else{
			history_bd = 0;
			write_ls("zb");
		}
}
function myfunc_p1(data){
	mapList[''+c_s+search_x+'_'+s+'_'+page_now+'_'+area_range+'_'+dataNum]=eval('(data)');
	write_ls("coor");
}