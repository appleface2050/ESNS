# coding=utf-8
# Date: 14/11/13
# Time: 14:59
# Email:fanjunwei003@163.com
import json
from django.core.management import BaseCommand
from needserver.models import Project
from webappjs.base import tform
from webappjs.base.tform import Field

__author__ = u'范俊伟'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Field.for_mustache = True
        model = Project
        form = [
            tform.TextField(model=model, name='name'),
            tform.TextField(model=model, name='total_name'),
            tform.TextField(model=model, name='address'),
            tform.IntField(model=model, name='jzmj'),
            tform.TextField(model=model, name='jglx'),
            tform.IntField(model=model, name='jzcs'),
            tform.IntField(model=model, name='htzj'),
            tform.DateField(model=model, name='kg_date'),
            tform.IntField(model=model, name='days'),
            tform.TextField(model=model, name='jsdw'),
            tform.TextField(model=model, name='jsdw_fzr'),
            tform.TextField(model=model, name='kcdw'),
            tform.TextField(model=model, name='kcdw_fzr'),
            tform.TextField(model=model, name='sgdw'),
            tform.TextField(model=model, name='sgdw_fzr'),
            tform.TextField(model=model, name='jldw'),
            tform.TextField(model=model, name='jldw_fzr'),
            tform.TextField(model=model, name='sjdw'),
            tform.TextField(model=model, name='sjdw_fzr'),
        ]

        for i in form:
            print unicode(i).encode('utf-8')



