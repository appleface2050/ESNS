# coding=utf-8
# Date:2015/1/10
# Email: wangjian2254@icloud.com

__author__ = u'王健'

"""
应用界面，整理成一个统一的由服务器端维护的 界面数据源

修改部分节点的 类型 和名字
by:王健 at:2015-1-17
修改部分节点图片内容
by:王健 at:2015-1-26
修改工程检查类型,修改2.0版本的typeflag
by:王健 at:2015-1-31

"""
"""
list: ios 界面应用类型
columnlist: 分栏按钮 + listview(android)
images: 多张图片+文字（不是每个图一段文字，而是类似微信朋友圈多张图配一个文字），顶、踩、评论
bgimages: 多张图+文字 , 处理意见，顶、踩、评论
files: 多（图片+文档）+文字（文档的标题或者输入的一段文字）
gyslist: 供应商表格列表
wuzilist: 物资采购记录和物资入库记录
wuzioutlist:物资出库记录

by:王健 at:2015-1-31
修改节点名字
by:王健 at:2015-2-10
设置节点图片
by:王健 at:2015-2-12
修改节点名字
by:王健 at:2015-3-4
增加节点施工总平面图
by:尚宗凯 at:2015-3-25
修改节点施工总平面图
by:尚宗凯 at:2015-3-27
节点图片名称修改
by:尚宗凯 at:2015-4-8
"""
#应用界面
# appitem = {"type": 'app', 'children':[
#     {"flag": 'gong_cheng_ri_zhi', 'name': u'施工日志', 'icon': 'shigongrizhi1.png', 'typeflag': 'log'},
#     {"flag": 'gong_cheng_xing_xiang_jin_du', 'name': u'工程形象进度', 'icon': 'gongchengxingxiangjindu1.png', 'typeflag': 'images'},
#     {"flag": 'gong_zuo_ying_xiang_ji_lu', 'name': u'工作影像记录', 'icon': 'gongzuoyingxiangjilu1.png', 'typeflag': 'images'},
#     {"flag": 'gong_cheng_jian_cha', 'name': u'工程检查', 'icon': 'gongchengjiancha11.png', 'typeflag': 'columnlist', 'children': [
#                                                                 {"flag": 'zhi_liang_jian_cha', 'name': u'工程实体质量检查', 'icon': 'log1.png', 'typeflag': 'jc'},
#                                                                 {"flag": 'an_quan_wen_ming_jian_cha', 'name': u'现场安全文明检查', 'icon': 'log1.png', 'typeflag': 'jc'},
#
#
#                                                                                             ]},
#     {"flag": 'xing_xiang_zhan_shi', 'name': u'优质工程展示', 'icon': 'xingxiangzhanshi1.png', 'typeflag': 'columnlist', 'children': [
#                                                                 {"flag": 'gong_cheng_shi_ti', 'name': u'工程实体', 'icon': 'log1.png', 'typeflag': 'images'},
#                                                                 {"flag": 'an_quan_wen_ming', 'name': u'安全文明', 'icon': 'log1.png', 'typeflag': 'images'},
#
#                                                                                             ]},
#     {"flag": 'bao_guang_jing_gao', 'name': u'违章曝光', 'icon': 'weizhangbaoguang1.png', 'typeflag': 'bgimages'},
#     {"flag": 'xiang_mu_wen_hua', 'name': u'项目文化展示', 'icon': 'xiangmuwenhua1.png', 'typeflag': 'images'},
#     {"flag": 'wu_zi_guan_li', 'name': u'工程物资管理', 'icon': 'wuziguanli1.png', 'typeflag': 'list', 'children': [
#                                                                 {"flag": 'gong_ying_shang_ming_lu', 'name': u'材料设备供应商名录', 'icon': 'gongyingshangminglu1.png', 'typeflag': 'gyslist'},
#                                                                 {"flag": 'wu_zi_cai_gou_ji_lu', 'name': u'物资采购记录', 'icon': 'wuzicaigoujilu1.png', 'typeflag': 'wuzilist'},
#                                                                 {"flag": 'wu_zi_ru_ku_ji_lu', 'name': u'物资入库记录', 'icon': 'wuzirukujilu1.png', 'typeflag': 'wuzilist'},
#                                                                 {"flag": 'wu_zi_chu_ku_ji_lu', 'name': u'物资出库记录', 'icon': 'wuzichukujilu1.png', 'typeflag': 'wuzioutlist'},
#                                                                                             ]},
#     {"flag": 'gong_cheng_jin_du', 'name': u'施工进度计划', 'icon': 'gongchengjindujihua1.png', 'typeflag': 'columnlist', 'children':[
#                                                                 {"flag": 'jin_du_ji_hua', 'name': u'施工进度计划', 'icon': 'log1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'jin_du_fen_xi', 'name': u'进度执行情况小结', 'icon': 'log1.png', 'typeflag': 'files'},
#
#                                                                                             ]},
#     {"flag": 'wen_jian_chuan_da', 'name': u'文件传达', 'icon': 'wenjianchuanda1.png', 'typeflag': 'list', 'children': [
#                                                                 {"flag": 'wen_jian_tong_zhi', 'name': u'文件通知', 'icon': 'wenjiantongzhi1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'hui_yi_ji_yao', 'name': u'会议纪要', 'icon': 'huiyijiyao1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'jia_fang_jian_li_fa_wen', 'name': u'甲方监理发文', 'icon': 'jiafangjianlifawen1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'xuan_chuan_bao_dao', 'name': u'宣传报导', 'icon': 'xuanchuanbaodao1.png', 'typeflag': 'files'},
#                                                                                             ]},
#
#     {"flag": 'gong_cheng_yu_jue_suan', 'name': u'工程预决算', 'icon': 'gongchengyujuesuan1.png', 'typeflag': 'list', 'children': [
#                                                                 {"flag": 'gong_cheng_liang_yu_suan', 'name': u'工程量预算', 'icon': 'gongchengliangyusuan1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'ge_lei_jie_suan', 'name': u'各类结算', 'icon': 'geleijiesuan1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'chan_zhi_bao_biao', 'name': u'产值报表', 'icon': 'chanzhibaobiao1.png', 'typeflag': 'files'},
#                                                                                             ]},
#     {"flag": 'shi_ce_shi_liang', 'name': u'实测实量报告', 'icon': 'shiceshiliangbaogao1.png', 'typeflag': 'files'},
#
#
#     {"flag": 'zhi_shi_ku', 'name': u'工程知识库', 'icon': 'zhishiku1.png', 'typeflag': 'list', 'children': [
#                                                                 {"flag": 'gui_fan_biao_zhun', 'name': u'规范标准', 'icon': 'guifanbiaozhun1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'tu_ji', 'name': u'图集', 'icon': 'tuji1.png', 'typeflag': 'files'},
#                                                                 {"flag": 'qi_ta_zhi_shi', 'name': u'其他知识', 'icon': 'qitazhishi1.png', 'typeflag': 'files'},
#                                                                                             ]},
#     {"flag": 'shi_gong_zong_ping_mian_tu', 'name': u'施工总平面图', 'icon': 'shigongzongpingmiantu.png', 'typeflag': 'files'},
#     {"flag": 'wo_xing_wo_xiu', 'name': u'我型我秀', 'icon': 'woxingwoxiu1.png', 'typeflag': 'images'},
# ]}

appitem = {"type": 'app', 'children':[
    {"flag": 'gong_cheng_ri_zhi', 'name': u'施工日志', 'icon': 'shi_gong_ri_zhi4.png', 'typeflag': 'log'},
    {"flag": 'gong_cheng_xing_xiang_jin_du', 'name': u'工程形象进度', 'icon': 'gong_cheng_xing_xiang_jin_du4.png', 'typeflag': 'images'},
    {"flag": 'gong_zuo_ying_xiang_ji_lu', 'name': u'工作影像记录', 'icon': 'gong_zuo_ying_xiang_ji_lu4.png', 'typeflag': 'images'},
    {"flag": 'gong_cheng_jian_cha', 'name': u'工程检查', 'icon': 'gong_cheng_jian_cha4.png', 'typeflag': 'list', 'children': [
                                                                {"flag": 'zhi_liang_jian_cha', 'name': u'工程实体质量检查', 'icon': 'gong_cheng_shi_ti_zhi_liang_jian_cha4.png', 'typeflag': 'jc'},
                                                                {"flag": 'an_quan_wen_ming_jian_cha', 'name': u'现场安全文明检查', 'icon': 'xian_chang_an_quan_wen_ming_jian_cha.png', 'typeflag': 'jc'},


                                                                                            ]},
    {"flag": 'xing_xiang_zhan_shi', 'name': u'优质工程展示', 'icon': 'you_zhi_gong_cheng_zhan_shi4.png', 'typeflag': 'columnlist', 'children': [
                                                                {"flag": 'gong_cheng_shi_ti', 'name': u'工程实体', 'icon': 'gong_cheng_shi_ti4.png', 'typeflag': 'images'},
                                                                {"flag": 'an_quan_wen_ming', 'name': u'安全文明', 'icon': 'an_quan_wen_ming4.png', 'typeflag': 'images'},

                                                                                            ]},
    {"flag": 'bao_guang_jing_gao', 'name': u'违章曝光', 'icon': 'wei_zhang_bao_guang4.png', 'typeflag': 'bgimages'},
    {"flag": 'xiang_mu_wen_hua', 'name': u'项目文化展示', 'icon': 'xiang_mu_wen_hua_zhan_shi3.png', 'typeflag': 'images'},
    {"flag": 'wu_zi_guan_li', 'name': u'工程物资管理', 'icon': 'gong_cheng_wu_zi_guan_li4.png', 'typeflag': 'list', 'children': [
                                                                {"flag": 'gong_ying_shang_ming_lu', 'name': u'材料设备供应商名录', 'icon': 'cai_liao_she_bei_gong_ying_shang_ming_lu4.png', 'typeflag': 'gyslist'},
                                                                {"flag": 'wu_zi_cai_gou_ji_lu', 'name': u'物资采购记录', 'icon': 'wu_zi_cai_gou_ji_lu4.png', 'typeflag': 'wuzilist'},
                                                                {"flag": 'wu_zi_ru_ku_ji_lu', 'name': u'物资入库记录', 'icon': 'wu_zi_ru_ku_ji_lu4.png', 'typeflag': 'wuzilist'},
                                                                {"flag": 'wu_zi_chu_ku_ji_lu', 'name': u'物资出库记录', 'icon': 'wu_zi_chu_ku_ji_lu4.png', 'typeflag': 'wuzioutlist'},
                                                                                            ]},
    {"flag": 'gong_cheng_jin_du', 'name': u'施工进度计划', 'icon': 'shi_gong_jin_du_ji_hua4.png', 'typeflag': 'columnlist', 'children':[
                                                                {"flag": 'jin_du_ji_hua', 'name': u'施工进度计划', 'icon': 'shi_gong_jin_du_ji_hua4.png', 'typeflag': 'files'},
                                                                {"flag": 'jin_du_fen_xi', 'name': u'进度执行情况小结', 'icon': 'jin_du_zhi_xing_qing_kuang_xiao_jie4.png', 'typeflag': 'files'},

                                                                                            ]},
    {"flag": 'wen_jian_chuan_da', 'name': u'文件传达', 'icon': 'wen_jian_chuan_da4.png', 'typeflag': 'list', 'children': [
                                                                {"flag": 'wen_jian_tong_zhi', 'name': u'文件通知', 'icon': 'wen_jian_tong_zhi4.png', 'typeflag': 'files'},
                                                                {"flag": 'hui_yi_ji_yao', 'name': u'会议纪要', 'icon': 'hui_yi_ji_yao4.png', 'typeflag': 'files'},
                                                                {"flag": 'jia_fang_jian_li_fa_wen', 'name': u'甲方监理发文', 'icon': 'jia_fang_jian_li_fa_wen4.png', 'typeflag': 'files'},
                                                                {"flag": 'xuan_chuan_bao_dao', 'name': u'宣传报导', 'icon': 'xuan_chuan_bao_dao4.png', 'typeflag': 'files'},
                                                                                            ]},

    {"flag": 'gong_cheng_yu_jue_suan', 'name': u'工程预决算', 'icon': 'gong_cheng_yu_jue_suan4.png', 'typeflag': 'list', 'children': [
                                                                {"flag": 'gong_cheng_liang_yu_suan', 'name': u'工程量预算', 'icon': 'gong_cheng_liang_yu_suan4.png', 'typeflag': 'files'},
                                                                {"flag": 'ge_lei_jie_suan', 'name': u'各类结算', 'icon': 'ge_lei_jie_suan4.png', 'typeflag': 'files'},
                                                                {"flag": 'chan_zhi_bao_biao', 'name': u'产值报表', 'icon': 'chan_zhi_bao_biao4.png', 'typeflag': 'files'},
                                                                                            ]},
    {"flag": 'shi_ce_shi_liang', 'name': u'实测实量报告', 'icon': 'shi_ce_shi_liang_bao_gao4.png', 'typeflag': 'files'},


    {"flag": 'zhi_shi_ku', 'name': u'工程知识库', 'icon': 'gong_cheng_zhi_shi_ku4.png', 'typeflag': 'list', 'children': [
                                                                {"flag": 'gui_fan_biao_zhun', 'name': u'规范标准', 'icon': 'gui_fan_biao_zhun4.png', 'typeflag': 'files'},
                                                                {"flag": 'tu_ji', 'name': u'图集', 'icon': 'tu_ji4.png', 'typeflag': 'files'},
                                                                {"flag": 'qi_ta_zhi_shi', 'name': u'其他知识', 'icon': 'qi_ta_zhi_shi4.png', 'typeflag': 'files'},
                                                                                            ]},
    {"flag": 'shi_gong_zong_ping_mian_tu', 'name': u'施工总平面图', 'icon': 'shi_gong_zong_ping_mian_tu4.png', 'typeflag': 'files'},
    {"flag": 'wo_xing_wo_xiu', 'name': u'我型我秀', 'icon': 'wo_xing_wo_xiu4.png', 'typeflag': 'images'},
    {"flag": 'ri_chang_xun_cha', 'name': u'日常巡查记录', 'icon': 'ri_chang_xun_cha_ji_lu4.png', 'typeflag': 'images'},
]}