/**
 * jQuery EasyUI 1.2.4
 * 
 * Licensed under the GPL terms
 * To use it on other terms please contact us
 *
 * Copyright(c) 2009-2011 stworthy [ stworthy@gmail.com ] 
 * 
 */
(function($){
function _1(_2){
var _3=$.data(_2,"accordion").options;
var _4=$.data(_2,"accordion").panels;
var cc=$(_2);
if(_3.fit==true){
var p=cc.parent();
_3.width=p.width();
_3.height=p.height();
}
if(_3.width>0){
cc.width($.boxModel==true?(_3.width-(cc.outerWidth()-cc.width())):_3.width);
}
var _5="auto";
if(_3.height>0){
cc.height($.boxModel==true?(_3.height-(cc.outerHeight()-cc.height())):_3.height);
var _6=_4.length?_4[0].panel("header").css("height",null).outerHeight():"auto";
var _5=cc.height()-(_4.length-1)*_6;
}
for(var i=0;i<_4.length;i++){
var _7=_4[i];
var _8=_7.panel("header");
_8.height($.boxModel==true?(_6-(_8.outerHeight()-_8.height())):_6);
_7.panel("resize",{width:cc.width(),height:_5});
}
};
function _9(_a){
var _b=$.data(_a,"accordion").panels;
for(var i=0;i<_b.length;i++){
var _c=_b[i];
if(_c.panel("options").collapsed==false){
return _c;
}
}
return null;
};
function _d(_e,_f,_10){
var _11=$.data(_e,"accordion").panels;
for(var i=0;i<_11.length;i++){
var _12=_11[i];
if(_12.panel("options").title==_f){
if(_10){
_11.splice(i,1);
}
return _12;
}
}
return null;
};
function _13(_14){
var cc=$(_14);
cc.addClass("accordion");
if(cc.attr("border")=="false"){
cc.addClass("accordion-noborder");
}else{
cc.removeClass("accordion-noborder");
}
if(cc.find(">div[selected=true]").length==0){
cc.find(">div:first").attr("selected","true");
}
var _15=[];
cc.find(">div").each(function(){
var pp=$(this);
_15.push(pp);
_18(_14,pp,{});
});
cc.bind("_resize",function(e,_16){
var _17=$.data(_14,"accordion").options;
if(_17.fit==true||_16){
_1(_14);
}
return false;
});
return {accordion:cc,panels:_15};
};
function _18(_19,pp,_1a){
pp.panel($.extend({},_1a,{collapsible:false,minimizable:false,maximizable:false,closable:false,doSize:false,collapsed:pp.attr("selected")!="true",tools:[{iconCls:"accordion-collapse",handler:function(){
var _1b=$.data(_19,"accordion").options.animate;
if(pp.panel("options").collapsed){
_27(_19);
pp.panel("expand",_1b);
}else{
_27(_19);
pp.panel("collapse",_1b);
}
return false;
}}],onBeforeExpand:function(){
var _1c=_9(_19);
if(_1c){
var _1d=$(_1c).panel("header");
_1d.removeClass("accordion-header-selected");
_1d.find(".accordion-collapse").triggerHandler("click");
}
var _1d=pp.panel("header");
_1d.addClass("accordion-header-selected");
_1d.find("div.accordion-collapse").removeClass("accordion-expand");
},onExpand:function(){
var _1e=$.data(_19,"accordion").options;
_1e.onSelect.call(_19,pp.panel("options").title);
},onBeforeCollapse:function(){
var _1f=pp.panel("header");
_1f.removeClass("accordion-header-selected");
_1f.find("div.accordion-collapse").addClass("accordion-expand");
}}));
pp.panel("body").addClass("accordion-body");
pp.panel("header").addClass("accordion-header").click(function(){
$(this).find(".accordion-collapse").triggerHandler("click");
return false;
});
};
function _20(_21,_22){
var _23=$.data(_21,"accordion").options;
var _24=$.data(_21,"accordion").panels;
var _25=_9(_21);
if(_25&&_25.panel("options").title==_22){
return;
}
var _26=_d(_21,_22);
if(_26){
_26.panel("header").triggerHandler("click");
}else{
if(_25){
_25.panel("header").addClass("accordion-header-selected");
_23.onSelect.call(_21,_25.panel("options").title);
}
}
};
function _27(_28){
var _29=$.data(_28,"accordion").panels;
for(var i=0;i<_29.length;i++){
_29[i].stop(true,true);
}
};
function add(_2a,_2b){
var _2c=$.data(_2a,"accordion").options;
var _2d=$.data(_2a,"accordion").panels;
_27(_2a);
var pp=$("<div></div>").appendTo(_2a);
_2d.push(pp);
_18(_2a,pp,_2b);
_1(_2a);
_2c.onAdd.call(_2a,_2b.title);
_20(_2a,_2b.title);
};
function _2e(_2f,_30){
var _31=$.data(_2f,"accordion").options;
var _32=$.data(_2f,"accordion").panels;
_27(_2f);
if(_31.onBeforeRemove.call(_2f,_30)==false){
return;
}
var _33=_d(_2f,_30,true);
if(_33){
_33.panel("destroy");
if(_32.length){
_1(_2f);
var _34=_9(_2f);
if(!_34){
_20(_2f,_32[0].panel("options").title);
}
}
}
_31.onRemove.call(_2f,_30);
};
$.fn.accordion=function(_35,_36){
if(typeof _35=="string"){
return $.fn.accordion.methods[_35](this,_36);
}
_35=_35||{};
return this.each(function(){
var _37=$.data(this,"accordion");
var _38;
if(_37){
_38=$.extend(_37.options,_35);
_37.opts=_38;
}else{
_38=$.extend({},$.fn.accordion.defaults,$.fn.accordion.parseOptions(this),_35);
var r=_13(this);
$.data(this,"accordion",{options:_38,accordion:r.accordion,panels:r.panels});
}
_1(this);
_20(this);
});
};
$.fn.accordion.methods={options:function(jq){
return $.data(jq[0],"accordion").options;
},panels:function(jq){
return $.data(jq[0],"accordion").panels;
},resize:function(jq){
return jq.each(function(){
_1(this);
});
},getSelected:function(jq){
return _9(jq[0]);
},getPanel:function(jq,_39){
return _d(jq[0],_39);
},select:function(jq,_3a){
return jq.each(function(){
_20(this,_3a);
});
},add:function(jq,_3b){
return jq.each(function(){
add(this,_3b);
});
},remove:function(jq,_3c){
return jq.each(function(){
_2e(this,_3c);
});
}};
$.fn.accordion.parseOptions=function(_3d){
var t=$(_3d);
return {width:(parseInt(_3d.style.width)||undefined),height:(parseInt(_3d.style.height)||undefined),fit:(t.attr("fit")?t.attr("fit")=="true":undefined),border:(t.attr("border")?t.attr("border")=="true":undefined),animate:(t.attr("animate")?t.attr("animate")=="true":undefined)};
};
$.fn.accordion.defaults={width:"auto",height:"auto",fit:false,border:true,animate:true,onSelect:function(_3e){
},onAdd:function(_3f){
},onBeforeRemove:function(_40){
},onRemove:function(_41){
}};
})(jQuery);

