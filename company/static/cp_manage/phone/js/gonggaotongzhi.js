/**
 * Created by wangjian on 15/7/1.
 */
var page_start = 0;
function getRecordByColumnAndCompany(){
    /**
     * 根据栏目和公司加载数据
     * by:王健 at:2015-07-01
     * @type {string}
     */
    var url = '/cp/zhgl/'+company_id+"/"+column_id;
    httpRequest(url, {}).done(function (data) {
        if(!data.success || !data.result){
            return ;
        }
        EJSTemplateRender('cp_manage/phone/ejs/gonggaotongzhi.ejs', data).done(function (html) {
            $('#recordlist').append(html);
        })
    });
}
$(function(){
    getRecordByColumnAndCompany();
});