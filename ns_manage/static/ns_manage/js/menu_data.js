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
 * @type {*[]}
 */
admin_menu_data = [
    {'title': '主页', 'icon': 'icon-home', view_id: "home"},
    {
        'title': '用户管理', 'icon': 'icon-user', 'menus': [
        {
            'title': '用户类型管理',
            'view_id': 'user_type_manage'
        }
    ]
    }
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