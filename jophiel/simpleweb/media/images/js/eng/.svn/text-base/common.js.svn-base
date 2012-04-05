	function changeCity()
	{//转到切换城市页面
		document.form1.action = "/city.php";
		document.form1.submit();
	}
	
	function selectCity(event)
	{//弹出选择城市tip框
		document.getElementById('SelectCity').style.display = "block";
		document.getElementById('SelectCity').style.top = event.clientY+10;
		document.getElementById('SelectCity').style.left = event.clientX-350;
	}
	
	function indexChangeByCity(city_name)
	{//首页推荐城市切换
		document.form1.cityname.value = city_name;
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/eng/index.php";
		document.form1.submit();
	}
	
	function index_change(cityname)
	{//首页切换城市页面切换
		document.form1.cityname.value = cityname;
		document.form1.action="/index.php";
		document.form1.submit();
	}
	
	function mapSearchByCity(city_name)
	{//map页面推荐城市直接搜索
		document.form1.cityname.value = city_name;
		document.getElementById('SelectCity').style.display = "none";
		document.form1.action="/map.php";
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
		document.form1.action="/eng/index_s.php";
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
	
	function chn_onstar_search(cityname)
	{//map页面切换城市页面选择搜索
		document.form1.cityname.value = cityname;
		alert("dd");return false;
		document.form1.action="/chn/onstar_search.php";
		document.form1.submit();
	}
	function closeSelectCity()
	{
		document.getElementById('SelectCity').style.display = "none";
	}
	
	function no_pop_window()
	{
		document.getElementById('SelectCity').style.display = "none";
	}