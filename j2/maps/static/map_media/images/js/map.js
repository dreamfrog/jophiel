	var dmap, gmap; //地图变量
	var turn = true; //控制切换变量
	var DmapMarker, GmapMarker;
    var GmapMoveListener, DmapMoveListener, GmapZoomListener, DmapZoomListener;
    var DmapMarkListener, GmapMarkListener;
	//var latitudeErr=0.001247372185753; //(51/100000-google),51与google的经度误差
	//var longtitudeErr=0.005965740801493;//(51/10000-google),51与google的纬度误差

	/**
	 * 描述:获取google地图坐标
	 * 参数:灵图坐标点
	 * 返回:google地图坐标
	 */
	function GetGPoint(ltpnt)
	{
		var latitudeErr=0.001247372185753; //(51/100000-google),51与google的经度误差
		var longtitudeErr=0.005965740801493;//(51/10000-google),51与google的纬度误差
		var point = new GLatLng(ltpnt.getLatitude()/100000-latitudeErr, ltpnt.getLongitude()/100000-longtitudeErr);
		return point;
	}

	/**
	 * 描述:获取灵图地图坐标
	 * 参数:google地图坐标
	 * 返回:灵图地图坐标
	 */
	function GetLTPoint(gpnt)
	{
		var latitudeErr=0.001247372185753; //(51/100000-google),51与google的经度误差
		var longtitudeErr=0.005965740801493;//(51/10000-google),51与google的纬度误差
		var point = new LTPoint((gpnt.lng()+longtitudeErr)*100000, (gpnt.lat()+latitudeErr)*100000);
		return point;

	}
	
	//灵图弹出信息窗口函数
	function getDInfo(marker,html)
	{
	    return function(){marker.openInfoWinHtml(html)} ;
	}
	//google弹出信息窗口函数
	function getGInfo(marker,html)
	{
	    return function(){marker.openInfoWindowHtml(html)} ;
	}
	
	/**
	 * 描述:更新google地图
	 * 
	 */
    function changeGmap()
    {
        GEvent.removeListener(GmapMoveListener);
        GEvent.removeListener(GmapZoomListener);
        var point = dmap.getCenterPoint();
        var dzoom = dmap.getCurrentZoom();
		var ltPnt = GetGPoint(point);
        gmap.setCenter(ltPnt, 17-dzoom); //二者之和差不多17级
        GmapMoveListener = GEvent.addListener(gmap, "moveend", changeDmap);
        GmapZoomListener = GEvent.addListener(gmap, "zoomend", changeDmap);
    }
	
	/**
	 * 描述:更新51地图
	 * 
	 */
    function changeDmap()
    {
        LTEvent.removeListener(DmapMoveListener);
        LTEvent.removeListener(DmapZoomListener);
        var point = gmap.getCenter();
        var gzoom = gmap.getZoom();
		var gPnt = GetLTPoint(point);
        dmap.centerAndZoom(gPnt,17 - gzoom);//二者之和差不多17级
        DmapMoveListener = LTEvent.addListener( dmap, "moveend", changeGmap);
        DmapZoomListener = LTEvent.addListener( dmap, "zoomend", changeGmap)
    }
	
	/**
	 * 切换地图
	 */
    function turnMaps()
    {
        turn = !turn;
        if(turn)
            turnToDmap();
        else
            turnToGmap();
    }
	
	/**
	 *切换成51地图
	 */
	function turnToDmap()
    {
        var center = gmap.getCenter();
        var zoom = gmap.getZoom();
        dmap=new LTMaps("map51");
		var ltPnt = GetLTPoint(center);
	    dmap.cityNameAndZoom(ltPnt , 17-zoom);
        //dmap.addControl(new LTStandMapControl());
        DmapMoveListener = LTEvent.addListener( dmap, "moveend" , changeGmap);
        DmapZoomListener = LTEvent.addListener( dmap, "zoomend", changeGmap);

        if (GBrowserIsCompatible())
        {
            gmap = new GMap2(document.getElementById("map"));
            gmap.setCenter(center, zoom);
            gmap.setMapType(new GMapType(G_HYBRID_MAP.getTileLayers(), G_HYBRID_MAP.getProjection(), "Custom", {minResolution:3}));
			gmap.addControl(new GLargeMapControl());
            GmapMoveListener = GEvent.addListener(gmap, "moveend", changeDmap);
            GmapZoomListener = GEvent.addListener(gmap, "zoomend", changeDmap);
        }

		SetPoints(gpoints);
    }
    
	/**
	 *切换成googel地图
	 */
    function turnToGmap()
    {
        var center = dmap.getCenterPoint();
        var zoom = dmap.getCurrentZoom();
        dmap=new LTMaps("map");
		dmap.addControl(new LTStandMapControl());
	    dmap.centerAndZoom(center, zoom);
        DmapMoveListener = LTEvent.addListener( dmap, "moveend" , changeGmap);
        DmapZoomListener = LTEvent.addListener( dmap, "zoomend", changeGmap);

        if (GBrowserIsCompatible())
        {
            gmap = new GMap2(document.getElementById("map51"));
			var gPnt = GetGPoint(center);
            gmap.setCenter(gPnt, 17-zoom);
            gmap.setMapType(new GMapType(G_HYBRID_MAP.getTileLayers(), G_HYBRID_MAP.getProjection(), "Custom", {minResolution:3}));
            //gmap.addControl(new GLargeMapControl());
            GmapMoveListener = GEvent.addListener(gmap, "moveend", changeDmap);
            GmapZoomListener = GEvent.addListener(gmap, "zoomend", changeDmap);
        }

		SetPoints(gpoints);
    }

	/**
	 * 描述:自动定位到某个点上,x为经度，y为纬度
	 * 参数: point:google地图坐标点 textInfo:弹出式窗口内容
	 */
	function gotoSpecPoint(point,textInfo)
	{
		
		gmap.panTo(point);
		//google
		gmap.openInfoWindowHtml(point, textInfo);
		
		//51map
		var ltPnt = GetLTPoint(point);
		var infoWin = new LTInfoWindow(ltPnt);
		infoWin.setLabel( textInfo); 
		dmap.addOverLay( infoWin ); 

	}
     
	 /**
	  * 创建点
	  */
	function createLables()
    {
        DmapMarkListener = LTEvent.addListener(dmap, "click", onDmapClick);
        GmapMarkListener = GEvent.addListener(gmap, "click", onGmapClick);
    }
    
	/**
	 * 在51地图上点点的事件
	 */
	function onDmapClick(p)
    {
        if(DmapMarker)
        {
            dmap.removeOverLay(DmapMarker);
            gmap.removeOverlay(GmapMarker);
        }
        var point = dmap.getClickLatLng(p);
        var dicon = GetLTIcon(0);
        DmapMarker = new LTMarker(point, dicon);
        DmapDragListener = LTEvent.addListener(DmapMarker, "dragend", onDmapMarkerDrag);
        DmapMarker.enableDrag();
        dmap.addOverLay(DmapMarker);

		var gIcon = GetGIcon(0);
		var gPnt =  GetGPoint(point);

        GmapMarker = new GMarker(gPnt,{icon:gIcon,draggable: true});
        GmapDragListener = GEvent.addListener(GmapMarker, "dragend", onGmapMarkerDrag);
        gmap.addOverlay(GmapMarker);

        LTEvent.removeListener(DmapMarkListener);
        GEvent.removeListener(GmapMarkListener);
    }
    
	/**
	 * 响应google地图点击事件
	 */
	function onGmapClick(marker, point)
    {
        if(GmapMarker)
        {
            dmap.removeOverLay(DmapMarker);
            gmap.removeOverlay(GmapMarker);
        }
		var gIcon = GetGIcon(0);
        GmapMarker = new GMarker(point,{icon:gIcon,draggable: true});
        GmapDragListener = GEvent.addListener(GmapMarker, "dragend", onGmapMarkerDrag);
        gmap.addOverlay(GmapMarker);

        var icon2 = GetLTIcon(0);
		var ltPnt = GetLTPoint(point);
        DmapMarker = new LTMarker(ltPnt, icon2);
        DmapDragListener = LTEvent.addListener(DmapMarker, "dragend", onDmapMarkerDrag);
        DmapMarker.enableDrag();
        dmap.addOverLay(DmapMarker);

        GEvent.removeListener(GmapMarkListener);
        LTEvent.removeListener(DmapMarkListener);
    }
	
	/**
	 * 拖拽点
	 */
	function onDmapMarkerDrag()
    {
        LTEvent.removeListener(DmapDragListener);
        gmap.removeOverlay(GmapMarker);
		var point = DmapMarker.getPoint();
		var gPnt = GetGPoint(point);
		var gIcon = GetGIcon(0);
        GmapMarker = new GMarker(gPnt, {icon:gIcon,draggable: true});
        GmapDragListener = GEvent.addListener(GmapMarker, "dragend", onGmapMarkerDrag);
        gmap.addOverlay(GmapMarker);
        DmapDragListener = LTEvent.addListener(DmapMarker, "dragend", onDmapMarkerDrag);
    }
    
	/**
	 *拖拽google地图上的点
	 */
	function onGmapMarkerDrag()
    {
        GEvent.removeListener(GmapDragListener);
        dmap.removeOverLay(DmapMarker);
        var point = GmapMarker.getPoint();
        var icon2 = GetLTIcon(0);
		var ltPnt = GetLTPoint(point);
        DmapMarker = new LTMarker(ltPnt, icon2);
        DmapDragListener = LTEvent.addListener(DmapMarker, "dragend", onDmapMarkerDrag);
        DmapMarker.enableDrag();
        dmap.addOverLay(DmapMarker);
        GmapDragListener = GEvent.addListener(GmapMarker, "dragend", onGmapMarkerDrag);
    }
    
	/**
	 * 获取点经度坐标,google坐标
	 */
	function getPos_x()
    {
        var point = GmapMarker.getPoint();
        return point.lng();
    }
    
	/**
	 *获取点的纬度坐标,google坐标
	 */
    function getPos_y()
    {
        var point = GmapMarker.getPoint();
        return point.lat();
    }
	
	/**
	 *返回google缩放级别
	 */
	function getGZoom()
	{
		return gmap.getZoom();
	}

    
	/**
	 *获取google地图图标样式
	 *参数: j 图标序号
	 */
	function GetGIcon(j)
	{
		var icon = new GIcon();
		icon.image = "images/icon_"+(j+1)+".gif";
		icon.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png";
		icon.iconSize = new GSize(25, 25);
		icon.shadowSize = new GSize(22, 20);
		icon.iconAnchor = new GPoint(12, 25);
		icon.infoWindowAnchor = new GPoint(5, 1);

		return icon;
	}
	
	/**
	 * 获取51地图图标样式
	 *参数: j 图标序号
	 */
	function GetLTIcon(j)
	{
		var dIcon = new LTIcon("images/icon_"+(j+1)+".gif",[25,25],[12,12]);

		return dIcon;
	}
	
	/**
	 * 描述:初始调用,要传入几个变量,全是数组形式;依次是:坐标点(google),放大级别,标题,地址,发布时间
	 */
    function load()
    {

       if (GBrowserIsCompatible())
        {

			gmap = new GMap2(document.getElementById("map"));
			gmap.addControl(new GLargeMapControl());
			dmap=new LTMaps("map51");
			//dmap.addControl(new LTStandMapControl());
            //var point = dmap.getCenterPoint();
			//var zoom=dmap.getCurrentZoom();
            //gmap.setCenter(new GLatLng(point.getLatitude()/100000-latitudeErr, point.getLongitude()/100000-longtitudeErr), 17-zoom);
            
            //gmap.addControl(new GSmallMapControl());
			GmapMoveListener = GEvent.addListener(gmap, "moveend", changeDmap);
            GmapZoomListener = GEvent.addListener(gmap, "zoomend", changeDmap);
            
			
			
			//没有值,默认显示北京
			if((gpoints == null) ||(gpoints.length==0))
			{
				gmap.setCenter(new GLatLng(39.89945, 116.4096), 14);
				//return;
			}
			else if(gpoints.length > 1)
			{
				//dmap.getBestMap(dpoints);//将地图定位到最佳视图
				var bound = new GBounds(gpoints);
				var ctrPnt = new GLatLng(Math.abs(bound.maxY+bound.minY)/2,Math.abs(bound.maxX+bound.minX)/2);
				var bnds = new GLatLngBounds(new GLatLng(bound.minY,bound.minX),new GLatLng(bound.maxY,bound.maxX));
				var level = gmap.getBoundsZoomLevel(bnds);
				gmap.setCenter(ctrPnt,level);
			}
			else if(gpoints.length == 1)
			{
				gmap.setCenter(gpoints[0], zoom[0]);
			}

            gmap.setMapType(new GMapType(G_HYBRID_MAP.getTileLayers(), G_HYBRID_MAP.getProjection(), "Custom", {minResolution:3}));

			
			var ltPnt = GetLTPoint(gmap.getCenter());
			var ltZoom = 17 - gmap.getZoom();
			dmap.centerAndZoom(ltPnt,ltZoom);
			DmapMoveListener = LTEvent.addListener( dmap, "moveend", changeGmap);
			DmapZoomListener = LTEvent.addListener( dmap, "zoomend", changeGmap);
			
			SetPoints(gpoints);
			
        }
     }
	
	 /**
	  *在地图上标注点,同时在两个窗口上标注
	  */
	 function SetPoints(gpoints)
	 {
		//循环显示点,同时监听弹出窗口
		for (var j=0; j<gpoints.length; j++)
		{
			var dicon = GetLTIcon(j);
			var ltPnt = GetLTPoint(gpoints[j]);
			var dmarker = new LTMarker(ltPnt, dicon);
			//拼凑弹出框显示内容,标题,地址,发布时间,扩展时,也可以把链接地址加上
			var html=title[j] + "<br>" + address[j] + "<br>" + time[j];

			LTEvent.addListener( dmarker , "mouseover" ,getDInfo(dmarker,html));
			dmap.addOverLay(dmarker);

			var icon = GetGIcon(j);
			var gmarker = new GMarker(gpoints[j], icon);
			GEvent.addListener(gmarker,"mouseover", getGInfo(gmarker,html));
			gmap.addOverlay(gmarker);
		}
	 }

