/**
 * Created by wangjian on 15/6/24.
 */
$(function(){
    /*
    加载评论
    by:王健 at:2015-06-24
    */
    load_replay();
});
function load_replay(){
    /**
     * 修改加载函数
     * by:王健 at:2015-06-24
     */
    $.post('/cp/'+company_id+'/query_replay_news_by_id', {'id': news_id, 'start': start}, function(data){
        if(!data.success || !data.result){
            return
        }
        start = start+data.result.length;
        EJSTemplateRender('/static/cp_manage/phone/ejs/news_replay.ejs', {'list':data.result}).done(function(html){
            $('body').append(html);
        });
    },'json');
}