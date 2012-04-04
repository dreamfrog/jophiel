/*
飞飞Ajax模仿google提示输入框 使用说明 v1.0
本程序由飞飞asp乐园编写，其中部分代码来源于网上
如有侵权 请与我联系

飞飞Asp乐园
www.ffasp.com
QQ:276230416

程序介绍：

本程序官网演示地址：http://www.ffasp.com/content.asp?newsid=969
转载请注明出处

此小程序是模仿Google输入提示框所编写
亦可用于用户注册邮箱时的提示
此程序使用方便简单、易用灵活
且不限Asp、php、net

文件使用说明：
在需要使用的页面首先要引用2个js文件
<script src="../inc/jquery1.2.3.min.js"></script>
<script src="search_suggest.js"></script>
此二文件必须放于调用函数之前
调用函数
<script>SuggestShow("aa","search.asp")</script>
函数介绍：
"aa"为需要输入信息的input的name和id,如果想修饰该input可以通过css“#”选择符修饰
search.asp 即为远程页面
该页面返回根据 “aa”输入的信息的所有提示
该文件输出格式为xml
该文件有一输入参数/接受参数inputval其值为“aa”输入的值
*/

var array=new Array(); //要SUGGEST的内容 
var area_width_src = "";
var kw_width_src = "";
var choose_flag = "no";
var sunjg = "";

var zz=-1; //此为指针
//函数生成下拉列表 
function buildList(InputName){ 
zz=-1; 
document.getElementById(InputName+"search_suggest").innerHTML=""; 
for(var i=0;i<array.length;i++)
{ 
	//根据输入框的宽度设置下来菜单的宽度
	if(area_width_src == 32){area_width_list = 232;}
	else if(area_width_src == 30){area_width_list = 232;}
	
	if(kw_width_src == 40){kw_width_list = 288;}
	else if(kw_width_src == 50){kw_width_list = 358;}
	else if(kw_width_src == 30||kw_width_src == 32){kw_width_list = 232;}
	
	if(array[i]!="" && i<(array.length-1))
	{ 
		if(InputName == "kw")
		{
			document.getElementById(InputName+"search_suggest").innerHTML+="<div id='"+InputName+"item" + i + "' style=\"width:"+kw_width_list+"\" class='item_normal' onmouseover='beMouseOver(" + i +",\""+InputName+"\")'  onclick='beClick(" + i + ",\""+InputName+"\")'>" + array[i] + "</div>"; 
		}
		else
		{
			document.getElementById(InputName+"search_suggest").innerHTML+="<div id='"+InputName+"item" + i + "' style=\"width:"+area_width_list+"\" class='item_normal' onmouseover='beMouseOver(" + i +",\""+InputName+"\")'  onclick='beClick(" + i + ",\""+InputName+"\")'>"+"<span>" + array[i] + "</span></div>"; 
		}
		
	} 
	if(array[i]!="" && i==(array.length-1))
	{ 
		if(InputName == "kw")
		{
			document.getElementById(InputName+"search_suggest").innerHTML+="<div id='"+InputName+"item" + i + "' style=\"width:"+kw_width_list+"\" align=right class='item_normal' onmouseover='beMouseOver(" + i +",\""+InputName+"\")'  onclick='beClick(" + i + ",\""+InputName+"\")'>" + "<span class=\"sclose\" onMouseOver=\"tdMOver(this)\" onMouseOut=\"tdMOut(this)\">"+"<u>"+array[i]+"</u></span>" + "</div>"; 
		}
		else
		{
			document.getElementById(InputName+"search_suggest").innerHTML+="<div id='"+InputName+"item" + i + "' style=\"width:"+area_width_list+"\" align=right class='item_normal' onmouseover='beMouseOver(" + i +",\""+InputName+"\")'  onclick='beClick(" + i + ",\""+InputName+"\")'>" + "<span class=\"sclose\" onMouseOver=\"tdMOver(this)\" onMouseOut=\"tdMOut(this)\">"+"<u>"+array[i]+"</u></span>" + "</div>"; 
		}
	}
}//for循环
}//函数

//函数鼠标经过效果 
function beMouseOverEFF(i,InputName){ 
	if ((i>=0)&(i<array.length-1))
	{ 
		document.getElementById(InputName+"item" + i).className="item_high";
		document.getElementById(InputName).value=array[i]; 
	} 
}
//函数鼠标移开效果 
function beMouseOutEFF(i,InputName)
{
	if ((i>=0)&(i<=array.length-1))
	{
		document.getElementById(InputName+"item" + i).className="item_normal"; 
	}
} 
//函数鼠标经过 
function beMouseOver(i,InputName)
{
	document.getElementById(InputName).focus(); 
	beMouseOutEFF(zz,InputName); 
	zz=i;
	/*beMouseOverEFF(zz,InputName);*/ 
	if ((i>=0)&(i<array.length-1))
	{ 
		document.getElementById(InputName+"item" + i).className="item_high";
	} 
} 

//函数单击 
function beClick(i,InputName)
{
	if(i != (array.length-1) && i>=0)
	{
		document.getElementById(InputName).value=array[i]; 
		document.getElementById(InputName).className="key_normal"; 
		document.getElementById(InputName+"search_suggest").className="suggest_hidden"; 
		document.getElementById(InputName).focus();
		document.getElementById(InputName).select();
	}
	else
	{
		document.getElementById(InputName).className="key_normal"; 
		document.getElementById(InputName+"search_suggest").className="suggest_hidden"; 
		document.getElementById(InputName).focus();
		document.getElementById(InputName).select();
	}
	choose_flag = "yes";
	zz=-1
}

//焦点移出 
function beOnBlur(InputName)
{
	if(zz>=0)
	{
		beClick(zz,InputName);
	}
	if(zz==-1 || choose_flag == "no")
	{//choose_flag = "yes";
		document.getElementById(InputName).className="key_normal"; 
		document.getElementById(InputName+"search_suggest").className="suggest_hidden";
	}
	zz=-1;
	
	if(InputName == "area")
	{
		if(document.form1.area.value == "")
		{
			document.form1.area.value='全市';
		}
	}
}

//焦点进入 
function beOnFocus(InputName)
{
	if(InputName == "area")
	{
		if(document.form1.area.value == "全市")
		{
			document.form1.area.value='';
		}
	}
}

//方向键和tab键接收函数 
function beKeyDown(InputName,event){ 
//往下按 
if (event.keyCode==40)
{ 
	if(zz==array.length-2)
	{
		beMouseOutEFF(zz,InputName);
		zz =-1;
	}
	
	if(zz<array.length-2)
	{
		beMouseOutEFF(zz++,InputName);
		beMouseOverEFF(zz,InputName);
		document.getElementById(InputName).value=array[zz];
	}
} 
//往上按 
if (event.keyCode==38)
{ 
	if (zz==0)
	{
		beMouseOutEFF(zz,InputName);
		document.getElementById(InputName).value=array[zz];
		zz = array.length-1;
	}
	
	if (zz>0)
	{
		beMouseOutEFF(zz--,InputName);
		beMouseOverEFF(zz,InputName);
		document.getElementById(InputName).value=array[zz];
	}
} 
//按回车
if (event.keyCode==13)
{ 
	if (zz!=-1)
	{
		beClick(zz,InputName);
	} 
}
//按TAB 
if (event.keyCode==9)
{
	beClick(zz,InputName);
}
} 

//beKeyUp事件。与服务器通信 
function beKeyUp(InputName,Url,event)
{
	if(event.keyCode!=13&event.keyCode!=9&event.keyCode!=38&event.keyCode!=40)
	{ 
		if (document.getElementById(InputName).value.length<1)
		{
			document.getElementById(InputName).className="key_normal"; 
			document.getElementById(InputName+"search_suggest").className="suggest_hidden";
		}
		else //if(document.getElementById(InputName).value.length>=1)
		{
			var validate_number = Math.random();
			Url = Url + document.getElementById(InputName).value+"&validate_number="+validate_number;
			
			AjaxObj = getXmlHttpRequestObject();
			//AjaxObj.open("post",Url,false);
			AjaxObj.open("GET",Url, false);
			
			AjaxObj.setRequestHeader('Content-type','application/x-www-form-urlencoded');
			//AjaxObj.onreadystatechange = processRequest;
			AjaxObj.send(null);
			
			sunjg = AjaxObj.responseText;
			array=new Array();
			if(sunjg.length >0)
			{
				begin_pos = 0;
				end_pos = sunjg.indexOf("\\",begin_pos);
				while(end_pos > 0)
				{
					tmp_str = sunjg.slice(begin_pos,end_pos);
					array.push(tmp_str);
					begin_pos = end_pos+1;
					end_pos = sunjg.indexOf("\\",begin_pos);
				}
			}
			else
			{
				document.getElementById(InputName).className="key_normal"; 
				document.getElementById(InputName+"search_suggest").className="suggest_hidden";
			}
			
			if (array.length>0)
			{
				buildList(InputName); 
				document.getElementById(InputName).className="key_abnormal"; 
				document.getElementById(InputName+"search_suggest").className="search_suggest"; 
			}
		}
	}
}

function SuggestShow(InputName,Url,input_width,other_info)
{
	if(InputName == "area")
	{
		area_width_src =input_width;
	}
	else if(InputName == "kw")
	{
		kw_width_src =input_width;
	}
	
	document.write("<div style='position:relative;z-index:200"+";'>");
	document.write("<input id=\""+InputName+"\" size="+input_width+" "+ other_info+" type=\"text\" name=\""+InputName+"\" class=\"key_normal\" onKeyDown=\"beKeyDown('"+InputName+"',"+"event"+")\" onKeyUp=\"beKeyUp('"+InputName+"','"+Url+'&'+InputName+'='+"',"+"event"+")\" onfocus=\"beOnFocus('"+InputName+"')\" onblur=\"beOnBlur('"+InputName+"')\" autoComplete=\"off\"\"/>");
	//alert("<input id=\""+InputName+"\" size="+input_width+" "+ other_info+" type=\"text\" name=\""+InputName+"\" class=\"key_normal\" onKeyDown=\"beKeyDown('"+InputName+"')\" onKeyUp=\"beKeyUp('"+InputName+"','"+Url+'&'+InputName+'='+"')\" onfocus=\"beOnFocus('"+InputName+"')\" onblur=\"beOnBlur('"+InputName+"')\" autoComplete=\"off\"\"/>");
	document.write("<div id=\""+InputName+"search_suggest\" class=\"suggest_hidden\">");
	document.write("</div></div>")
}

function getXmlHttpRequestObject() {
	if (window.XMLHttpRequest) {
		return new XMLHttpRequest();
	} else if(window.ActiveXObject) {
		return new ActiveXObject("Microsoft.XMLHTTP");
	} else {
		alert("Your Browser Sucks!\nIt's about time to upgrade don't you think?");
	}
}

function processRequest()
{
	if(AjaxObj.readyState == 4)
	{
		if(AjaxObj.status == 200)
		{
			if(AjaxObj.responseText!= "")
			{
				sunjg = AjaxObj.responseText;
			}
			else
			{
				sunjg = "";
			}
		}
		else
		{ 
			alert("您所请求的页面有异常。")
		}
	}
}