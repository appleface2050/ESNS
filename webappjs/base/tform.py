# coding=utf-8
# Date: 15/1/19
# Time: 16:19
# Email:fanjunwei003@163.com
"""
表单模板相关类,主要用于快速构建初始页面,提供一种比django自带From的轻量级且灵活的Form界面构建
由于本系统大都采用js在前台处理数据,所以此模板设计去掉表单验证相关功能
"""
from django.template import loader

__author__ = u'范俊伟'


class Field(object):
    """
    表单模板字段基类
    by:范俊伟 at:2015-01-21
    增加与model的关联,便于自动生成label和和helper_text
    by:范俊伟 at:2015-01-21
    """

    name = None
    label = None
    value = None
    required = True
    help_text = None
    template = None
    input_check = None
    errors = []
    model = None
    # 如果没有设置filed_name,则使用name作为filed_name
    filed_name = None
    for_mustache = False

    def __init__(self, name=None, label=None, value=None, required=True, help_text=None, template=None, errors=None,
                 input_check=None, model=None, filed_name=None):
        '''
        初始化
        by:范俊伟 at:2015-01-21
        :param name: input name属性
        :param label: label显示内容
        :param value: input 默认值
        :param required: 是否是必须的
        :param help_text: 帮助文字
        :param template: 所使用的模板
        :param errors: 默认错误
        :param input_check: 自定义js校验函数
        :param model:数据库,便于自动生成label和helper_text
        :param filed_name:所对应的模型字段,如果不设置,默认采用name值
        '''
        self.name = name
        self.label = label
        self.value = value
        self.required = required
        self.help_text = help_text
        if template:
            self.template = template
        self.errors = errors
        self.input_check = input_check
        self.model = model
        self.filed_name = filed_name

    def auto_id(self):
        '''
        input id属性
        by:范俊伟 at:2015-01-21
        '''
        return self.name

    def render(self):
        '''
        根据模板渲染生成html
        by:范俊伟 at:2015-01-21
        '''
        if self.model != None:
            if self.filed_name == None:
                self.filed_name = self.name
            for field in self.model._meta.fields:
                if field.name == self.filed_name:
                    if self.label == None:
                        self.label = field.verbose_name
                    if self.help_text == None:
                        self.help_text = field.help_text

        if self.required and not self.input_check:
            self.input_check = u"required"
        if self.for_mustache:
            self.value = '{{ ' + self.name + ' }}'
        if self.template:
            content = loader.render_to_string(self.template, {'field': self})
            return content
        else:
            return ''

    def __unicode__(self):
        return self.render()


class TextField(Field):
    """
    单行文本字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_text.html'
    max_length = None

    def __init__(self, max_length=None, **kwargs):
        '''
        初始化
        by:范俊伟 at:2015-01-21
        :param max_length: 文本最多长度
        '''
        self.max_length = max_length
        super(TextField, self).__init__(**kwargs)


class NumberField(TextField):
    '''
    数字文本字段
    by:范俊伟 at:2015-02-03
    '''

    def __init__(self, max_length=None, **kwargs):
        super(TextField, self).__init__(**kwargs)
        if self.required:
            self.input_check = 'required,number'
        else:
            self.input_check = 'number'


class IntField(TextField):
    '''
    数字文本字段
    by:范俊伟 at:2015-02-03
    '''

    def __init__(self, max_length=None, **kwargs):
        super(TextField, self).__init__(**kwargs)
        if self.required:
            self.input_check = 'required,int'
        else:
            self.input_check = 'int'


class DateTimeField(Field):
    """
    时间日期字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_datetime.html'
    date = None
    time = None

    def __init__(self, date=None, time=None, **kwargs):
        '''
        初始化
        by:范俊伟 at:2015-01-21
        :param date: 日期
        :param time: 时间
        '''
        self.date = date
        self.time = time
        super(DateTimeField, self).__init__(**kwargs)


class CheckboxField(Field):
    """
    选择框字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_checkbox.html'
    value = False


class HiddenField(Field):
    """
    隐藏字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_hidden.html'


class PasswordField(TextField):
    """
    密码字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_password.html'


class SelectField(Field):
    """
    下拉列表字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_select.html'
    choices = []

    def __init__(self, choices=None, **kwargs):
        '''
        初始化
        by:范俊伟 at:2015-01-21
        :param choices:(key,value)列表
        '''
        self.choices = choices
        super(SelectField, self).__init__(**kwargs)


class DateField(Field):
    """
    日期字段
    by:范俊伟 at:2015-01-21
    """
    template = 'web/include/form_field_date.html'
    date = None
    time = None

    def __init__(self, date=None, **kwargs):
        '''
        初始化
        by:范俊伟 at:2015-01-21
        :param date:日期
        '''
        self.date = date
        super(DateField, self).__init__(**kwargs)








