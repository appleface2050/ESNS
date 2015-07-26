/**
 * Date: 15/2/14
 * Time: 18:31
 * Email:fanjnwei003@163.com
 * Athor:范俊伟
 */
/**
 * 菜单数据
 by: 范俊伟 at:2015-04-23
 * @type {{title: string, menus: *[]}[]}
 */
/**
 *  管理员菜单
 by: 范俊伟 at:2015-06-12
 *  增加集团展示设置
 by: 尚宗凯 at:2015-06-15
 *  增加创建集团,创建公司等
 by: 尚宗凯 at:2015-06-16
 *  增加测试的内容
 by：尚宗凯 at：2015-06-22
 * @type {*[]}
 */
admin_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"},
    {
        'title': '客服', 'icon': 'icon-user',view_id: "service_manage", 'menus': [
        {
            'title': '创建集团',
            'view_id': 'customer_service_create_big_company'
        },
        {
            'title': '创建公司',
            'view_id': 'customer_service_create_company'
        },
        {
            'title': '集团默认展示',
            'view_id': 'customer_service_manage'
        },
        {
            'title': '系统新闻设置',
            'view_id': 'customer_service_sys_news'
        },
        {
            'title': '新建系统新闻',
            'view_id': 'customer_service_create_sys_news'
        },
        {
            'title': '公司管理',
            'view_id': 'customer_service_admin_company_manage'
        },
        {
            'title': '创建系统banner',
            'view_id': 'customer_service_create_sys_banner'
        },
        {
            'title': '系统banner设置',
            'view_id': 'customer_service_set_sys_banner'
        },
        {
            'title': '创建系统栏目',
            'view_id': 'customer_service_create_sys_column'
        },
        {
            'title': '系统栏目设置',
            'view_id': 'customer_service_set_sys_column'
        }
    ]
    },
    //测试使用
    //{
    //    'title': '企业管理员', 'icon': 'icon-user',view_id: "company_manage", 'menus': [
    //    {
    //        'title': '公司管理',
    //        'view_id': 'customer_service_manage'
    //    },
    //            {
    //        'title': '新闻管理',
    //        'view_id': 'customer_service_create_company_news'
    //    },
    //            {
    //        'title': '新闻列表',
    //        'view_id': 'customer_service_company_news'
    //    },
    //            {
    //        'title': '公司banner',
    //        'view_id': 'customer_service_company_banner'
    //    },
    //            {
    //        'title': '创建banner',
    //        'view_id': 'customer_service_create_company_banner'
    //    },
    //            {
    //        'title': '新闻栏目',
    //        'view_id': 'customer_service_company_news_column'
    //    },
    //            {
    //        'title': '权限设置',
    //        'view_id': 'customer_service_company_jurisdiction'
    //    }
    //]
    //}
];
/**
 *  客服菜单
 by: 范俊伟 at:2015-06-12
 * @type {*[]}
 */
kf_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"}
];

/**
 *  会计菜单
 by: 范俊伟 at:2015-06-12
 * @type {*[]}
 */
accountancy_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"}
];


/**
 *  推广员菜单
 by: 范俊伟 at:2015-06-12
 * @type {*[]}
 */
promoter_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"}
];

/**
 *  企业管理员菜单
 by: 尚宗凯 at:2015-06-18
 * @type {*[]}
 */
company_manager_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"},
    {
        'title': '企业管理员', 'icon': 'icon-user',view_id: "company_manage", 'menus': [
        {
            'title': '公司管理',
            'view_id': 'customer_service_company_manage'
        },
           {
            'title': '项目管理',
            'view_id': 'customer_service_company_project_manage'
        },
                {
            'title': '公司banner',
            'view_id': 'customer_service_company_banner'
        },
                {
            'title': '创建banner',
            'view_id': 'customer_service_create_company_banner'
        },
                {
            'title': '新闻栏目',
            'view_id': 'customer_service_company_news_column'
        },
                {
            'title': '权限设置',
            'view_id': 'customer_service_company_jurisdiction'
        },
                {
            'title': '员工管理',
            'view_id': 'customer_service_employee_manage'
        }
    ]
    },
     //新闻管理
    {
        'title': '新闻管理', 'icon': 'icon-user',view_id: "news_manage", 'menus': [
        {
            'title': '企业资讯',
            'view_id': 'customer_service_news_company_news'
        },
                {
            'title': '公司简介',
            'view_id': 'customer_service_news_company_profile'
        },
                {
            'title': '企业文化',
            'view_id': 'customer_service_news_company_culture'
        },
                {
            'title': '公司业绩',
            'view_id': 'customer_service_news_company_performance'
        }
    ]
    },
    {
        'title': '综合管理', 'icon': 'icon-user',view_id: "integrated_manage", 'menus': [
           {
            'title': '文件传达',
            'view_id': 'customer_service_company_integrated_file_convey'
        },
           {
            'title': '通知公告',
            'view_id': 'customer_service_company_integrated_notice_inform'
        },
          {
            'title': '宣传报道',
            'view_id': 'customer_service_company_integrated_publicity_contribute'
        },
         {
            'title': '技术指导',
            'view_id': 'customer_service_company_integrated_technical_guidance'
        },
         {
            'title': '工程管理',
            'view_id': 'customer_service_company_integrated_engineering_supervision'
        },

                {
            'title': '信息发布',
            'view_id': 'customer_service_company_integrated_information_publish'
        },
           {
            'title': '报审资料',
            'view_id': 'customer_service_company_integrated_report_data'
        }
    ]
    }
];

