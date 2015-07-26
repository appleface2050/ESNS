# coding=utf-8
# Date: 15/1/25'
# Email: wangjian2254@icloud.com
import logging
import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.http import HttpResponseRedirect, HttpResponse

from alipay.alipay import create_direct_phone_pay, get_auth, parseXml, notify_verify, create_direct_pay_by_user, \
    notify_pc_verify
from needserver.models import Project, Group, ProjectRechargeRecord, ProjectPersonChangeRecord
from util.tools import common_except_log
from webhtml.base import tform
from webhtml.base.views import BaseView, format_money
from webhtml.models import Order, Product, Address, Tax, PayOrder, STATUS_SUCCESS


need_log = logging.getLogger('need')
__author__ = u'王健'
# 确认支付
def zhifubao_pay(request):
    """
    修改函数名
    by: 范俊伟 at:2015-03-04
    修改支付宝接口
    by: 范俊伟 at:2015-03-06
    逻辑修改
    by: 范俊伟 at:2015-03-07
    :param request:
    :return:
    """
    order_id = request.REQUEST.get('order_id')
    pay_type = request.REQUEST.get('pay_type')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('id错误')

    payOrder = order.create_pay_order(pay_type)
    out_trade_no = payOrder.flag
    subject = payOrder.order.product.name
    total_fee = format_money(payOrder.real_price)
    request_token = get_auth(subject, out_trade_no, total_fee)
    url = create_direct_phone_pay(request_token)
    # 去支付页面
    return HttpResponseRedirect(url)


class ZhifubaoPayCompleteView(BaseView):
    """
    支付完成页
    by: 范俊伟 at:2015-03-07
    修改基类
    by: 范俊伟 at:2015-03-11
    """
    template_name = 'webhtml/phone/step5.html'

    def get_context_data(self, **kwargs):
        """
        获取页面参数
        by: 范俊伟 at:2015-03-07
        信息校验
        by: 范俊伟 at:2015-03-08
        修改支付逻辑
        by: 范俊伟 at:2015-03-12
        """
        need_log.debug('ZhifubaoPayCompleteView META:' + str(self.request.META))
        need_log.debug('ZhifubaoPayCompleteView GET:' + str(self.request.GET.items()))
        need_log.debug('ZhifubaoPayCompleteView POST:' + str(self.request.POST.items()))
        verify = notify_verify(self.request.GET)
        if not verify:
            messages.error(self.request, '校验失败')
            return super(ZhifubaoPayCompleteView, self).get_context_data(**kwargs)
        out_trade_no = self.request.REQUEST.get('out_trade_no')
        try:
            pay_order = PayOrder.objects.get(flag=out_trade_no)
        except PayOrder.DoesNotExist:
            messages.error(self.request, '订单不存在')
            return super(ZhifubaoPayCompleteView, self).get_context_data(**kwargs)
        if pay_order.status == STATUS_SUCCESS:
            kwargs['order'] = pay_order.order
            kwargs['success'] = True
        else:
            messages.error(self.request, '可能因为网络数据过多,支付还未完成,请稍后查看,请不要重复支付!')
        return super(ZhifubaoPayCompleteView, self).get_context_data(**kwargs)


class ZhifubaoPayCompleteViewV2(BaseView):
    """
    支付完成页
    by：尚宗凯 at：2015-04-22
    """
    template_name = 'webhtml/phone/pay_phone_v2/phone_pay_success.html'

    def get_context_data(self, **kwargs):
        """
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """
        need_log.debug('ZhifubaoPayCompleteView META:' + str(self.request.META))
        need_log.debug('ZhifubaoPayCompleteView GET:' + str(self.request.GET.items()))
        need_log.debug('ZhifubaoPayCompleteView POST:' + str(self.request.POST.items()))
        verify = notify_verify(self.request.GET)
        if not verify:
            kwargs['message'] = '校验失败'
            return super(ZhifubaoPayCompleteViewV2, self).get_context_data(**kwargs)
        out_trade_no = self.request.REQUEST.get('out_trade_no')
        try:
            pay_order = PayOrder.objects.get(flag=out_trade_no)
        except PayOrder.DoesNotExist:
            kwargs['message'] = '订单不存在'
            return super(ZhifubaoPayCompleteViewV2, self).get_context_data(**kwargs)
        if pay_order.status == STATUS_SUCCESS:
            order = pay_order.order
            kwargs['order'] = order
            kwargs['success'] = True
            try:
                project_id = order.project_id
                product_id = order.product_id
                address_id = order.address_id

                p = Project.objects.get(pk=order.project_id)
                balance = get_project_balance_base(project_id)
                kwargs['project_name'] = p.name
                kwargs['person_nums'] = balance.get("person_nums")
                kwargs['balance'] = balance.get('total') - balance.get('price')
                kwargs['days'] = balance.get("days")

                product = Product.objects.get(pk=product_id)
                kwargs['gold'] = product.gold

                if address_id:
                    tax_id = order.tax_id
                    tax = Tax.objects.get(pk=tax_id)
                    kwargs["fptt"] = tax.fptt
                    address = Address.objects.get(pk=address_id)
                    kwargs["address"] = address.address_v2
                    kwargs["address_detail"] = address.address_detail
                    kwargs["zip_code"] = address.zip_code
                    kwargs["username"] = address.username
                    kwargs["phone"] = address.phone
                    kwargs["has_fp"] = "True"
            except Exception as e:
                print e
                kwargs['message'] = '订单不存在'

        else:
            kwargs['message'] = '订单不存在'
        return super(ZhifubaoPayCompleteViewV2, self).get_context_data(**kwargs)


def zhifubao_pay_callback(request):
    """
    支付宝回调页面
    by: 范俊伟 at:2015-03-06
    逻辑修改
    by: 范俊伟 at:2015-03-07
    信息校验
    by: 范俊伟 at:2015-03-08
    修改支付逻辑
    by: 范俊伟 at:2015-03-12
    :param request:
    :return:
    """
    need_log.debug('zhifubao_pay_callback META:' + str(request.META))
    need_log.debug('zhifubao_pay_callback GET:' + str(request.GET.items()))
    need_log.debug('zhifubao_pay_callback POST:' + str(request.POST.items()))
    need_log.debug('zhifubao_pay_callback body:' + str(request.body))
    try:
        verify = notify_verify(request.POST, ['service', 'v', 'sec_id', 'notify_data'], True)
        need_log.debug('zhifubao_pay_callback verify:' + str(verify))
        if verify:
            notify_data = parseXml(request.POST.get('notify_data').encode('utf-8'))
            out_trade_no = notify_data.get('out_trade_no')
            trade_status = notify_data.get('trade_status')
            if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                pay_order = PayOrder.objects.get(flag=out_trade_no)
                pay_order.success(notify_data.get('trade_no'))
            return HttpResponse('success')
        else:
            return HttpResponse('fail')
    except PayOrder.DoesNotExist:
        pass
    except:
        common_except_log()
    return HttpResponse('fail')


def zhifubao_pay_pc(request):
    """
    pc支付宝跳转接口
    by: 范俊伟 at:2015-03-04
    :param request:
    :return:
    """
    order_id = request.REQUEST.get('order_id')
    pay_type = request.REQUEST.get('pay_type')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('id错误')

    payOrder = order.create_pay_order(pay_type)
    out_trade_no = payOrder.flag
    subject = payOrder.order.product.name
    total_fee = format_money(payOrder.real_price)
    url = create_direct_pay_by_user(out_trade_no, subject, total_fee)
    # 去支付页面
    return HttpResponseRedirect(url)


class ZhifubaoPayPCCompleteView(BaseView):
    """
    pc支付完成页
    by: 范俊伟 at:2015-03-07
    """
    template_name = 'webhtml/step5.html'

    def get_context_data(self, **kwargs):
        """
        获取页面参数
        by: 范俊伟 at:2015-03-07
        """
        need_log.debug('ZhifubaoPayPCCompleteView META:' + str(self.request.META))
        need_log.debug('ZhifubaoPayPCCompleteView GET:' + str(self.request.GET.items()))
        need_log.debug('ZhifubaoPayPCCompleteView POST:' + str(self.request.POST.items()))
        verify = notify_verify(self.request.GET)
        if not verify:
            messages.error(self.request, '校验失败')
            return super(ZhifubaoPayPCCompleteView, self).get_context_data(**kwargs)
        out_trade_no = self.request.REQUEST.get('out_trade_no')
        try:
            pay_order = PayOrder.objects.get(flag=out_trade_no)
        except PayOrder.DoesNotExist:
            messages.error(self.request, '订单不存在')
            return super(ZhifubaoPayPCCompleteView, self).get_context_data(**kwargs)
        if pay_order.status == STATUS_SUCCESS:
            kwargs['order'] = pay_order.order
            kwargs['success'] = True
        else:
            messages.error(self.request, '可能因为网络数据过多,支付还未完成,请稍后查看,请不要重复支付!')
        return super(ZhifubaoPayPCCompleteView, self).get_context_data(**kwargs)


def zhifubao_pay_pc_callback(request):
    """
    pc支付宝回调页面
    by: 范俊伟 at:2015-03-06
    修改支付逻辑
    by: 范俊伟 at:2015-03-12
    :param request:
    :return:
    """
    need_log.debug('zhifubao_pay_pc_callback META:' + str(request.META))
    need_log.debug('zhifubao_pay_pc_callback GET:' + str(request.GET.items()))
    need_log.debug('zhifubao_pay_pc_callback POST:' + str(request.POST.items()))
    need_log.debug('zhifubao_pay_pc_callback body:' + str(request.body))
    try:
        verify = notify_pc_verify(request.POST)
        need_log.debug('zhifubao_pay_pc_callback verify:' + str(verify))
        if verify:
            out_trade_no = request.POST.get('out_trade_no')
            trade_status = request.POST.get('trade_status')
            if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                pay_order = PayOrder.objects.get(flag=out_trade_no)
                pay_order.success(request.POST.get('trade_no'))
            return HttpResponse('success')
        else:
            return HttpResponse('fail')
    except PayOrder.DoesNotExist:
        pass
    except:
        common_except_log()
    return HttpResponse('fail')


def get_project_balance_base(project_id):
    """
    获取项目的余额信息
    by:王健 at:2015-3-2
    修改 余额获取函数，未来应该写成一个
    by:王健 at:2015-3-15
    以消耗值 和 余额取反了
    by:王健 at:2015-3-16
    :param request:
    :param project_id:
    :return:
    """
    record_list = ProjectRechargeRecord.objects.filter(project_id=project_id).order_by('-date')[:1]
    if len(record_list) > 0:
        pre = record_list[0]
    else:
        pre = ProjectRechargeRecord(date=datetime.datetime(year=2105, month=1, day=1))
    result = {'total': pre.price2}
    ppcr = ProjectPersonChangeRecord.objects.filter(project_id=project_id).order_by('-create_date')[:1]
    if len(ppcr) == 1:
        ppcr = ppcr[0]
    result['price'] = result['total'] - ppcr.commit_value()
    if not result['price']:
        result['price'] = 0
    result['person_nums'] = ppcr.members
    result['days'] = ppcr.commit_days()
    return result


class PayViewV2(BaseView):
    """
    用户充值
    by:尚宗凯 at:2015-04-21
    充值界面修改
    by: 范俊伟 at:2015-05-13
    """
    template_name = 'webhtml/phone/pay_phone_v2/pay.html'
    view_id = 'charge'
    need_site_permission = True


    def post(self, request, *args, **kwargs):
        """
        post请求
        by:尚宗凯 at:2015-04-21
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """

        project_id = request.REQUEST.get('project_id')
        if not project_id:
            kwargs['message'] = '未选择项目'
            return self.get(request, *args, **kwargs)
        try:
            project = Project.objects.get(id=project_id)
        except Product.DoesNotExist:
            kwargs['message'] = '项目不存在'
            return self.get(request, *args, **kwargs)
        product_id = request.REQUEST.get('product_id')
        if not product_id:
            kwargs['message'] = '未选套餐'
            return self.get(request, *args, **kwargs)
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            kwargs['message'] = '套餐不存在'
            return self.get(request, *args, **kwargs)

        if project and project:
            tax = None
            # if (kwargs.get('has_fp') == '1'):
            if self.request.REQUEST.get("fp_check") == "yes" and self.request.REQUEST.get('fa_piao_tian_xie') == "True":
                address = Address()
                address.username = request.REQUEST.get('lxr')
                address.address_v2 = request.REQUEST.get('address')
                address.address_detail = request.REQUEST.get('jdxqdz')
                address.phone = request.REQUEST.get('lxdh')
                address.zip_code = request.REQUEST.get('yzbm')
                address.user = self.request.user
                address.save()
                tax = Tax()
                tax.fptt = request.REQUEST.get('fptt')
                tax.address = address
                tax.user = self.request.user
                tax.save()
            order = Order()
            order.user = self.request.user
            order.product = product
            order.price = order.real_price = product.price
            kwargs['origin'] = product.price - product.gift
            if tax:
                order.is_mail = True
            else:
                order.is_mail = False
            # if (kwargs.get('has_fp') == '1'):
            if self.request.REQUEST.get("fp_check") == "yes" and self.request.REQUEST.get('fa_piao_tian_xie') == "True":
                order.address = tax.address
                order.tax = tax
            else:
                order.address = None
                order.tax = None
            order.project = project
            order.save()

            if self.isPhoneRequest():
                url = '%s?pay_type=0&order_id=%s' % (reverse('zhifubao_pay'), order.id)
            else:
                url = '%s?pay_type=0&order_id=%s' % (reverse('zhifubao_pay_pc'), order.id)
            return HttpResponseRedirect(url)

            # return HttpResponseRedirect("/phone_pay"+self.get_query_string(new_params={"product_id":request.REQUEST.get("product_id")}))


    def get_context_data(self, **kwargs):
        """
        获取参数
        by: 尚宗凯 at:2015-04-21
        充值界面修改
        by: 范俊伟 at:2015-05-13
        :param kwargs:
        :return:
        """

        project_id = self.request.REQUEST.get('project_id')
        if project_id:
            try:
                p = Project.objects.get(pk=project_id)
                balance = get_project_balance_base(project_id)

                kwargs['project_name'] = p.name
                kwargs['person_nums'] = balance.get("person_nums")
                kwargs['balance'] = balance.get('total') - balance.get('price')
                kwargs['success'] = True
                kwargs['days'] = balance.get("days")

                if self.request.REQUEST.get('fa_piao_tian_xie') == "True":
                    kwargs['fa_piao_tian_xie'] = True
                    fapiao = {}
                    fapiao['address'] = self.request.REQUEST.get('address')
                    fapiao['fptt'] = self.request.REQUEST.get('fptt')
                    fapiao['jdxqdz'] = self.request.REQUEST.get('jdxqdz')
                    fapiao['yzbm'] = self.request.REQUEST.get('yzbm')
                    fapiao['lxr'] = self.request.REQUEST.get('lxr')
                    fapiao['lxdh'] = self.request.REQUEST.get('lxdh')
                    kwargs['fapiao'] = fapiao
            except Project.DoesNotExist:
                kwargs['success'] = False
                kwargs['message'] = '不存在此项目'
        else:
            kwargs['message'] = '未选择项目'
            return super(PayViewV2, self).get_context_data(**kwargs)

        product_id = self.request.REQUEST.get("product_id")
        if product_id:
            try:
                p = Product.objects.get(pk=product_id)
                kwargs['gold'] = p.gold
                kwargs['price'] = p.price / 100.
                kwargs['gift'] = p.gift
                kwargs["origin"] = p.gold - p.gift
                kwargs["this_pay_days"] = int(p.gold / kwargs['person_nums'])
            except Exception as e:
                print e
        return super(PayViewV2, self).get_context_data(**kwargs)


class PayProductChooseView(BaseView):
    '''
    手机充值套餐选择
    by: 尚宗凯 at:2015-04-21
        充值界面修改
        by: 范俊伟 at:2015-05-13
    '''
    view_id = 'phone_pay_product_choose'
    template_name = 'webhtml/phone/pay_phone_v2/phone_pay_product_choose.html'

    def post(self, request, *arg, **kwargs):
        """
        POST方法
        by: 尚宗凯 at:2015-04-21
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """
        return HttpResponseRedirect(
            "/phone_pay" + self.get_query_string(new_params={"product_id": request.REQUEST.get("product_id")}))

    def get_context_data(self, **kwargs):
        """
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """
        project_id = self.request.REQUEST.get('project_id')
        balance = get_project_balance_base(project_id)
        person_nums = balance.get("person_nums")
        kwargs['person_nums'] = person_nums
        query = Product.objects.filter(is_active=True).order_by('sorted')
        products = []
        for i in query:
            i.origin = i.gold - i.gift
            products.append(i)
        kwargs['products'] = products
        try:
            product_id = int(self.request.REQUEST.get("product_id"))
            kwargs['product_id'] = product_id
        except:
            pass
        return super(PayProductChooseView, self).get_context_data(**kwargs)


class PayReceiptView(BaseView):
    """
    手机支付发票填写
    by 尚宗凯 at：2015-04-21
    """
    view_id = 'phone_pay_receipt'

    def post(self, request, *arg, **kwargs):
        """
        post方法
        by:尚宗凯 at：2015-04-21
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """
        # args=request.session.get("pay_args")
        # if not args:
        # args={}
        # args.update(request.POST.dict())
        # args['fa_piao_tian_xie'] = True
        # request.session["pay_args"] = args
        new_params = {
            # "product_id": request.REQUEST.get("product_id"),
            "address": request.REQUEST.get("address"),
            "fptt": request.REQUEST.get("fptt"),
            "jdxqdz": request.REQUEST.get("jdxqdz"),
            "yzbm": request.REQUEST.get("yzbm"),
            "lxr": request.REQUEST.get("lxr"),
            "lxdh": request.REQUEST.get("lxdh"),
            "fa_piao_tian_xie": True
        }
        return HttpResponseRedirect("/phone_pay" + self.get_query_string(new_params=new_params))

    def get_context_data(self, **kwargs):
        """
        充值界面修改
        by: 范俊伟 at:2015-05-13
        """
        kwargs.update(self.request.GET.dict())
        self.template_name = 'webhtml/phone/pay_phone_v2/phone_pay_receipt.html'
        return super(PayReceiptView, self).get_context_data(**kwargs)


class ZhiFuXieYiView(BaseView):
    """
    支付协议
    by：尚宗凯 at：2015-04-23
    """
    view_id = 'zhi_fu_xie_yi'
    template_name = 'webhtml/phone/pay_phone_v2/zhi_fu_xie_yi.html'


class PayView(BaseView):
    """
    用户充值
    by:范俊伟 at:2015-02-11
    逻辑修改
    by: 范俊伟 at:2015-02-13
    获取项余额
    by: 范俊伟 at:2015-03-07
    修改基类
    by: 范俊伟 at:2015-03-11
    合并支付视图
    by: 范俊伟 at:2015-03-11
    """
    view_id = 'charge'
    need_site_permission = True
    step = 1

    def get(self, request, *args, **kwargs):
        """
        get请求
        by: 范俊伟 at:2015-02-11
        逻辑修改
        by: 范俊伟 at:2015-02-13
        创建订单和发票信息
        by: 范俊伟 at:2015-02-13
        修改表单字段
        by: 范俊伟 at:2015-03-08
        有project_id输入后,只显示一个项目
        by: 范俊伟 at:2015-03-11
        根据UserAgent调用不同模板
        by: 范俊伟 at:2015-03-11
        修改余额计算中的 days 和 project 中的 days 产生的bug
        by: 王健 at:2015-03-14
        修改发票表单字段
        by: 范俊伟 at:2015-03-19
        支付流程修改
        by: 范俊伟 at:2015-03-20
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        phone_template = {
            1: 'webhtml/phone/step1.html',
            2: 'webhtml/phone/step2.html',
            3: 'webhtml/phone/step3.html',
            4: 'webhtml/phone/step4.html',
        }
        pc_template = {
            1: 'webhtml/step1.html',
            2: 'webhtml/step2.html',
            3: 'webhtml/step3.html',
            4: 'webhtml/step4.html',
        }
        if self.isPhoneRequest():
            self.template_name = phone_template.get(self.step)
        else:
            self.template_name = pc_template.get(self.step)

        if self.step == 1:
            project_id = request.GET.get('project_id')
            if (project_id):
                kwargs['project_id'] = project_id
            kwargs['tform'] = [
                tform.HiddenField(name='product_id', value=kwargs.get('product_id')),
                tform.HiddenField(name='has_fp', value=kwargs.get('has_fp')),
                tform.HiddenField(name='fptt', value=kwargs.get('fptt')),
                tform.HiddenField(name='username', value=kwargs.get('username')),
                tform.HiddenField(name='tel', value=kwargs.get('tel')),
                tform.HiddenField(name='taxtype', value=kwargs.get('taxtype')),
                tform.HiddenField(name='taxnum', value=kwargs.get('taxnum')),
                tform.HiddenField(name='companyaddress', value=kwargs.get('companyaddress')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='banknum', value=kwargs.get('banknum')),
                tform.HiddenField(name='bankaddress', value=kwargs.get('bankaddress')),
                tform.HiddenField(name='addr_name', value=kwargs.get('addr_name')),
                tform.HiddenField(name='addr_username', value=kwargs.get('addr_username')),
                tform.HiddenField(name='addr_address', value=kwargs.get('addr_address')),
                tform.HiddenField(name='addr_address_detail', value=kwargs.get('addr_address_detail')),
                tform.HiddenField(name='addr_tel', value=kwargs.get('addr_tel')),
                tform.HiddenField(name='addr_phone', value=kwargs.get('addr_phone')),
            ]
            if not project_id:
                projects_query = []
                query_set = Group.objects.filter(type='sys_manage').filter(
                    Q(say_members=request.user) | Q(look_members=request.user))
                for i in query_set:
                    projects_query.append(i.project)

                query_set = Project.objects.filter(manager=request.user)
                for i in query_set:
                    if not i in projects_query:
                        projects_query.append(i)
                projects = []
                for i in projects_query:
                    project = i.toJSON()
                    res = get_project_balance_base(i.id)
                    project['balance'] = res.get('total') - res.get('price')
                    project['days'] = res.get('days')
                    projects.append(project)
                kwargs['projects'] = projects
                kwargs['projects_count'] = len(projects_query)
            else:
                kwargs['onProject'] = True
                try:
                    project = Project.objects.get(id=project_id)
                    res = get_project_balance_base(project.id)
                    p = project.toJSON()
                    del p['days']
                    res.update(p)
                    res['balance'] = res.get('total') - res.get('price')
                    kwargs['project'] = res
                    kwargs['success'] = True
                except Project.DoesNotExist:
                    kwargs['success'] = False
                    messages.error(request, '不存在此项目')
        elif self.step == 2:
            kwargs['tform'] = [
                tform.HiddenField(name='project_id', value=kwargs.get('project_id')),

                tform.HiddenField(name='has_fp', value=kwargs.get('has_fp')),
                tform.HiddenField(name='fptt', value=kwargs.get('fptt')),
                tform.HiddenField(name='username', value=kwargs.get('username')),
                tform.HiddenField(name='tel', value=kwargs.get('tel')),
                tform.HiddenField(name='taxtype', value=kwargs.get('taxtype')),
                tform.HiddenField(name='taxnum', value=kwargs.get('taxnum')),
                tform.HiddenField(name='companyaddress', value=kwargs.get('companyaddress')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='banknum', value=kwargs.get('banknum')),
                tform.HiddenField(name='bankaddress', value=kwargs.get('bankaddress')),
                tform.HiddenField(name='addr_name', value=kwargs.get('addr_name')),
                tform.HiddenField(name='addr_username', value=kwargs.get('addr_username')),
                tform.HiddenField(name='addr_address', value=kwargs.get('addr_address')),
                tform.HiddenField(name='addr_address_detail', value=kwargs.get('addr_address_detail')),
                tform.HiddenField(name='addr_tel', value=kwargs.get('addr_tel')),
                tform.HiddenField(name='addr_phone', value=kwargs.get('addr_phone')),
            ]
            kwargs['products'] = Product.objects.all()
        elif self.step == 3:
            model = Tax
            addr_model = Address
            kwargs['tform'] = [
                tform.HiddenField(name='project_id', value=kwargs.get('project_id')),
                tform.HiddenField(name='product_id', value=kwargs.get('product_id')),
                tform.SelectField(label='开发票', name='has_fp', choices=[('0', '否'), ( '1', '是')],
                                  template='webhtml/include/phone/form_field_select.html', value=kwargs.get('has_fp')),

            ]

            kwargs['tform2'] = [
                tform.TextField(name='fptt', model=model, value=kwargs.get('fptt'),
                                template='webhtml/include/phone/form_field_text.html'),
            ]
            kwargs['tform3'] = [
                tform.TextField(filed_name='username', model=addr_model, name='addr_username',
                                value=kwargs.get('addr_username'),
                                template='webhtml/include/phone/form_field_text.html'),
                tform.CityField(filed_name='address_v2', model=addr_model, name='addr_address',
                                value=kwargs.get('addr_address'),
                                template='webhtml/include/phone/form_field_address_v2.html'),
                tform.TextField(filed_name='address_detail', model=addr_model, name='addr_address_detail',
                                value=kwargs.get('addr_address_detail'),
                                template='webhtml/include/phone/form_field_text.html'),
                tform.TextField(filed_name='phone', model=addr_model, name='addr_phone', required=True,
                                value=kwargs.get('addr_phone'), template='webhtml/include/phone/form_field_text.html'),
            ]
        elif self.step == 4:
            project_id = request.REQUEST.get('project_id')
            if not project_id:
                messages.error(request, '未选择项目')
                return self.get(request, *args, **kwargs)
            try:
                project = Project.objects.get(id=project_id)
            except Product.DoesNotExist:
                messages.error(request, '项目不存在')
                return self.get(request, *args, **kwargs)
            product_id = request.REQUEST.get('product_id')
            if not product_id:
                messages.error(request, '未选套餐')
                return self.get(request, *args, **kwargs)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, '套餐不存在')
                return self.get(request, *args, **kwargs)
            kwargs['project'] = project
            kwargs['product'] = product
            kwargs['has_fp_bool'] = (kwargs.get('has_fp') == '1')
            kwargs['tform'] = [
                tform.HiddenField(name='project_id', value=kwargs.get('project_id')),
                tform.HiddenField(name='product_id', value=kwargs.get('product_id')),
                tform.HiddenField(name='has_fp', value=kwargs.get('has_fp')),
                tform.HiddenField(name='fptt', value=kwargs.get('fptt')),
                tform.HiddenField(name='username', value=kwargs.get('username')),
                tform.HiddenField(name='tel', value=kwargs.get('tel')),
                tform.HiddenField(name='taxtype', value=kwargs.get('taxtype')),
                tform.HiddenField(name='taxnum', value=kwargs.get('taxnum')),
                tform.HiddenField(name='companyaddress', value=kwargs.get('companyaddress')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='companytel', value=kwargs.get('companytel')),
                tform.HiddenField(name='banknum', value=kwargs.get('banknum')),
                tform.HiddenField(name='bankaddress', value=kwargs.get('bankaddress')),
                tform.HiddenField(name='addr_name', value=kwargs.get('addr_name')),
                tform.HiddenField(name='addr_username', value=kwargs.get('addr_username')),
                tform.HiddenField(name='addr_address', value=kwargs.get('addr_address')),
                tform.HiddenField(name='addr_address_detail', value=kwargs.get('addr_address_detail')),
                tform.HiddenField(name='addr_tel', value=kwargs.get('addr_tel')),
                tform.HiddenField(name='addr_phone', value=kwargs.get('addr_phone')),
            ]

        return super(PayView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 范俊伟 at:2015-02-11
        逻辑修改
        by: 范俊伟 at:2015-02-13
        修改逻辑
        by: 尚宗凯 at:2015-03-25
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs.update(self.request.POST.dict())
        if '__state_1' in request.POST:
            self.step = 1
        elif '__state_2' in request.POST:
            project_id = request.REQUEST.get('project_id')
            if not project_id:
                messages.error(request, '未选择项目')
                self.step = 1
                return self.get(request, *args, **kwargs)
            self.step = 2
        elif '__state_3' in request.POST:
            product_id = request.REQUEST.get('product_id')
            if not product_id:
                messages.error(request, '未选套餐')
                self.step = 2
                return self.get(request, *args, **kwargs)
            self.step = 3
        elif '__state_4' in request.POST:
            self.step = 4
        elif '__state_5' in request.POST:
            project_id = request.REQUEST.get('project_id')
            if not project_id:
                messages.error(request, '未选择项目')
                return self.get(request, *args, **kwargs)
            try:
                project = Project.objects.get(id=project_id)
            except Product.DoesNotExist:
                messages.error(request, '项目不存在')
                return self.get(request, *args, **kwargs)
            product_id = request.REQUEST.get('product_id')
            if not product_id:
                messages.error(request, '未选套餐')
                return self.get(request, *args, **kwargs)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, '套餐不存在')
                return self.get(request, *args, **kwargs)

            if project and project:
                tax = None
                if (kwargs.get('has_fp') == '1'):
                    address = Address()
                    address.username = kwargs.get('addr_username')
                    address.address_v2 = kwargs.get('addr_address')
                    address.address_detail = kwargs.get('addr_address_detail')
                    address.phone = kwargs.get('addr_phone')
                    address.user = self.request.user
                    address.save()
                    tax = Tax()
                    tax.fptt = kwargs.get('fptt')
                    tax.address = address
                    tax.user = self.request.user
                    tax.save()
                order = Order()
                order.user = self.request.user
                order.product = product
                order.price = order.real_price = product.price
                if tax:
                    order.is_mail = True
                else:
                    order.is_mail = False
                if (kwargs.get('has_fp') == '1'):
                    order.address = tax.address
                    order.tax = tax
                else:
                    order.address = None
                    order.tax = None
                order.project = project
                order.save()

                if self.isPhoneRequest():
                    url = '%s?pay_type=0&order_id=%s' % (reverse('zhifubao_pay'), order.id)
                else:
                    url = '%s?pay_type=0&order_id=%s' % (reverse('zhifubao_pay_pc'), order.id)
                return HttpResponseRedirect(url)

        if '__back_state_1' in request.POST:
            self.step = 1
        elif '__back_state_2' in request.POST:
            self.step = 2
        elif '__back_state_3' in request.POST:
            self.step = 3

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        获取参数
        by: 范俊伟 at:2015-02-11
        逻辑修改
        by: 范俊伟 at:2015-02-13
        :param kwargs:
        :return:
        """
        return super(PayView, self).get_context_data(**kwargs)


class PayOrderView(BaseView):
    """
    继续支付未完成订单
    by:范俊伟 at:2015-02-11
    """
    need_site_permission = True
    step = 1

    def get(self, request, *args, **kwargs):
        """
        get请求
        by: 范俊伟 at:2015-02-11
        """

        if self.isPhoneRequest():
            self.template_name = 'webhtml/phone/step_pay_order.html'
        else:
            self.template_name = 'webhtml/step_pay_order.html'

        order_id = request.REQUEST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            messages.error(request, '订单不存在')
            return super(PayOrderView, self).get(request, *args, **kwargs)

        kwargs['order'] = order
        kwargs['product'] = order.product
        kwargs['project'] = order.project
        if order.tax:
            kwargs['has_fp_bool'] = True
            kwargs['fptt'] = order.tax.fptt
            kwargs['addr_username'] = order.address.username
            kwargs['addr_address'] = order.address.address_v2
            kwargs['addr_address_detail'] = order.address.address_detail
            kwargs['addr_phone'] = order.address.phone

        return super(PayOrderView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        """
        获取参数
        by: 范俊伟 at:2015-02-11
        逻辑修改
        by: 范俊伟 at:2015-02-13
        :param kwargs:
        :return:
        """
        return super(PayOrderView, self).get_context_data(**kwargs)


def cancel_order(request):
    """
    取消未完成订单
    by: 范俊伟 at:2015-03-20
    :param request:
    :return:
    """
    order_id = request.REQUEST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
        order.cancel()
    except Order.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('user_center'))


class JiFenView(BaseView):
    """
    积分页面
    by: 王健 at:2015-03-10
    修改基类
    by: 范俊伟 at:2015-03-11
	改为正在建设中
	by：尚宗凯 at：2015-04-29
    """
    # template_name = 'webhtml/phone/jifen_role.html'
    template_name = 'webhtml/phone/jifen_role_detail.html'
    # template_name = 'webhtml/phone/not_ready_yet.html'


class JiFenDetailView(BaseView):
    """
    积分详情
    by：尚宗凯 at：2015-04-27
    """
    template_name = 'webhtml/phone/jifen_role_detail.html'


class UserXieYiView(BaseView):
    """
    积分页面
    by: 王健 at:2015-03-10
    修改基类
    by: 范俊伟 at:2015-03-11
    """
    template_name = 'webhtml/phone/jifen_role.html'


class ProjectPayDetail(BaseView):
    """
    项目账户信息
    by:王健 at:2015-05-14
    """
    template_name = 'webhtml/phone/xiangmuzhanghuxinxi.html'

    def get(self, request, *args, **kwargs):
        """
        get请求
        by:王健 at:2015-05-14
        """

        project_id = request.REQUEST.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Order.DoesNotExist:
            messages.error(request, '项目不存在')
            return super(ProjectPayDetail, self).get(request, *args, **kwargs)

        res = get_project_balance_base(project.id)
        p = project.toJSON()
        del p['days']
        res.update(p)
        res['balance'] = res.get('total') - res.get('price')
        kwargs['project'] = res
        try:
            kwargs['balance_persent'] = int(((res['balance'] * 1.0) / res['total'])*100)
        except:
            kwargs['balance_persent'] = 100
        if 75 <= kwargs['balance_persent'] <= 100:
            kwargs['classname'] = 'green'
        elif 50 <= kwargs['balance_persent'] <= 74:
            kwargs['classname'] = 'yellow'
        elif 25 <= kwargs['balance_persent'] <= 49:
            kwargs['classname'] = 'orange'
        else:
            kwargs['classname'] = 'red'

        return super(ProjectPayDetail, self).get(request, *args, **kwargs)


class ProjectPayDetailAppleCheck(BaseView):
    """
    项目账户信息，苹果审核用
    by:王健 at:2015-05-14
    """
    template_name = 'webhtml/phone/xiangmuzhanghuxinxi_applecheck.html'

    def get(self, request, *args, **kwargs):
        """
        get请求
        by:王健 at:2015-05-14
        修复project_id不存在bug
        by:王健 at:2015-05-22
        """

        project_id = request.REQUEST.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Order.DoesNotExist:
            messages.error(request, '项目不存在')
            return super(ProjectPayDetailAppleCheck, self).get(request, *args, **kwargs)
        res = get_project_balance_base(project.id)
        p = project.toJSON()
        del p['days']
        res.update(p)
        kwargs['project'] = res
        return super(ProjectPayDetailAppleCheck, self).get(request, *args, **kwargs)
