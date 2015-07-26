# coding=utf-8
__author__ = '王健'

from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='ueditorAll')
def ueditorAll(content, name, company_id=''):
    """
    过滤器标签，可根据是否是公司，配置url
    by:王健 at:2015-06-14
    :param content:
    :param name:
    :param company_id:
    :return:
    """
    html = '''
    <script type="text/javascript">
            <!--
            window.UEDITOR_HOME_URL = '%sueditor/%s';
            //-->
        </script>
        <script type="text/javascript" src="%sueditor/editor.min.js"></script>
        <script type="text/javascript" src="%sueditor/editor_config.js"></script>

        <link rel="stylesheet" href="%sueditor/themes/default/ueditor.css" />
    <script type="text/plain" id="id_%s" style="width:100%%" name="%s">%s</script><script type="text/javascript">
            var editor = new UE.ui.Editor();
            editor.render('id_%s');
        </script>''' % (settings.STATIC_URL, (company_id and ['%s/' % company_id] or ['/'])[0], settings.STATIC_URL, settings.STATIC_URL, settings.STATIC_URL, name, name,
                        (content.value() and [content.value()] or [''])[0], name)
    return html


@register.filter(name='ueditorReplay')
def ueditorReplay(content, name, company_id=''):
    """
    在线回复标签
    by:王健 at:2015-06-14
    :param content:
    :param name:
    :param company_id:
    :return:
    """
    html = '''
    <script type="text/javascript">
            <!--
            window.UEDITOR_HOME_URL = '%sueditor/%s';
            //-->
        </script>
        <script type="text/javascript" src="%sueditor/editor.min.js"></script>
        <script type="text/javascript" src="%sueditor/editor_help_config.js"></script>

        <link rel="stylesheet" href="%sueditor/themes/default/ueditor.css" />
    <script type="text/plain" id="u_editor" style="width:100%%" name="%s">%s</script><script type="text/javascript">
            var editor = new UE.ui.Editor();
            editor.render('u_editor');
        </script>''' % (
        settings.STATIC_URL, (company_id and ['%s/' % company_id] or ['/'])[0], settings.STATIC_URL, settings.STATIC_URL, settings.STATIC_URL, name, content)
    return html