var displaymode="always";//"oncepersession"只显示一次，"always"每次显示
var enablefade="yes" //("yes"显示淡入效果, "no"无淡入效果)
var autohidebox=["no", 5] //设置多少称关闭浮动层 ["yes"x秒自动关闭设置有效果"no"无效,即不自动关闭]
var showonscroll="yes" //随滚动条滚动 ("yes"/"no)
var IEfadelength=1 //fade in duration for IE, in seconds
var Mozfadedegree=0.05 //fade in degree for NS6+ (number between 0 and 1. Recommended max: 0.2)
if (parseInt(displaymode)!=NaN)
  var random_num=Math.floor(Math.random()*displaymode)
function displayfadeinbox(){
  var ie=document.all && !window.opera
  var dom=document.getElementById
  iebody=(document.compatMode=="CSS1Compat")? document.documentElement : document.body
  objref=(dom)? document.getElementById("fadeinbox") : document.all.fadeinbox
  
  var scroll_top=(ie)? iebody.scrollTop : window.pageYOffset
  var docwidth=(ie)? iebody.clientWidth : window.innerWidth
  docheight=(ie)? iebody.clientHeight: window.innerHeight
  var objheight=objref.docheight
  
  objref.style.width="50%";
  objref.style.right="5.5%";
  objref.style.top=scroll_top+get_div_y('hr_pos')+28+"px"
  
  sunjg_objref=(dom)? document.getElementById("sunjg_1") : document.all.sunjg_1
  //alert("可见区域高："+document.body.clientHeight+"正文全文高："+document.body.scrollHeight+"被卷去的高："+document.body.scrollTop+"正文部分上："+window.screenTop+"分辨率的高："+window.screen.Height+"可用工作区高度："+window.screen.availHeight);

if (showonscroll=="yes")
  showonscrollvar=setInterval("staticfadebox()", 50)
if (enablefade=="yes" && objref.filters){
  objref.filters[0].duration=IEfadelength
  objref.filters[0].Apply()
  objref.filters[0].Play()
  }
  objref.style.visibility="visible"
  if (objref.style.MozOpacity){
  if (enablefade=="yes")
  mozfadevar=setInterval("mozfadefx()", 90)
  else{
  objref.style.MozOpacity=1
  controlledhidebox()
  }
  }
  else
  controlledhidebox()
  }
function mozfadefx(){
  if (parseFloat(objref.style.MozOpacity)<1)
  objref.style.MozOpacity=parseFloat(objref.style.MozOpacity)+Mozfadedegree
  else{
  clearInterval(mozfadevar)
  controlledhidebox()
  }
  }
function staticfadebox(){
  var ie=document.all && !window.opera
  var scroll_top=(ie)? iebody.scrollTop : window.pageYOffset
  //objref.style.top=scroll_top+docheight/2-objheight/2+130+"px"
  objref.style.top=scroll_top+get_div_y('hr_pos')+28+"px"
  }
function hidefadebox(){
  objref.style.visibility="hidden"
  if (typeof showonscrollvar!="undefined")
  clearInterval(showonscrollvar)
  }
function controlledhidebox(){
  if (autohidebox[0]=="yes"){
  var delayvar=(enablefade=="yes" && objref.filters)? (autohidebox[1]+objref.filters[0].duration)*10 : autohidebox[1]*10
  setTimeout("hidefadebox()", delayvar)
  }
  }
function initfunction(){
  setTimeout("displayfadeinbox()", 10)
  }
function get_cookie(Name) {
  var search = Name + "="
  var returnvalue = ""
  if (document.cookie.length > 0) {
  offset = document.cookie.indexOf(search)
  if (offset != -1) {
  offset += search.length
  end = document.cookie.indexOf(";", offset)
  if (end == -1)
  end = document.cookie.length;
  returnvalue=unescape(document.cookie.substring(offset, end))
  }
  }
  return returnvalue;
  }

if (displaymode=="oncepersession" && get_cookie("fadedin")=="" || displaymode=="always" || parseInt(displaymode)!=NaN && random_num==0){
  if (window.addEventListener)
  window.addEventListener("load", initfunction, false)
  else if (window.attachEvent)
  window.attachEvent("onload", initfunction)
  else if (document.getElementById)
  window.onload=initfunction
  document.cookie="fadedin=yes"
}

function getElementPos(elementId) {
var ua = navigator.userAgent.toLowerCase();
var isOpera = (ua.indexOf('opera') != -1);
var isIE = (ua.indexOf('msie') != -1 && !isOpera); // not opera spoof

var el = document.getElementById(elementId);
if(el.parentNode === null || el.style.display == 'none') {
   return false;
}
var parent = null;
var pos = [];     
var box;     
if(el.getBoundingClientRect)    //IE
{         
   box = el.getBoundingClientRect();
   var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop);
   var scrollLeft = Math.max(document.documentElement.scrollLeft, document.body.scrollLeft);
   return {x:box.left + scrollLeft, y:box.top + scrollTop};
}else if(document.getBoxObjectFor)    // gecko    
{
   box = document.getBoxObjectFor(el); 
   var borderLeft = (el.style.borderLeftWidth)?parseInt(el.style.borderLeftWidth):0; 
   var borderTop = (el.style.borderTopWidth)?parseInt(el.style.borderTopWidth):0; 
   pos = [box.x - borderLeft, box.y - borderTop];
} else    // safari & opera    
{
   pos = [el.offsetLeft, el.offsetTop]; 
   parent = el.offsetParent;     
   if (parent != el) { 
    while (parent) { 
   pos[0] += parent.offsetLeft; 
   pos[1] += parent.offsetTop; 
   parent = parent.offsetParent;
    } 
   }   
   if (ua.indexOf('opera') != -1 || ( ua.indexOf('safari') != -1 && el.style.position == 'absolute' )) { 
    pos[0] -= document.body.offsetLeft;
    pos[1] -= document.body.offsetTop;         
   }    
}              
if (el.parentNode) { 
   parent = el.parentNode;
    } else {
   parent = null;
    }
while (parent && parent.tagName != 'BODY' && parent.tagName != 'HTML') { // account for any scrolled ancestors
   pos[0] -= parent.scrollLeft;
   pos[1] -= parent.scrollTop;
   if (parent.parentNode) {
    parent = parent.parentNode;
   } else {
    parent = null;
   }
}
return {x:pos[0], y:pos[1]};
}

function get(divId)
{
   var pos=getElementPos(divId);
   alert("距左边距离"+ pos.x +",距上边距离"+pos.y);

}
function get_div_x(divId)
{
   var pos=getElementPos(divId);
   return pos.x;

}
function get_div_y(divId)
{
   var pos=getElementPos(divId);
   return pos.y;

}
