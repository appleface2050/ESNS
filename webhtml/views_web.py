# coding=utf-8
# Date: 15/1/25'
# Email: wangjian2254@icloud.com
from webhtml.base.views import BaseView
from webhtml.models import Product

__author__ = u'王健'


class ProductView(BaseView):
    '''
    前台web界面
    by:王健 at:2015-01-26
    修改基类
    by: 范俊伟 at:2015-03-11
    '''
    view_id = 'product'
    template_name = 'webhtml/product.html'
    title = u'天津依子轩科技有限公司'

    def get_context_data(self, **kwargs):
        '''
        设置 产品显示
        by:王健 at:2015-01-27
        '''
        kwargs['products'] = Product.objects.filter(is_active=True).order_by('sorted')
        return super(ProductView, self).get_context_data(**kwargs)


class BuyCarView(BaseView):
    """
    订单界面
    by:王健 at:2015-01-27
    修改基类
    by: 范俊伟 at:2015-03-11
    """
    view_id = 'buycar'
    template_name = 'webhtml/buycar.html'
    title = u'天津依子轩科技有限公司'

    def get_context_data(self, **kwargs):
        '''
        显示购物车界面
        by:王健 at:2015-01-27
        '''
        pids = self.request.session.get('pids', [])
        pid = self.request.REQUEST.get('pid')
        if int(pid) not in pids:
            pids.append(pid)
            self.request.session['pids'] = pids
        kwargs['products'] = Product.objects.filter(id__in=pids)

        return super(BuyCarView, self).get_context_data(**kwargs)


class CreateOrderView(BaseView):
    """
    生成订单
    by:王健 at:2015-01-28
    修改基类
    by: 范俊伟 at:2015-03-11
    """
    view_id = 'createorder'
    template_name = 'webhtml/createorder.html'
    title = u'天津依子轩科技有限公司'

    def get_context_data(self, **kwargs):
        '''
        显示购物车界面
        by:王健 at:2015-01-28
        '''
        pids = self.request.session.get('pids', [])
        pid = self.request.REQUEST.get('pid')
        if int(pid) not in pids:
            pids.append(pid)
            self.request.session['pids'] = pids
        kwargs['products'] = Product.objects.filter(id__in=pids)

        return super(CreateOrderView, self).get_context_data(**kwargs)