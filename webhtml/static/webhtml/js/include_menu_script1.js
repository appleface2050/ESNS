/**
 * 左侧边栏显示隐藏切换
 * Created by 尚宗凯 on 2015/3/16.
 * 解决无法切换问题
 * by 尚宗凯 on 2015/3/17
 */
$(document).ready(function(){
     qiehuan(2);
	$("#firstpane .menu_body:eq(0)").hide();
	$("#firstpane .menu_body:eq(1)").show();
	$("#firstpane p.menu_head").click(function(){
		$(this).addClass("current").next("div.menu_body").slideToggle(300).siblings("div.menu_body").slideUp("slow");
		$(this).siblings().removeClass("current");
	});
});