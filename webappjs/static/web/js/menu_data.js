/**
 * Date: 15/2/14
 * Time: 18:31
 * Email:fanjnwei003@163.com
 * Athor:范俊伟
 */
/**
 * 未选项项目时菜单
 by: 范俊伟 at:2015-02-14
 * @type {{title: string, menus: *[]}[]}
 */
no_project_menu = [
    {
        'title': '', 'menus': [
        {
            'title': '所有项目',
            'icon': 'glyphicon-list-alt',
            'view_id': 'all_project'
        },
        {
            'title': '我关注的项目',
            'view_id': 'my_project',
            'icon': 'glyphicon-star'
        },
        {
            'title': '新建项目',
            'view_id': 'create_project',
            'icon': 'glyphicon-plus'
        }

    ]
    }
];
/**
 * 选择项目后菜单
 by: 范俊伟 at:2015-02-14
 修改菜单显示方式
 by: 范俊伟 at:2015-03-01
 * @type {{title: string, menus: *[]}[]}
 */
project_menu = [
    {
        'title': '', 'menus': [
        {
            'title': '项目信息',
            'icon': 'glyphicon-book',
            'view_id': 'project_info'
        },
        {
            'title': '系统消息',
            'view_id': 'system_message',
            'icon': 'glyphicon-envelope'
        },
        {
            'title': '项目公告',
            'view_id': 'project_message',
            'icon': 'glyphicon-envelope',
            "permission": "xmjl"
        },
        {
            'title': '加入请求',
            'view_id': 'join_request',
            'icon': 'glyphicon-question-sign',
            "permission": "manager"
        },
        {
            'title': '成员管理',
            'icon': 'glyphicon-user',
            'view_id': 'manage_user',
            "permission": "manager"
        },
        {
            'title': '消息',
            'view_id': 'message',
            'icon': 'glyphicon-envelope'
        },
        {
            'title': '应用',
            'view_id': 'application',
            'icon': 'glyphicon-th-large'
        },
        //{
        //    'title': '统计',
        //    'view_id': 'statistic',
        //    'icon': 'glyphicon-stats'
        //}
    ]
    }
];
