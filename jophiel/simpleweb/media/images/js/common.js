﻿	function changeCity()
	{//转到切换城市页面
		document.form1.action = "/city";
		document.form1.submit();
	}
	
	function changeCity_Link()
	{//转到切换城市页面
		document.form1.action = "/link/city";
		document.form1.submit();
	}
	
	function selectCity(event)
	{//弹出选择城市tip框
		document.getElementById('SelectCity').style.display = "block";
		document.getElementById('SelectCity').style.top = event.clientY+10;
		document.getElementById('SelectCity').style.left = event.clientX-400;
	}
	
	function LinkIndexSelectSource()
	{
		document.getElementById('LinkSelectSource').style.display = "block";
	}
	function LinkIndexSelectCity()
	{
		document.getElementById('LinkSelectCity').style.display = "block";
		//document.getElementById('SelectCity').style.top = 0;
		//document.getElementById('SelectCity').style.left = 0;	
	}
	
	function indexChangeByCity(city_name)
	{//首页推荐城市切换
		document.form1.cityname.value = city_name;
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/index";
		document.form1.submit();
	}
	
	function index_change(cityname)
	{//首页切换城市页面切换
		document.form1.cityname.value = cityname;
		document.form1.action="/index";
		document.form1.submit();
	}
	
	function index_change_Link(cityname)
	{//首页切换城市页面切换
		document.form1.cityname.value = cityname;
		document.form1.action="/link/index";
		document.form1.submit();
	}
	
	function mapSearchByCity(city_name)
	{//map页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/map";
		document.form1.submit();
	}
		
	function map_search(cityname,kw)
	{//map页面切换城市页面选择搜索
		document.form1.cityname.value = cityname;
		document.form1.kw.value = kw;
		
		document.form1.action="/map.php";
		document.form1.submit();
	}

	
	function detailSearchByCity(city_name)
	{//detail页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/index_s.php";
		document.form1.submit();
	}
	
	function qiiIndexSearchByCity(city_name)
	{//qii首页推荐城市直接搜索
		document.form1.cityname.value = city_name;
		
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/qii/index.php";
		document.form1.submit();
		//alert("sfsfsd");
	}
	
	function qiiIndex_search(cityname)
	{//qii首页切换城市直接搜索
		document.form1.cityname.value = cityname;
		document.form1.action="/qii/index.php";
		document.form1.submit();
		/*alert("sfsfsd");*/
	}
		
	function linkIndexChangeCity(city_name)
	{//link首页推荐城市直接搜索
		document.form1.cityname.value = city_name;
		document.getElementById('LinkSelectCity').style.display = "none";
		document.form1.action="/link/index.php";
		document.form1.submit();
	}
	
	function linkSearchChangeCity(city_name)
	{//link首页推荐城市直接搜索
		document.form1.cityname.value = city_name;
		document.form1.CitynameButton.value = city_name;
		document.getElementById('LinkSelectCity').style.display = "none";
		//document.form1.action="/link/index_s.php";
		//document.form1.submit();
	}
	
	function movieSearchByCity(city_name)
	{//movie/页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/movie/index.php";
		document.form1.submit();
	}
	
	function discountSearchByCity(city_name)
	{//discount/页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/discount/index.php";
		document.form1.submit();
	}
	
	function indexsSearchByCity(city_name)
	{//index_s页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/index_s.php";
		document.form1.submit();
	}
		
	function index_s_search(city_name,area,kw)
	{//detail和index_s页面切换城市页面选择搜索
		document.form1.cityname.value = city_name;
		document.form1.area.value = area;
		document.form1.kw.value = kw;
		
		document.form1.action="/index_s.php";
		document.form1.submit();
	}
	
	function chnOnstarSearchByCity(city_name)
	{//chn/onstar_search页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/chn/onstar_search.php";
		document.form1.submit();
	}
	
	function chn_onstar_search(cityname,kw)
	{//chn/onstar_search页面切换城市页面选择搜索
		document.form1.cityname.value = cityname;
		document.form1.kw.value = kw;
		
		document.form1.action="/chn/onstar_search.php";
		document.form1.submit();
	}
	function closeSelectCity()
	{
		document.getElementById('SelectCity').style.display = "none";
	}
	function closeLinkSelectCity()
	{
		document.getElementById('LinkSelectCity').style.display = "none";
	}
	function closeLinkSelectSourceUnSubmit()
	{
		document.getElementById('LinkSelectSource').style.display = "none";
	}
	
	function closeLinkSelectSourceSubmitIndex()
	{
		document.form1.sourcename.value = "";
		for (var i=0;i< document.form1.elements.length;i++)
		{//遍历表单项
			var e = form1.elements[i]
      if (e.name == "source_check" && e.checked)
    	{
        if(document.form1.sourcename.value != "")
    			{
    				document.form1.sourcename.value += "+";
    			}
         	document.form1.sourcename.value += e.id;
    	}
    }
		document.getElementById('LinkSelectSource').style.display = "none";
		document.form1.action="/link/index.php";
		document.form1.submit();
	}
	
	function closeLinkSelectSourceChangeDisplay()
	{
		document.form1.sourcename.value = "";
		var checkAllflag = 1;
		for (var i=0;i< document.form1.elements.length;i++)
		{//遍历表单项
			var e = form1.elements[i]
      if (e.name == "source_check")
    	{
    		if (e.checked)
    		{
    			if(document.form1.sourcename.value != "")
    			{
    				document.form1.sourcename.value += "+";
    			}
         	document.form1.sourcename.value += e.id;
       	}
       	else
       	{
       		checkAllflag = 0;
       	}
    	}
    }
    if (checkAllflag == 1)
    {
    	document.form1.SourcenameButton.value = "所有";
  	}	
  	else
  	{
  		document.form1.SourcenameButton.value = document.form1.sourcename.value;
		}
		
		document.getElementById('LinkSelectSource').style.display = "none";
		//document.form1.action="/link/index_s.php";
		//document.form1.submit();
	}
	
	function no_pop_window()
	{
		document.getElementById('SelectCity').style.display = "none";
	}
	
	function selectSourceByID(id)
	{
		if(document.getElementById(id).checked == false)
		{
			document.getElementById(id).checked = true;
		}
		else
		{
			document.getElementById(id).checked = false;
		}
	}
	
	function check_it(id)
	{
		document.getElementById(id).checked = true;
	}
	
	 function check_all(obj,cName)
{
     var checkboxs = document.getElementsByName(cName);
     for(var i=0;i<checkboxs.length;i++){checkboxs[i].checked = obj.checked;}
 }